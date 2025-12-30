package com.weather.api.dto;

public class WeatherMessage {
    private String correlationId;
    private String city;

    public WeatherMessage() {
    }

    public WeatherMessage(String correlationId, String city) {
        this.correlationId = correlationId;
        this.city = city;
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
}
