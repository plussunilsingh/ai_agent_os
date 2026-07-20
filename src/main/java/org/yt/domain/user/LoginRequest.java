package com.example.domain.user.security.dto;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;
import java.util.Objects;

public class LoginRequest {

    @NotNull(message = "Email is required")
    @Email(message = "Invalid email format")
    private String email;

    @NotBlank(message = "Password is required")
    @Size(min = 8, max = 20, message = "Password must be between 8 and 20 characters long")
    @Pattern(regexp = "(?=.*[0-9])(?=.*[a-zA-Z]).{8,}", message = "Password must contain at least one number and one letter")
    private String password;

    public LoginRequest() {
        // No-arg constructor for JPA
    }

    public LoginRequest(String email, String password) {
        this.email = email;
        this.password = password;
    }

    @NotBlank(message = "Email is required")
    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    @NotBlank(message = "Password is required")
    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        LoginRequest that = (LoginRequest) o;
        return Objects.equals(email, that.email) &&
                Objects.equals(password, that.password);
    }

    @Override
    public int hashCode() {
        return Objects.hash(email, password);
    }
}

This `LoginRequest` DTO class includes Jakarta validation annotations to ensure the email and password fields are validated according to specific rules. The `equals` and `hashCode` methods are overridden for proper object comparison.