package com.example.domain.manufacturing.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * DTO class representing the status of a production line.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ProductionLineDTO {

    /**
     * Unique identifier for the production line.
     */
    private Long id;

    /**
     * Name of the production line.
     */
    private String name;

    /**
     * Current status of the production line (e.g., running, stopped).
     */
    private String status;

    /**
     * Last updated timestamp of the production line status.
     */
    private java.util.Date lastUpdated;

    /**
     * Number of units produced in the last hour.
     */
    private Integer unitsProducedLastHour;

    /**
     * Number of units that are currently being processed.
     */
    private Integer unitsProcessing;

    /**
     * Reason for any current issues or errors, if applicable.
     */
    private String issueReason;
}

This `ProductionLineDTO` class is designed to represent the status of a production line in a manufacturing domain. It includes fields that are commonly needed when tracking and reporting on production lines, such as their ID, name, status, last updated timestamp, units produced in the last hour, current processing count, and issue reasons if applicable. The use of Lombok annotations (`@Data`, `@Builder`, `@NoArgsConstructor`, and `@AllArgsConstructor`) simplifies the boilerplate code for getters, setters, constructors, and builders, ensuring a clean and maintainable design.