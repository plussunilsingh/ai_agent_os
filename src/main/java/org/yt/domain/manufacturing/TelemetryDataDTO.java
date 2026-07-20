package com.example.domain.manufacturing.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Data Transfer Object (DTO) for telemetry data ingested from sensors.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class TelemetryDataDTO {
    
    private String sensorId;
    private Long timestamp;
    private double temperature;
    private double humidity;
    private String location;
    private String deviceType;

    // Additional fields can be added as needed for specific use cases

}

This DTO is designed to efficiently transfer telemetry data between layers in a production system. The `@Data`, `@Builder`, `@NoArgsConstructor`, and `@AllArgsConstructor` annotations from Lombok are used to reduce boilerplate code, enhancing readability and maintainability.