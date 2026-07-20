package com.example.domain.supplychain.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Data Transfer Object (DTO) for Dock Scheduling.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ReceivingDockDTO {

    private String dockId; // Unique identifier of the dock

    private String location; // Physical location of the dock

    private Boolean isAvailable; // Indicates if the dock is currently available for scheduling

    private Integer expectedArrivalTime; // Expected time when a shipment is scheduled to arrive at the dock

    private Integer actualArrivalTime; // Actual time when a shipment arrived at the dock (nullable)

    private String vesselName; // Name of the vessel that will be docking

    private String cargoType; // Type of cargo being handled

    private Integer estimatedCargoQuantity; // Estimated quantity of cargo to be loaded/unloaded

    private Boolean isPriorityDock; // Indicates if the dock is a priority dock for scheduling
}

This `ReceivingDockDTO` class uses Lombok annotations to simplify the boilerplate code, ensuring that you have getters and setters, constructors, and builder pattern support. This DTO can be used in various scenarios where information about a receiving dock needs to be transferred between layers of your application or during API exchanges.