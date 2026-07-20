package com.example.warehouse.domain.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * DTO class representing a Stock Item.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class StockItemDTO {

    private Long id;
    private String skuCode;
    private String productName;
    private int quantityInStock;
    private double unitPrice;
    private String supplierName;

    // Optional: You can add getters and setters if needed

}

This `StockItemDTO` class is a simple Data Transfer Object (DTO) designed to represent stock items in the Warehouse & Stock domain. It uses Lombok annotations for convenience, making it concise and clean.

- **@Data**: This annotation provides `equals`, `hashCode`, `toString`, and generates all getters and setters.
- **@Builder**: Allows for flexible object construction via a builder pattern.
- **@NoArgsConstructor** and **@AllArgsConstructor**: Provide default and fully parameterized constructors respectively.