package com.weather.consumer.service;

import com.rabbitmq.client.Channel;
import com.weather.consumer.client.WeatherApiClient;
import com.weather.consumer.dto.WeatherMessage;
import com.weather.consumer.dto.WeatherResponse;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.amqp.support.AmqpHeaders;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.messaging.handler.annotation.Header;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.util.Map;

@Service
public class WeatherConsumerService {

    private static final Logger log = LoggerFactory.getLogger(WeatherConsumerService.class);
    private final WeatherApiClient weatherApiClient;
    private final RabbitTemplate rabbitTemplate;

    public WeatherConsumerService(WeatherApiClient weatherApiClient, RabbitTemplate rabbitTemplate) {
        this.weatherApiClient = weatherApiClient;
        this.rabbitTemplate = rabbitTemplate;
    }

    @Value("${rabbitmq.exchange.weather}")
    private String exchangeName;

    @Value("${rabbitmq.routing-key.response}")
    private String responseRoutingKey;

    @Value("${weather.api.delay}")
    private long delay;

    @RabbitListener(queues = "${rabbitmq.queue.request}")
    public void consumeWeatherRequest(
            WeatherMessage message,
            Channel channel,
            @Header(AmqpHeaders.DELIVERY_TAG) long deliveryTag) {
        
        log.info("Received weather request for city: {} with correlationId: {}", 
                message.getCity(), message.getCorrelationId());
        
        WeatherResponse response;
        
        try {
            // Добавляем задержку между запросами
            Thread.sleep(delay);
            
            // Получаем данные о погоде из OpenWeatherMap API
            Map<String, Object> weatherData = weatherApiClient.getWeatherData(message.getCity());
            
            // Формируем успешный ответ
            response = new WeatherResponse(
                    message.getCorrelationId(),
                    message.getCity(),
                    weatherData,
                    true,
                    null
            );
            
            log.info("Successfully fetched weather data for city: {}", message.getCity());
            
        } catch (Exception e) {
            log.error("Error processing weather request for city: {}", message.getCity(), e);
            
            // Формируем ответ с ошибкой
            response = new WeatherResponse(
                    message.getCorrelationId(),
                    message.getCity(),
                    null,
                    false,
                    e.getMessage()
            );
        }
        
        try {
            // Отправляем ответ в очередь
            rabbitTemplate.convertAndSend(exchangeName, responseRoutingKey, response);
            log.info("Sent weather response for city: {} with correlationId: {}", 
                    message.getCity(), message.getCorrelationId());
            
            // Подтверждаем обработку сообщения вручную
            channel.basicAck(deliveryTag, false);
            log.debug("Acknowledged message with deliveryTag: {}", deliveryTag);
            
        } catch (IOException e) {
            log.error("Error acknowledging message with deliveryTag: {}", deliveryTag, e);
            // В случае ошибки при подтверждении, сообщение вернется в очередь
            try {
                channel.basicNack(deliveryTag, false, true);
            } catch (IOException ex) {
                log.error("Error nacking message", ex);
            }
        }
    }
}



