package com.example.domain.supplychain.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Data Transfer Object (DTO) for Category in the Material Catalog.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CategoryDTO {

    private Long id;
    private String name;
    private String description;
    private String categoryCode;
    private Boolean isActive;
    private Integer sortOrder;

    // Optional: Constructors, Getters, and Setters for additional fields can be added here if needed.
}

This `CategoryDTO` class is designed to transfer data related to categories in a material catalog between layers of an application. It uses Lombok annotations to reduce boilerplate code, making the class more concise and readable.

### Key Points:
- **Annotations**:
  - `@Data`: Generates getters, setters, `toString()`, `equals()`, and `hashCode()` methods.
  - `@Builder`: Provides a fluent builder pattern for creating objects.
  - `@NoArgsConstructor` and `@AllArgsConstructor`: Provide default constructors and a constructor with all fields.

- **Fields**:
  - `id`: Unique identifier of the category.
  - `name`: Name of the category.
  - `description`: Description of the category.
  - `categoryCode`: A unique code representing the category.
  - `isActive`: Boolean flag indicating if the category is active or not.
  - `sortOrder`: An integer value used to sort categories.

This DTO can be easily used in various scenarios, such as transferring data between the service layer and the UI, or mapping database records.