package com.weather.aggregator.dto;

import java.util.Map;

public class WeatherResponse {
    private String correlationId;
    private String city;
    private Map<String, Object> weatherData;
    private boolean success;
    private String errorMessage;

    public WeatherResponse() {
    }

    public WeatherResponse(String correlationId, String city, Map<String, Object> weatherData, 
                          boolean success, String errorMessage) {
        this.correlationId = correlationId;
        this.city = city;
        this.weatherData = weatherData;
        this.success = success;
        this.errorMessage = errorMessage;
    }

    public String getCorrelationId() {
        return correlationId;
    }

    public void setCorrelationId(String correlationId) {
        this.correlationId = correlationId;
    }

    public String getCity() {
        return city;
    }

    public void setCity(String city) {
        this.city = city;
    }

    public Map<String, Object> getWeatherData() {
        return weatherData;
    }

    public void setWeatherData(Map<String, Object> weatherData) {
        this.weatherData = weatherData;
    }

    public boolean isSuccess() {
        return success;
    }

    public void setSuccess(boolean success) {
        this.success = success;
    }

    public String getErrorMessage() {
        return errorMessage;
    }

    public void setErrorMessage(String errorMessage) {
        this.errorMessage = errorMessage;
    }
}
