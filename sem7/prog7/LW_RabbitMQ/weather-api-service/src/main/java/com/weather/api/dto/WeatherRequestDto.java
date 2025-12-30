package com.weather.api.dto;

import java.util.List;

public class WeatherRequestDto {
    private List<String> cities;

    public WeatherRequestDto() {
    }

    public WeatherRequestDto(List<String> cities) {
        this.cities = cities;
    }

    public List<String> getCities() {
        return cities;
    }

    public void setCities(List<String> cities) {
        this.cities = cities;
    }
}
