package com.example.manufacturing.domain;

import javax.persistence.*;
import java.time.LocalDateTime;
import java.util.UUID;

@Entity
@Table(name = "telemetry_data")
public class TelemetryEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(unique = true, nullable = false)
    private UUID sensorId;

    @Column(nullable = false)
    private String sensorType;

    @Column(nullable = false)
    private double value;

    @Column(nullable = false)
    private LocalDateTime timestamp;

    public TelemetryEntity() {
        this.sensorId = UUID.randomUUID();
    }

    public TelemetryEntity(UUID sensorId, String sensorType, double value, LocalDateTime timestamp) {
        this.sensorId = sensorId;
        this.sensorType = sensorType;
        this.value = value;
        this.timestamp = timestamp;
    }

    @PrePersist
    protected void onCreate() {
        if (sensorId == null) {
            this.sensorId = UUID.randomUUID();
        }
    }

    public Long getId() {
        return id;
    }

    public UUID getSensorId() {
        return sensorId;
    }

    public String getSensorType() {
        return sensorType;
    }

    public double getValue() {
        return value;
    }

    public LocalDateTime getTimestamp() {
        return timestamp;
    }

    public void setSensorType(String sensorType) {
        this.sensorType = sensorType;
    }

    public void setValue(double value) {
        this.value = value;
    }

    public void setTimestamp(LocalDateTime timestamp) {
        this.timestamp = timestamp;
    }
}

### Explanation:
- **UUID(sensorId)**: Unique identifier for the sensor.
- **String(sensorType)**: Type of sensor (e.g., temperature, pressure).
- **double(value)**: Value read by the sensor.
- **LocalDateTime(timestamp)**: Timestamp when the value was recorded.

### Entity Configuration:
- **@Entity**: Marks this class as a JPA entity.
- **@Table(name = "telemetry_data")**: Specifies the table name in the database.
- **@Id @GeneratedValue(strategy = GenerationType.IDENTITY)**: Auto-generated primary key for the entity.
- **@PrePersist onCreate()**: Ensures that `sensorId` is generated if it is null during object creation.

This code is designed to be production-ready, with clear and concise methods for accessing and setting properties.