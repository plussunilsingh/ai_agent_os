package com.example.domain.supplychain.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.PositiveOrZero;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class MaterialRequestDTO {

    private Long id;

    @NotBlank(message = "Material name cannot be blank")
    private String materialName;

    @NotNull(message = "Quantity must not be null")
    @PositiveOrZero(message = "Quantity must be a positive or zero value")
    private int quantity;

    @NotNull(message = "Supplier ID must not be null")
    private Long supplierId;

    @NotBlank(message = "Description cannot be blank")
    private String description;

    public MaterialRequestDTO(Long id, String materialName, int quantity, Long supplierId, String description) {
        this.id = id;
        this.materialName = materialName;
        this.quantity = quantity;
        this.supplierId = supplierId;
        this.description = description;
    }
}

This `MaterialRequestDTO` class includes:

1. **Fields**: `id`, `materialName`, `quantity`, `supplierId`, and `description`.
2. **Validation**:
   - `@NotBlank` for non-blank constraints.
   - `@NotNull` for ensuring values are not null.
   - `@PositiveOrZero` to ensure the quantity is a positive or zero value.
3. **Builder Pattern**: Using Lombok's `@Builder` to simplify object creation.
4. **Default Constructors**: Provided by Lombok's `@NoArgsConstructor` and `@AllArgsConstructor`.
5. **Custom Constructor**: For creating objects with specific fields.

This DTO can be used in the supply chain domain for handling material requests, ensuring all necessary validations are met before processing any request.