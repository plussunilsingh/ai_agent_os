package com.example.domain.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * UserResponseDTO is a Data Transfer Object used to transfer user information from the backend to the frontend.
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class UserResponseDTO {

    private Long id;
    private String username;
    private String email;
    private String firstName;
    private String lastName;
    private boolean active;

    // Optional: Add any additional fields you might need, such as roles or last login details.
}

This `UserResponseDTO` class uses Lombok to simplify the boilerplate code for getters and setters. It is designed to be a lightweight object used in API responses. The properties include basic user information that would typically be sent back to the client. You can add more fields as needed, depending on your specific requirements.