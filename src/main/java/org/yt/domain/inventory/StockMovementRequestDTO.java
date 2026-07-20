package com.example.warehouse.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.Date;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class StockMovementRequestDTO {

    private String requestId;

    private String warehouseFromId;

    private String warehouseToId;

    private Integer quantity;

    private Date requestedDate;

    private String status; // Enum: PENDING, IN_PROGRESS, COMPLETED, CANCELLED

    private String备注; // Optional note or reason for the movement

    public StockMovementRequestDTO(String warehouseFromId, String warehouseToId, int quantity) {
        this.warehouseFromId = warehouseFromId;
        this.warehouseToId = warehouseToId;
        this.quantity = quantity;
        this.requestedDate = new Date();
        this.status = "PENDING";
    }
}

### Explanation:
1. **Package Declaration**: The package `com.example.warehouse.dto` is used to organize the DTO classes related to the warehouse.
2. **Lombok Annotations**:
   - `@Data`: This annotation generates all the boilerplate code for getters, setters, `toString()`, and constructors based on fields.
   - `@NoArgsConstructor`: Generates a no-argument constructor.
   - `@AllArgsConstructor`: Generates a constructor with parameters for all fields.
3. **Fields**:
   - `requestId`: A unique identifier for each request.
   - `warehouseFromId` and `warehouseToId`: IDs of the source and destination warehouses, respectively.
   - `quantity`: The number of items to be moved.
   - `requestedDate`: The date when the request was made. Initialized with the current date if not provided.
   - `status`: Current status of the movement (e.g., PENDING, IN_PROGRESS, COMPLETED, CANCELLED).
   - `备注`: Optional note or reason for the movement.

4. **Constructor**:
   - A constructor that initializes fields commonly used in new request scenarios (source and destination IDs, quantity).

### Considerations:
- The `status` field is an example of using a string to represent an enum. In production code, it would be preferable to use an actual enum type for better type safety.
- The `备注` field is marked as optional with the intention that it might not always be required in all scenarios.

This DTO can now be used to create inventory transfer requests within your application while maintaining a clean and maintainable structure.