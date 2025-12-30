package com.weather.api.controller;

import com.weather.api.dto.AggregatedWeatherReport;
import com.weather.api.dto.WeatherRequestDto;
import com.weather.api.service.WeatherService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/weather")
@CrossOrigin(origins = "*")
public class WeatherController {

    private static final Logger log = LoggerFactory.getLogger(WeatherController.class);
    private final WeatherService weatherService;

    public WeatherController(WeatherService weatherService) {
        this.weatherService = weatherService;
    }

    @PostMapping("/forecast")
    public ResponseEntity<AggregatedWeatherReport> getWeatherForecast(@RequestBody WeatherRequestDto request) {
        log.info("Received weather forecast request for cities: {}", request.getCities());
        
        try {
            AggregatedWeatherReport report = weatherService.processWeatherRequest(request.getCities());
            return ResponseEntity.ok(report);
        } catch (Exception e) {
            log.error("Error processing weather forecast request", e);
            return ResponseEntity.internalServerError().build();
        }
    }
}

