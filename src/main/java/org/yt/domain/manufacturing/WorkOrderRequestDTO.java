package com.example.domain.manufacturing.dto;

import lombok.Data;
import lombok.EqualsAndHashCode;

import java.util.Date;

/**
 * DTO class for Work Order Request.
 */
@Data
@EqualsAndHashCode(callSuper = false)
public class WorkOrderRequestDTO {

    private Long id;

    private String workOrderId;

    private String manufacturerId;

    private String productId;

    private int quantity;

    private Date requestedDateTime;

    private Date estimatedCompletionDate;

    private String status; // E.g., "PENDING", "IN_PROGRESS", "COMPLETED"

    private String priorityLevel; // E.g., "HIGH", "MEDIUM", "LOW"

    private String notes;

    private Long assignedWorkerId;

    public WorkOrderRequestDTO() {
        this.status = "PENDING";
        this.priorityLevel = "MEDIUM";
    }
}

This `WorkOrderRequestDTO` class is designed to represent a work order request in the manufacturing domain. It uses Lombok annotations for concise and clean code, specifically `@Data` which adds getters, setters, equals, hashCode, and toString methods, and `@EqualsAndHashCode(callSuper = false)` to avoid inheriting from a superclass if it also implements `equals` and `hashCode`.

### Key Points:
- **Fields**: The fields include basic details like the work order ID, manufacturer ID, product ID, quantity, timestamps, status, priority level, and notes.
- **Constructor**: A default constructor initializes the status to "PENDING" and sets the priority level to "MEDIUM".
- **Lombok Annotations**: `@Data` and `@EqualsAndHashCode` are used for convenient field management.

This DTO can be easily used in request and response handling between services or as a value object within the application.