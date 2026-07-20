package com.example.domain.manufacturing.repository;

import com.example.domain.manufacturing.model.Telemetry;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Repository
public interface TelemetryRepository extends JpaRepository<Telemetry, Long> {

    /**
     * Retrieves a list of telemetry entries for a specific machine and date range.
     *
     * @param machineId The ID of the machine to filter by.
     * @param startDate Start date for the query.
     * @param endDate End date for the query.
     * @return A list of Telemetry entities that match the criteria.
     */
    @Transactional(readOnly = true)
    List<Telemetry> findByMachineIdBetweenDates(Long machineId, java.util.Date startDate, java.util.Date endDate);

    /**
     * Retrieves a single telemetry entry by its unique ID.
     *
     * @param id The unique identifier of the Telemetry entity to retrieve.
     * @return The Telemetry entity with the specified ID or null if not found.
     */
    @Transactional(readOnly = true)
    Telemetry findById(Long id);

    /**
     * Retrieves a list of telemetry entries that have exceeded their threshold values within a date range.
     *
     * @param machineId The ID of the machine to filter by.
     * @param startDate Start date for the query.
     * @param endDate End date for the query.
     * @return A list of Telemetry entities that match the criteria.
     */
    @Transactional(readOnly = true)
    List<Telemetry> findByMachineIdAndValueGreaterThanThresholdBetweenDates(Long machineId, java.util.Date startDate, java.util.Date endDate, double threshold);
}

This code defines a `TelemetryRepository` interface for handling CRUD operations on `Telemetry` entities in the context of manufacturing domain. The repository extends `JpaRepository`, which provides standard CRUD methods and additional query methods via Spring Data JPA.

The `findByMachineIdBetweenDates` method optimizes the retrieval by specifying date ranges directly, reducing unnecessary data fetching. The `findById` method retrieves a single entity efficiently by its unique ID. Lastly, `findByMachineIdAndValueGreaterThanThresholdBetweenDates` is a more complex query that filters telemetry entries based on multiple criteria, ensuring efficient execution with appropriate database indexes.

Ensure your entity and related classes are properly defined to match the above interface methods for this code to work seamlessly in your application.