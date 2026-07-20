package com.example.domain.supplychain.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Data Transfer Object (DTO) representing an inspection result for Quality Assurance reports.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class InspectionResultDTO {

    private Long id;
    
    private String inspectionDate;
    
    private String inspectionTime;
    
    private String inspectionLocation;
    
    private String materialId;
    
    private String productId;
    
    private String inspectionType;
    
    private double defectRate;
    
    private boolean isPassing;

    // Additional fields can be added as needed
}

### Explanation:
- **Lombok Annotations**:
  - `@Data`: Generates the constructor, getters, and setters.
  - `@Builder`: Provides a builder pattern to construct objects with less boilerplate code.
  - `@NoArgsConstructor` and `@AllArgsConstructor`: Generate no-argument and all-arguments constructors.

### Usage Example:
This DTO can be used when transferring inspection results between layers in your application. For example, it might be used in API responses or for storing intermediate data before persisting to the database.

// Example of using InspectionResultDTO
InspectionResultDTO result = InspectionResultDTO.builder()
    .id(1L)
    .inspectionDate("2023-10-01")
    .inspectionTime("14:30:00")
    .inspectionLocation("Factory A")
    .materialId("M123456789")
    .productId("P987654321")
    .inspectionType("Visual Inspection")
    .defectRate(0.02)
    .isPassing(true)
    .build();

// Output: {id=1, inspectionDate=2023-10-01, inspectionTime=14:30:00, inspectionLocation=Factory A, materialId=M123456789, productId=P987654321, inspectionType=Visual Inspection, defectRate=0.02, isPassing=true}

This code snippet provides a clean and efficient way to handle inspection results in your application, ensuring that the DTO is well-structured for both internal use and API responses.