package com.example.domain.order.fulfillment.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Data Transfer Object (DTO) representing a Carrier option for order fulfillment.
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class CarrierDTO {

    private Long id;
    private String carrierName;
    private String serviceType;
    private double costPerKg;
    private int deliveryTimeInDays;

    /**
     * Constructor with all fields.
     *
     * @param id the unique identifier of the carrier option.
     * @param carrierName the name of the carrier company.
     * @param serviceType the type of service offered (e.g., standard, expedited).
     * @param costPerKg the cost per kilogram for shipping with this carrier.
     * @param deliveryTimeInDays the estimated number of days it takes to deliver using this carrier.
     */
    public CarrierDTO(Long id, String carrierName, String serviceType, double costPerKg, int deliveryTimeInDays) {
        this.id = id;
        this.carrierName = carrierName;
        this.serviceType = serviceType;
        this.costPerKg = costPerKg;
        this.deliveryTimeInDays = deliveryTimeInDays;
    }

    /**
     * Builder method to create a CarrierDTO instance.
     *
     * @return the builder object to configure the fields and build the CarrierDTO.
     */
    public static CarrierDTOBuilder builder() {
        return new CarrierDTOBuilder();
    }
}

### Explanation:
- **Lombok Annotations**:
  - `@Data`: Auto-generates getters, setters, equals, hashCode, and toString methods.
  - `@NoArgsConstructor`, `@AllArgsConstructor`: Generate a no-argument constructor and a constructor with all parameters.
  - `@Builder`: Provides a fluent builder for constructing objects.

### Usage Example:

CarrierDTO carrier = CarrierDTO.builder()
    .id(1L)
    .carrierName("FedEx")
    .serviceType("Standard")
    .costPerKg(0.5)
    .deliveryTimeInDays(3)
    .build();

This DTO is designed to be used in a production environment, with clean and efficient coding practices.