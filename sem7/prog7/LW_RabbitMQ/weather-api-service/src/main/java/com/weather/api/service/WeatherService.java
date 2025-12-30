package com.weather.api.service;

import com.weather.api.dto.AggregatedWeatherReport;
import com.weather.api.dto.WeatherMessage;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.UUID;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.TimeoutException;

@Service
public class WeatherService {

    private static final Logger log = LoggerFactory.getLogger(WeatherService.class);

    private final RabbitTemplate rabbitTemplate;
    private final ConcurrentHashMap<String, CompletableFuture<AggregatedWeatherReport>> pendingRequests = new ConcurrentHashMap<>();

    @Value("${rabbitmq.exchange.weather}")
    private String exchangeName;

    @Value("${rabbitmq.routing-key.request}")
    private String requestRoutingKey;

    public WeatherService(RabbitTemplate rabbitTemplate) {
        this.rabbitTemplate = rabbitTemplate;
    }

    public AggregatedWeatherReport processWeatherRequest(List<String> cities) {
        String correlationId = UUID.randomUUID().toString();
        log.info("Processing weather request for {} cities with correlationId: {}", cities.size(), correlationId);

        CompletableFuture<AggregatedWeatherReport> future = new CompletableFuture<>();
        pendingRequests.put(correlationId, future);

        try {
            // Отправляем сообщения для каждого города
            for (String city : cities) {
                WeatherMessage message = new WeatherMessage(correlationId, city);
                rabbitTemplate.convertAndSend(exchangeName, requestRoutingKey, message);
                log.debug("Sent weather request for city: {} with correlationId: {}", city, correlationId);
            }

            // Ждем результата с таймаутом (30 секунд)
            AggregatedWeatherReport report = future.get(30, TimeUnit.SECONDS);
            log.info("Received aggregated report for correlationId: {}", correlationId);
            return report;

        } catch (TimeoutException e) {
            log.error("Timeout waiting for aggregated report for correlationId: {}", correlationId);
            pendingRequests.remove(correlationId);
            throw new RuntimeException("Timeout waiting for weather data", e);
        } catch (Exception e) {
            log.error("Error processing weather request for correlationId: {}", correlationId, e);
            pendingRequests.remove(correlationId);
            throw new RuntimeException("Error processing weather request", e);
        } finally {
            pendingRequests.remove(correlationId);
        }
    }

    @RabbitListener(queues = "${rabbitmq.queue.aggregated}")
    public void receiveAggregatedReport(AggregatedWeatherReport report) {
        log.info("Received aggregated report with correlationId: {}", report.getCorrelationId());
        
        CompletableFuture<AggregatedWeatherReport> future = pendingRequests.get(report.getCorrelationId());
        if (future != null) {
            future.complete(report);
            log.debug("Completed future for correlationId: {}", report.getCorrelationId());
        } else {
            log.warn("No pending request found for correlationId: {}", report.getCorrelationId());
        }
    }
}

