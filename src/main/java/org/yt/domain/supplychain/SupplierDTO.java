package com.example.domain.supplychain.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Data Transfer Object (DTO) for Supplier information.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class SupplierDTO {

    private Long id;
    private String name;
    private String contactPerson;
    private String phone;
    private String email;
    private String address;
    private String website;
    private String notes;

    // Optional: You can add validation annotations here if needed.
}

This `SupplierDTO` class is a simple, clean, and production-ready Data Transfer Object (DTO) designed to handle supplier information. It uses Lombok annotations for concise constructor injection, builder pattern, getter/setter generation, and field initialization.