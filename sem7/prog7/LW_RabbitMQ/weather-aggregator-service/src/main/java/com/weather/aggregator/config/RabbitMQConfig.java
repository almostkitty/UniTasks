package com.weather.aggregator.config;

import org.springframework.amqp.core.Binding;
import org.springframework.amqp.core.BindingBuilder;
import org.springframework.amqp.core.Queue;
import org.springframework.amqp.core.TopicExchange;
import org.springframework.amqp.rabbit.connection.ConnectionFactory;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.amqp.support.converter.Jackson2JsonMessageConverter;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class RabbitMQConfig {

    @Value("${rabbitmq.queue.response}")
    private String responseQueueName;

    @Value("${rabbitmq.queue.aggregated}")
    private String aggregatedQueueName;

    @Value("${rabbitmq.exchange.weather}")
    private String exchangeName;

    @Value("${rabbitmq.routing-key.response}")
    private String responseRoutingKey;

    @Value("${rabbitmq.routing-key.aggregated}")
    private String aggregatedRoutingKey;

    @Bean
    public TopicExchange weatherExchange() {
        return new TopicExchange(exchangeName);
    }

    @Bean
    public Queue responseQueue() {
        return new Queue(responseQueueName, true);
    }

    @Bean
    public Queue aggregatedQueue() {
        return new Queue(aggregatedQueueName, true);
    }

    @Bean
    public Binding responseBinding() {
        return BindingBuilder
                .bind(responseQueue())
                .to(weatherExchange())
                .with(responseRoutingKey);
    }

    @Bean
    public Binding aggregatedBinding() {
        return BindingBuilder
                .bind(aggregatedQueue())
                .to(weatherExchange())
                .with(aggregatedRoutingKey);
    }

    @Bean
    public Jackson2JsonMessageConverter messageConverter() {
        return new Jackson2JsonMessageConverter();
    }

    @Bean
    public RabbitTemplate rabbitTemplate(ConnectionFactory connectionFactory) {
        RabbitTemplate template = new RabbitTemplate(connectionFactory);
        template.setMessageConverter(messageConverter());
        return template;
    }
}



