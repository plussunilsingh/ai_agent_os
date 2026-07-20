package com.example.warehouse.domain.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * DTO class for Reorder Notification.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ReorderNotificationDTO {

    /**
     * Unique identifier for the notification.
     */
    private String notificationId;

    /**
     * Identifier of the stock item that needs to be reordered.
     */
    private String stockItemId;

    /**
     * Current inventory level of the stock item.
     */
    private int currentInventoryLevel;

    /**
     * Minimum inventory threshold below which a reorder is needed.
     */
    private int minimumThreshold;

    /**
     * Recommended quantity to be ordered based on calculations.
     */
    private int recommendedOrderQuantity;

    /**
     * Reason for the notification (e.g., low stock, critical shortage).
     */
    private String reasonForNotification;

    /**
     * Timestamp when the notification was generated.
     */
    private java.util.Date timestamp;
}

This `ReorderNotificationDTO` class is designed to be used as a data transfer object for procurement alerts in the warehouse domain. It includes all necessary fields and annotations for easy use with modern Java frameworks such as Spring Boot. The `@Data`, `@Builder`, `@NoArgsConstructor`, and `@AllArgsConstructor` annotations from Lombok are used to reduce boilerplate code, making it cleaner and more maintainable.