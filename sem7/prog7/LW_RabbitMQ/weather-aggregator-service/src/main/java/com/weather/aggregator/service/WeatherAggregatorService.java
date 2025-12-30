package com.weather.aggregator.service;

import com.weather.aggregator.dto.AggregatedWeatherReport;
import com.weather.aggregator.dto.WeatherResponse;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;

import java.util.*;
import java.util.concurrent.ConcurrentHashMap;

@Service
public class WeatherAggregatorService {

    private static final Logger log = LoggerFactory.getLogger(WeatherAggregatorService.class);
    private final RabbitTemplate rabbitTemplate;
    private final ConcurrentHashMap<String, AggregationContext> aggregationStore = new ConcurrentHashMap<>();

    public WeatherAggregatorService(RabbitTemplate rabbitTemplate) {
        this.rabbitTemplate = rabbitTemplate;
    }

    @Value("${rabbitmq.exchange.weather}")
    private String exchangeName;

    @Value("${rabbitmq.routing-key.aggregated}")
    private String aggregatedRoutingKey;

    @Value("${aggregator.timeout}")
    private int timeoutSeconds;

    @RabbitListener(queues = "${rabbitmq.queue.response}")
    public void aggregateWeatherResponse(WeatherResponse response) {
        log.info("Received weather response for city: {} with correlationId: {}", 
                response.getCity(), response.getCorrelationId());

        AggregationContext context = aggregationStore.get(response.getCorrelationId());
        
        if (context == null) {
            log.warn("Received response for unknown correlationId: {}. Creating new context with unknown totalCities.", 
                    response.getCorrelationId());
            // Если контекст не найден, создаем новый с неизвестным totalCities
            // В этом случае агрегация завершится по таймауту или когда больше не будет новых ответов
            context = new AggregationContext(response.getCorrelationId(), -1);
            aggregationStore.put(response.getCorrelationId(), context);
        }

        final String correlationId = response.getCorrelationId();
        synchronized (context) {
            context.addResponse(response);
            context.updateLastResponseTime();
            log.debug("Added response for city: {}. Received: {}/{}", 
                    response.getCity(), context.getReceivedCount(), context.getTotalCities());

            // Для неизвестного количества городов завершаем агрегацию после небольшой задержки
            if (context.getTotalCities() == -1 && context.getReceivedCount() > 0) {
                final AggregationContext finalContext = context;
                // Запускаем проверку завершения через 2 секунды
                new Thread(() -> {
                    try {
                        Thread.sleep(2000); // Ждем 2 секунды для получения всех ответов
                        synchronized (finalContext) {
                            if (aggregationStore.containsKey(correlationId) && 
                                finalContext.getTotalCities() == -1) {
                                // Проверяем, были ли новые ответы за последние 2 секунды
                                long timeSinceLastResponse = System.currentTimeMillis() - finalContext.getLastResponseTime();
                                if (timeSinceLastResponse >= 2000) {
                                    log.info("Completing aggregation for unknown totalCities. correlationId: {}", 
                                            correlationId);
                                    completeAggregation(finalContext, correlationId);
                                }
                            }
                        }
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                    }
                }).start();
            }

            if (context.isComplete()) {
                completeAggregation(context, correlationId);
            }
        }
    }

    public void initializeAggregation(String correlationId, int totalCities) {
        log.info("Initializing aggregation for correlationId: {} with totalCities: {}", 
                correlationId, totalCities);
        
        AggregationContext context = new AggregationContext(correlationId, totalCities);
        aggregationStore.put(correlationId, context);
    }

    private void completeAggregation(AggregationContext context, String correlationId) {
        log.info("Aggregation complete for correlationId: {}. Sending aggregated report.", correlationId);
        
        AggregatedWeatherReport report = buildAggregatedReport(context);
        rabbitTemplate.convertAndSend(exchangeName, aggregatedRoutingKey, report);
        
        aggregationStore.remove(correlationId);
        log.info("Removed aggregation context for correlationId: {}", correlationId);
    }

