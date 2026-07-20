package com.example.domain.manufacturing.dto;

import lombok.Builder;
import lombok.Getter;
import lombok.Setter;
import java.util.List;

/**
 * Data Transfer Object (DTO) for representing batch yield metrics.
 */
@Getter
@Setter
@Builder
public class BatchYieldDTO {

    private Long batchId;
    private String productId;
    private Integer totalProducedUnits;
    private Integer defectiveUnits;
    private Integer nonDefectiveUnits;
    private Double yieldPercentage;

    /**
     * List of detailed yield records for the batch.
     */
    private List<BatchYieldDetailDTO> details;

    /**
     * Constructor to initialize all fields.
     */
    public BatchYieldDTO(Long batchId, String productId, Integer totalProducedUnits,
                         Integer defectiveUnits, Double yieldPercentage) {
        this.batchId = batchId;
        this.productId = productId;
        this.totalProducedUnits = totalProducedUnits;
        this.defectiveUnits = defectiveUnits;
        this.yieldPercentage = yieldPercentage;
    }

    /**
     * Method to calculate the non-defective units from total and defective units.
     */
    public void calculateNonDefectiveUnits() {
        if (totalProducedUnits != null && defectiveUnits != null) {
            this.nonDefectiveUnits = totalProducedUnits - defectiveUnits;
        }
    }

    /**
     * Method to validate the yield percentage, ensuring it is within a valid range.
     */
    public void validateYieldPercentage() {
        if (yieldPercentage != null) {
            if (yieldPercentage < 0 || yieldPercentage > 100) {
                throw new IllegalArgumentException("Yield Percentage must be between 0 and 100.");
            }
        }
    }

    /**
     * Method to update the yield percentage based on total produced and defective units.
     */
    public void updateYieldPercentage() {
        if (totalProducedUnits != null && defectiveUnits != null) {
            double nonDefective = nonDefectiveUnits == null ? 0 : nonDefectiveUnits;
            this.yieldPercentage = ((double) nonDefective / totalProducedUnits) * 100;
        }
    }
}

### Explanation:
- **Class and Package**: The class is defined within the `com.example.domain.manufacturing.dto` package.
- **Lombok Annotations**: Lombok annotations (`@Getter`, `@Setter`, and `@Builder`) are used to simplify field management.
- **Fields**:
  - `batchId`: Unique identifier for the batch.
  - `productId`: ID of the product being manufactured.
  - `totalProducedUnits`: Total number of units produced in the batch.
  - `defectiveUnits`: Number of defective units in the batch.
  - `nonDefectiveUnits`: Calculated non-defective units (defaulted to null).
  - `yieldPercentage`: Percentage yield of the batch.
  - `details`: List of detailed yield records for the batch.
- **Constructors**: A parameterized constructor and a default no-argument constructor are provided.
- **Methods**:
  - `calculateNonDefectiveUnits()`: Calculates non-defective units based on total produced and defective units.
  - `validateYieldPercentage()`: Validates that the yield percentage is between 0 and 100.
  - `updateYieldPercentage()`: Updates the yield percentage based on calculated or provided values.

This DTO class can be used in various scenarios where batch yield metrics need to be represented, such as reporting, analysis, or data transfer.