package com.example.domain.user.security;

import javax.persistence.*;
import java.time.Instant;
import java.util.UUID;

/**
 * Entity representing a user session.
 */
@Entity(name = "user_sessions")
public class UserSessionEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private UUID sessionId;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    private UserEntity user;

    @Column(nullable = false)
    private Instant startTime;

    @Column
    private Instant endTime;

    public UserSessionEntity() {
        this.sessionId = UUID.randomUUID();
    }

    public UserSessionEntity(UserEntity user, Instant startTime) {
        this.user = user;
        this.sessionId = UUID.randomUUID();
        this.startTime = startTime;
    }

    // Getters and Setters

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public UUID getSessionId() {
        return sessionId;
    }

    public void setSessionId(UUID sessionId) {
        this.sessionId = sessionId;
    }

    public UserEntity getUser() {
        return user;
    }

    public void setUser(UserEntity user) {
        this.user = user;
    }

    public Instant getStartTime() {
        return startTime;
    }

    public void setStartTime(Instant startTime) {
        this.startTime = startTime;
    }

    public Instant getEndTime() {
        return endTime;
    }

    public void setEndTime(Instant endTime) {
        this.endTime = endTime;
    }
}

This code defines the `UserSessionEntity` class, which is a JPA entity representing user sessions. It includes fields for the session ID, associated user, start time, and end time of the session. The `UUID` is used to uniquely identify each session. The constructor initializes the `sessionId` with a randomly generated UUID.

The getters and setters are provided for easy access and modification of these fields.