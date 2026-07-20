package com.example.domain.order.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import java.util.List;

/**
 * Data Transfer Object (DTO) for Sales Order Request.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class SalesOrderRequestDTO {

    /**
     * Unique identifier of the customer.
     */
    @NotBlank(message = "Customer ID is mandatory")
    private String customerId;

    /**
     * List of items to be ordered, each item containing product details and quantity.
     */
    @NotNull(message = "Items list is mandatory")
    private List<OrderItemDTO> items;

    /**
     * Shipping address for the order.
     */
    @NotBlank(message = "Shipping Address is mandatory")
    private String shippingAddress;

    /**
     * Billing address for the order, can be different from shipping address.
     */
    private String billingAddress;

    /**
     * Special instructions for the order.
     */
    private String specialInstructions;

    /**
     * Expected delivery date for the order.
     */
    private java.time.LocalDate expectedDeliveryDate;

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class OrderItemDTO {

        /**
         * Unique identifier of the product.
         */
        @NotBlank(message = "Product ID is mandatory")
        private String productId;

        /**
         * Quantity of the product to be ordered.
         */
        @NotNull(message = "Quantity is mandatory")
        private int quantity;
    }
}

### Explanation:
- **Lombok Annotations**:
  - `@Data`: Generates getters, setters, `toString`, `equals`, and `hashCode`.
  - `@Builder`: Provides a builder pattern for object construction.
  - `@NoArgsConstructor` and `@AllArgsConstructor`: Generate no-argument and all-arguments constructors respectively.

- **Fields**:
  - `customerId`: Unique identifier of the customer making the order.
  - `items`: List of items to be ordered, each containing product details (`productId`) and quantity.
  - `shippingAddress`: Address where the order is to be shipped.
  - `billingAddress`: Optional address for billing; can be different from shipping address.
  - `specialInstructions`: Any special instructions related to the order.
  - `expectedDeliveryDate`: Expected delivery date of the order.

- **OrderItemDTO**:
  - Represents an item in the order, with fields `productId` and `quantity`.

This DTO is designed for use in a production environment, ensuring that all necessary validation checks are performed on incoming requests.