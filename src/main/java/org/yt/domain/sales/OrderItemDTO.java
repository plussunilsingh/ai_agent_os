package com.example.domain.order.fulfillment.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * DTO class representing an item in the order cart.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class OrderItemDTO {

    private Long id; // Unique identifier for the order item

    private String productId; // Identifier of the product in the item

    private Integer quantity; // Quantity of the product in the order item

    private Double unitPrice; // Price per unit of the product

    private Double totalCost; // Total cost of this item, calculated as quantity * unitPrice
}

### Explanation:
- **Lombok Annotations**:
  - `@Data`: Generates getters, setters, equals, hashCode, and constructor from fields.
  - `@Builder`: Creates a builder pattern to construct instances easily.
  - `@NoArgsConstructor` and `@AllArgsConstructor`: Generate no-args and all-args constructors.

### Usage Example:
OrderItemDTO orderItem = OrderItemDTO.builder()
    .id(1L)
    .productId("PROD123")
    .quantity(5)
    .unitPrice(9.99)
    .build();

This class is designed to be lightweight and efficient, making it suitable for use in DTOs, especially when dealing with cart items or order fulfillment scenarios.