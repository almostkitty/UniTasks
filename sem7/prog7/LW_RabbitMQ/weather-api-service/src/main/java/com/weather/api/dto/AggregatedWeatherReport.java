package com.weather.api.dto;

import java.util.List;
import java.util.Map;

public class AggregatedWeatherReport {
    private String correlationId;
    private Map<String, Object> weatherData;
    private List<String> processedCities;
    private int totalCities;
    private int processedCount;

    public AggregatedWeatherReport() {
    }

    public AggregatedWeatherReport(String correlationId, Map<String, Object> weatherData, 
                                   List<String> processedCities, int totalCities, int processedCount) {
        this.correlationId = correlationId;
        this.weatherData = weatherData;
        this.processedCities = processedCities;
        this.totalCities = totalCities;
        this.processedCount = processedCount;
    }

    public String getCorrelationId() {
        return correlationId;
    }

    public void setCorrelationId(String correlationId) {
        this.correlationId = correlationId;
    }

    public Map<String, Object> getWeatherData() {
        return weatherData;
    }

    public void setWeatherData(Map<String, Object> weatherData) {
        this.weatherData = weatherData;
    }

    public List<String> getProcessedCities() {
        return processedCities;
    }

    public void setProcessedCities(List<String> processedCities) {
        this.processedCities = processedCities;
    }

    public int getTotalCities() {
        return totalCities;
    }

    public void setTotalCities(int totalCities) {
        this.totalCities = totalCities;
    }

    public int getProcessedCount() {
        return processedCount;
    }

    public void setProcessedCount(int processedCount) {
        this.processedCount = processedCount;
    }
}
