package com.weather.consumer.client;

import com.weather.consumer.dto.OpenWeatherMapResponse;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestTemplate;

import java.util.HashMap;
import java.util.Map;

@Component
public class WeatherApiClient {

    private static final Logger log = LoggerFactory.getLogger(WeatherApiClient.class);
    private final RestTemplate restTemplate;

    public WeatherApiClient(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }

    @Value("${weather.api.key}")
    private String apiKey;

    @Value("${weather.api.url}")
    private String apiUrl;

    public Map<String, Object> getWeatherData(String city) {
        try {
            String url = String.format("%s?q=%s&appid=%s&units=metric&lang=ru", 
                    apiUrl, city, apiKey);
            
            log.info("Fetching weather data for city: {}", city);
            ResponseEntity<OpenWeatherMapResponse> response = restTemplate.getForEntity(
                    url, OpenWeatherMapResponse.class);
            
            OpenWeatherMapResponse weatherData = response.getBody();
            if (weatherData == null) {
                throw new RuntimeException("Empty response from OpenWeatherMap API");
            }
            
            Map<String, Object> result = new HashMap<>();
            result.put("city", weatherData.getName());
            result.put("country", weatherData.getSys() != null ? weatherData.getSys().getCountry() : "");
            result.put("temperature", weatherData.getMain() != null ? weatherData.getMain().getTemp() : null);
            result.put("feelsLike", weatherData.getMain() != null ? weatherData.getMain().getFeelsLike() : null);
            result.put("pressure", weatherData.getMain() != null ? weatherData.getMain().getPressure() : null);
            result.put("humidity", weatherData.getMain() != null ? weatherData.getMain().getHumidity() : null);
            result.put("description", weatherData.getWeather() != null && !weatherData.getWeather().isEmpty() 
                    ? weatherData.getWeather().get(0).getDescription() : "");
            result.put("main", weatherData.getWeather() != null && !weatherData.getWeather().isEmpty() 
                    ? weatherData.getWeather().get(0).getMain() : "");
            result.put("windSpeed", weatherData.getWind() != null ? weatherData.getWind().getSpeed() : null);
            result.put("windDeg", weatherData.getWind() != null ? weatherData.getWind().getDeg() : null);
            
            log.info("Successfully fetched weather data for city: {}", city);
            return result;
            
        } catch (RestClientException e) {
            log.error("Error fetching weather data for city: {}", city, e);
            throw new RuntimeException("Failed to fetch weather data: " + e.getMessage(), e);
        }
    }
}



