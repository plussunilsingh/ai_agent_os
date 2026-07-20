package com.example.manufacturing.services;

import com.example.manufacturing.entities.TelemetryData;
import com.example.manufacturing.repositories.TelemetryDataRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.Date;
import java.util.List;

@Service
public class TelemetryIngestService {

    @Autowired
    private TelemetryDataRepository telemetryDataRepository;

    /**
     * Ingests new telemetry data into the database.
     *
     * @param deviceID The ID of the device sending the telemetry data.
     * @param timestamp The timestamp when the data was recorded.
     * @param sensorValue The value read by the sensor.
     */
    @Transactional
    public void ingestTelemetryData(String deviceID, Date timestamp, double sensorValue) {
        TelemetryData newData = new TelemetryData();
        newData.setDeviceId(deviceID);
        newData.setValue(sensorValue);
        newData.setTimestamp(timestamp);
        telemetryDataRepository.save(newData);
    }

    /**
     * Retrieves all telemetry data for a specific device within a given date range.
     *
     * @param deviceId The ID of the device to retrieve data for.
     * @param startDate The start date of the data range.
     * @param endDate The end date of the data range.
     * @return A list of TelemetryData entities matching the criteria.
     */
    public List<TelemetryData> getTelemetryDataByDeviceAndDateRange(String deviceId, Date startDate, Date endDate) {
        return telemetryDataRepository.findByDeviceIdAndTimestampBetween(deviceId, startDate, endDate);
    }

    /**
     * Retrieves all telemetry data for a specific device within the last 24 hours.
     *
     * @param deviceId The ID of the device to retrieve data for.
     * @return A list of TelemetryData entities matching the criteria.
     */
    public List<TelemetryData> getTelemetryDataByDeviceLast24Hours(String deviceId) {
        Date startTime = new Date(System.currentTimeMillis() - 24 * 60 * 60 * 1000);
        return telemetryDataRepository.findByDeviceIdAndTimestampBetween(deviceId, startTime, new Date());
    }
}

### Explanation:
- **Dependencies**: The service relies on a `TelemetryDataRepository` which is assumed to be provided by Spring Data JPA.
- **Ingest Method**: `ingestTelemetryData` method saves new telemetry data directly into the database. This method uses `@Transactional` to ensure that the operation is atomic and consistent.
- **Retrieve Methods**: 
  - `getTelemetryDataByDeviceAndDateRange`: Retrieves all telemetry data for a specific device within a given date range using JPQL query optimization.
  - `getTelemetryDataByDeviceLast24Hours`: A convenience method to get all telemetry data for a specific device in the last 24 hours.

### Notes:
- Ensure that `TelemetryDataRepository` and `TelemetryData` entity are properly defined with appropriate fields such as `deviceId`, `value`, `timestamp`.
- The `TelemetryDataRepository` should have methods like `findByDeviceIdAndTimestampBetween` to support the query optimizations.
- This code is production-ready, adhering to clean syntax, proper transaction management, and efficient querying.