    private AggregatedWeatherReport buildAggregatedReport(AggregationContext context) {
        Map<String, Object> aggregatedData = new HashMap<>();
        List<String> processedCities = new ArrayList<>();
        
        for (WeatherResponse response : context.getResponses()) {
            if (response.isSuccess() && response.getWeatherData() != null) {
                processedCities.add(response.getCity());
                aggregatedData.put(response.getCity(), response.getWeatherData());
            } else {
                log.warn("Failed response for city: {} - {}", response.getCity(), response.getErrorMessage());
                processedCities.add(response.getCity() + " (error: " + response.getErrorMessage() + ")");
            }
        }

        return new AggregatedWeatherReport(
                context.getCorrelationId(),
                aggregatedData,
                processedCities,
                context.getTotalCities(),
                context.getReceivedCount()
        );
    }

    @Scheduled(fixedRate = 10000) // Проверка каждые 10 секунд
    public void cleanupExpiredAggregations() {
        long currentTime = System.currentTimeMillis();
        long timeoutMillis = timeoutSeconds * 1000L;
        
        List<String> expiredIds = new ArrayList<>();
        
        for (Map.Entry<String, AggregationContext> entry : aggregationStore.entrySet()) {
            AggregationContext context = entry.getValue();
            long elapsed = currentTime - context.getStartTime();
            
            if (elapsed > timeoutMillis) {
                expiredIds.add(entry.getKey());
                log.warn("Found expired aggregation for correlationId: {}. Elapsed: {}ms. Sending partial report.", 
                        entry.getKey(), elapsed);
                
                // Отправляем частичный отчет с полученными данными
                synchronized (context) {
                    AggregatedWeatherReport report = buildAggregatedReport(context);
                    rabbitTemplate.convertAndSend(exchangeName, aggregatedRoutingKey, report);
                    log.info("Sent partial aggregated report for expired correlationId: {}", entry.getKey());
                }
            }
        }
        
        for (String correlationId : expiredIds) {
            aggregationStore.remove(correlationId);
            log.info("Removed expired aggregation context for correlationId: {}", correlationId);
        }
        
        if (!expiredIds.isEmpty()) {
            log.info("Cleaned up {} expired aggregation contexts", expiredIds.size());
        }
    }

    private static class AggregationContext {
        private final String correlationId;
        private final int totalCities;
        private final List<WeatherResponse> responses = new ArrayList<>();
        private final long startTime = System.currentTimeMillis();
        private long lastResponseTime = System.currentTimeMillis();
        private int receivedCount = 0;

        public AggregationContext(String correlationId, int totalCities) {
            this.correlationId = correlationId;
            this.totalCities = totalCities;
        }

        public String getCorrelationId() {
            return correlationId;
        }

        public int getTotalCities() {
            return totalCities;
        }

        public List<WeatherResponse> getResponses() {
            return responses;
        }

        public long getStartTime() {
            return startTime;
        }

        public int getReceivedCount() {
            return receivedCount;
        }

        public long getLastResponseTime() {
            return lastResponseTime;
        }

        public synchronized void addResponse(WeatherResponse response) {
            responses.add(response);
            receivedCount++;
        }

        public synchronized void updateLastResponseTime() {
            this.lastResponseTime = System.currentTimeMillis();
        }

        public synchronized boolean isComplete() {
            // Если totalCities == -1, значит контекст был создан автоматически
            // В этом случае не можем точно определить завершение, полагаемся на таймаут
            // Но для надежности, если получили хотя бы один ответ и прошло достаточно времени,
            // считаем завершенным (это обрабатывается в cleanupExpiredAggregations)
            if (totalCities == -1) {
                return false; // Завершение по таймауту
            }
            return receivedCount >= totalCities;
        }
    }
}

