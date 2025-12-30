package com.weather.consumer.dto;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.List;

@JsonIgnoreProperties(ignoreUnknown = true)
public class OpenWeatherMapResponse {
    private String name;
    
    @JsonProperty("main")
    private MainWeatherData main;
    
    @JsonProperty("weather")
    private List<WeatherInfo> weather;
    
    @JsonProperty("wind")
    private WindData wind;
    
    @JsonProperty("sys")
    private SystemData sys;

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public MainWeatherData getMain() {
        return main;
    }

    public void setMain(MainWeatherData main) {
        this.main = main;
    }

    public List<WeatherInfo> getWeather() {
        return weather;
    }

    public void setWeather(List<WeatherInfo> weather) {
        this.weather = weather;
    }

    public WindData getWind() {
        return wind;
    }

    public void setWind(WindData wind) {
        this.wind = wind;
    }

    public SystemData getSys() {
        return sys;
    }

    public void setSys(SystemData sys) {
        this.sys = sys;
    }
    
    @JsonIgnoreProperties(ignoreUnknown = true)
    public static class MainWeatherData {
        private Double temp;
        @JsonProperty("feels_like")
        private Double feelsLike;
        private Integer pressure;
        private Integer humidity;

        public Double getTemp() {
            return temp;
        }

        public void setTemp(Double temp) {
            this.temp = temp;
        }

        public Double getFeelsLike() {
            return feelsLike;
        }

        public void setFeelsLike(Double feelsLike) {
            this.feelsLike = feelsLike;
        }

        public Integer getPressure() {
            return pressure;
        }

        public void setPressure(Integer pressure) {
            this.pressure = pressure;
        }

        public Integer getHumidity() {
            return humidity;
        }

        public void setHumidity(Integer humidity) {
            this.humidity = humidity;
        }
    }
    
    @JsonIgnoreProperties(ignoreUnknown = true)
    public static class WeatherInfo {
        private String main;
        private String description;
        private String icon;

        public String getMain() {
            return main;
        }

        public void setMain(String main) {
            this.main = main;
        }

        public String getDescription() {
            return description;
        }

        public void setDescription(String description) {
            this.description = description;
        }

        public String getIcon() {
            return icon;
        }

        public void setIcon(String icon) {
            this.icon = icon;
        }
    }
    
    @JsonIgnoreProperties(ignoreUnknown = true)
    public static class WindData {
        private Double speed;
        private Integer deg;

        public Double getSpeed() {
            return speed;
        }

        public void setSpeed(Double speed) {
            this.speed = speed;
        }

        public Integer getDeg() {
            return deg;
        }

        public void setDeg(Integer deg) {
            this.deg = deg;
        }
    }
    
    @JsonIgnoreProperties(ignoreUnknown = true)
    public static class SystemData {
        private String country;

        public String getCountry() {
            return country;
        }

        public void setCountry(String country) {
            this.country = country;
        }
    }
}
