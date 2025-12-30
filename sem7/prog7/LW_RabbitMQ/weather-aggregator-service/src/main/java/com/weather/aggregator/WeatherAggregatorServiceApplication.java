package com.weather.aggregator;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;

@SpringBootApplication
@EnableScheduling
public class WeatherAggregatorServiceApplication {

    public static void main(String[] args) {
        SpringApplication.run(WeatherAggregatorServiceApplication.class, args);
    }
}



