package com.example.domain.user.security;

import javax.persistence.*;
import java.time.Instant;
import java.util.UUID;

@Entity
@Table(name = "password_reset_tokens")
public class PasswordResetEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private String token;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    private UserEntity user;

    @Column(nullable = false)
    private Instant createdDate;

    @Column(nullable = false)
    private Instant expiryDate;

    public PasswordResetEntity() {
        this.token = UUID.randomUUID().toString();
        this.createdDate = Instant.now();
        this.expiryDate = this.createdDate.plusMinutes(15); // Expiry in 15 minutes
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getToken() {
        return token;
    }

    public void setToken(String token) {
        this.token = token;
    }

    public UserEntity getUser() {
        return user;
    }

    public void setUser(UserEntity user) {
        this.user = user;
    }

    public Instant getCreatedDate() {
        return createdDate;
    }

    public void setCreatedDate(Instant createdDate) {
        this.createdDate = createdDate;
    }

    public Instant getExpiryDate() {
        return expiryDate;
    }

    public void setExpiryDate(Instant expiryDate) {
        this.expiryDate = expiryDate;
    }
}

This code defines the `PasswordResetEntity` JPA entity, which is mapped to a database table named `password_reset_tokens`. The entity includes fields for a unique token, the associated user, and dates for creation and expiry. The constructor initializes the token with a UUID and sets the created date and expiry date.

Make sure that the `UserEntity` class is defined elsewhere in your project structure, as it is referenced here. This class should be part of the User & Security domain to ensure proper encapsulation and data integrity.