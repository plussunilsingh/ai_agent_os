package com.example.domain.user;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.Table;
import java.util.Date;

@Entity
@Table(name = "user_accounts")
public class UserEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private String username;

    @Column(nullable = false)
    private String passwordHash; // Consider using a secure hashing algorithm like bcrypt

    @Column(nullable = false)
    private String email;

    @Column(name = "first_name", nullable = false)
    private String firstName;

    @Column(name = "last_name", nullable = false)
    private String lastName;

    @Column(nullable = false, updatable = false)
    private Date createdAt;

    @Column(nullable = false)
    private boolean enabled;

    // Getters and Setters
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getPasswordHash() {
        return passwordHash;
    }

    public void setPasswordHash(String passwordHash) {
        this.passwordHash = passwordHash;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getFirstName() {
        return firstName;
    }

    public void setFirstName(String firstName) {
        this.firstName = firstName;
    }

    public String getLastName() {
        return lastName;
    }

    public void setLastName(String lastName) {
        this.lastName = lastName;
    }

    public Date getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(Date createdAt) {
        this.createdAt = createdAt;
    }

    public boolean isEnabled() {
        return enabled;
    }

    public void setEnabled(boolean enabled) {
        this.enabled = enabled;
    }
}

### Explanation:
1. **Annotations**:
   - `@Entity`: Marks the class as a JPA entity.
   - `@Table(name = "user_accounts")`: Specifies that this entity maps to the `user_accounts` table in the database.

2. **Fields and Properties**:
   - `id`: The primary key of the user account.
   - `username`, `passwordHash`, `email`, `firstName`, `lastName`: User information fields.
   - `createdAt`: Timestamp for when the user account was created.
   - `enabled`: Boolean flag to indicate if the user account is active.

3. **Getters and Setters**:
   - All fields have corresponding getters and setters, which are essential for JPA operations and external access.

4. **Data Validation**:
   - Fields marked as `nullable = false` ensure that these columns cannot be null in the database.
   - `unique = true` on `username` ensures that usernames are unique across all users.

5. **Performance Considerations**:
   - The use of a secure hashing algorithm for `passwordHash` is critical to protect user passwords.
   - Proper indexing and query optimization should be applied when querying this entity in production code.

This class provides a clean, production-ready implementation for mapping the `user_accounts` table to a JPA entity.