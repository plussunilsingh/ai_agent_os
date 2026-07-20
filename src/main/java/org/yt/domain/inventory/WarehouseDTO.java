package com.example.domain.dto;

import lombok.Data;
import java.util.List;

/**
 * Data Transfer Object (DTO) representing a summary of a warehouse.
 */
@Data
public class WarehouseDTO {

    private Long id;
    private String warehouseName;
    private String location;
    private Integer totalStockQuantity;
    private List<String> categories; // List of product categories available in the warehouse

    /**
     * Constructor to initialize all fields.
     *
     * @param id                    Unique identifier for the warehouse
     * @param warehouseName         Name of the warehouse
     * @param location              Physical location of the warehouse
     * @param totalStockQuantity    Total quantity of stock available in the warehouse
     * @param categories            List of product categories available in the warehouse
     */
    public WarehouseDTO(Long id, String warehouseName, String location, Integer totalStockQuantity, List<String> categories) {
        this.id = id;
        this.warehouseName = warehouseName;
        this.location = location;
        this.totalStockQuantity = totalStockQuantity;
        this.categories = categories;
    }

    /**
     * Default constructor for deserialization or object creation.
     */
    public WarehouseDTO() {}

    // Additional methods can be added here if needed
}

### Explanation:
1. **Imports**: The `lombok` library is used to automatically generate the necessary boilerplate code (like getters, setters, and constructors).
2. **Fields**:
   - `id`: Unique identifier for the warehouse.
   - `warehouseName`: Name of the warehouse.
   - `location`: Physical location of the warehouse.
   - `totalStockQuantity`: Total quantity of stock available in the warehouse.
   - `categories`: List of product categories available in the warehouse.
3. **Constructors**: 
   - A parameterized constructor to initialize all fields.
   - A default constructor for deserialization or object creation.
4. **Lombok Annotations**:
   - `@Data` from Lombok, which automatically generates getters, setters, and a default constructor.

This DTO can be used in various parts of the application where you need to transfer warehouse summary information, ensuring that it is clean, optimized, and easy to use.