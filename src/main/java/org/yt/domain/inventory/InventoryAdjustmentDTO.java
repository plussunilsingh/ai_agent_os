package com.example.domain.warehouse.dto;

import java.time.LocalDateTime;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * DTO class for representing an inventory adjustment.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class InventoryAdjustmentDTO {

    /**
     * Unique identifier for the inventory adjustment.
     */
    private String id;

    /**
     * Date and time when the inventory adjustment was made.
     */
    private LocalDateTime dateTime;

    /**
     * The type of adjustment (e.g., addition, subtraction).
     */
    private String adjustmentType;

    /**
     * Quantity of items adjusted.
     */
    private int quantity;

    /**
     * Description of the reason for the adjustment.
     */
    private String description;

    /**
     * ID of the warehouse where the adjustment was made.
     */
    private String warehouseId;

    /**
     * ID of the product being adjusted.
     */
    private String productId;

    /**
     * Status of the inventory adjustment (e.g., pending, confirmed).
     */
    private String status;

    /**
     * User who made the adjustment.
     */
    private String userId;

    /**
     * Audit trail for the inventory adjustment.
     */
    private String auditTrail;
}

This code defines a `InventoryAdjustmentDTO` class that is designed to represent an inventory adjustment in a warehouse management system. The class uses Lombok annotations to simplify boilerplate code, ensuring that it is production-ready with minimal overhead. Each field has been carefully named and annotated for clarity and maintainability.