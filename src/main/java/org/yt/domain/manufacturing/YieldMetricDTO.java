package com.example.domain.manufacturing.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * DTO class for representing yield metrics.
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class YieldMetricDTO {

    private Long id;
    private String processName;
    private String batchId;
    private int totalUnitsProduced;
    private int unitsRejected;
    private double yieldPercentage;

    public YieldMetricDTO(String processName, String batchId, int totalUnitsProduced, int unitsRejected) {
        this.processName = processName;
        this.batchId = batchId;
        this.totalUnitsProduced = totalUnitsProduced;
        this.unitsRejected = unitsRejected;
        this.yieldPercentage = calculateYieldPercentage(totalUnitsProduced, unitsRejected);
    }

    private double calculateYieldPercentage(int totalUnitsProduced, int unitsRejected) {
        if (totalUnitsProduced == 0) return 0.0;
        return ((double) (totalUnitsProduced - unitsRejected) / totalUnitsProduced) * 100;
    }
}

### Explanation:
- **Annotations**:
  - `@Data`: Auto-generates getters, setters, equals, hashCode, and toString.
  - `@NoArgsConstructor` and `@AllArgsConstructor`: Provide no-argument and all-args constructors respectively.
  - `@Builder`: Provides a builder pattern for constructing instances of the class.

- **Fields**:
  - `id`, `processName`, `batchId`: Basic identifiers for the metric.
  - `totalUnitsProduced`: Total units produced in the batch.
  - `unitsRejected`: Number of rejected units in the batch.
  - `yieldPercentage`: Calculated yield percentage based on total and rejected units.

- **Constructor**:
  - A parameterized constructor is provided to initialize the object directly with basic metrics, which then calculates the yield percentage using a helper method.

This code is designed for high performance and maintainability, ensuring that it can be integrated seamlessly into larger applications.