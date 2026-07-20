package com.example.domain.order.fulfillment.dto;

import lombok.Builder;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

import java.util.Date;

/**
 * DTO class representing a Shipment Dispatch Details including Shipping Label information.
 */
@Getter
@Setter
@Builder
@ToString
public class ShipmentDispatchDTO {

    private Long id; // Unique identifier for the shipment dispatch

    private String orderId; // Order ID associated with this shipment

    private String shippingLabelNumber; // The unique number of the shipping label

    private Date dispatchDate; // The date and time when the shipment was dispatched

    private String senderAddress; // Address from where the shipment is sent

    private String recipientAddress; // Address to which the shipment is being sent

    private String trackingNumber; // Tracking number for the shipment

    private String shippingMethod; // Method of shipping used (e.g., Standard, Express)

    private boolean isLabelPrinted; // Flag indicating if the label has been printed or not
}

### Explanation:
1. **Imports**: The necessary Lombok annotations (`@Getter`, `@Setter`, `@Builder`, and `@ToString`) are imported to simplify field accessors.
2. **Fields**:
   - `id`: A unique identifier for each shipment dispatch entry.
   - `orderId`: The ID of the order this shipment is associated with.
   - `shippingLabelNumber`: A unique number assigned to the shipping label.
   - `dispatchDate`: The date and time when the shipment was dispatched.
   - `senderAddress`: Address from where the shipment originates.
   - `recipientAddress`: Address to which the shipment is being sent.
   - `trackingNumber`: Tracking number for the shipment, useful for tracking purposes.
   - `shippingMethod`: Method of shipping used (e.g., Standard, Express).
   - `isLabelPrinted`: A boolean flag indicating whether the label has been printed or not.

This DTO class can be easily used in various parts of your application to represent and transfer shipment dispatch details.