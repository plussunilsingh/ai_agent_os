package com.example.domain.orderfulfillment.entities;

import jakarta.persistence.*;
import java.util.Date;
import java.util.HashSet;
import java.util.Set;

/**
 * Entity representing a customer profile.
 */
@Entity
@Table(name = "CUSTOMER")
public class CustomerEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private String customerId;

    @Column(nullable = false)
    private String firstName;

    @Column(nullable = false)
    private String lastName;

    @Column(unique = true)
    private String email;

    @Temporal(TemporalType.TIMESTAMP)
    private Date createdAt;

    @Temporal(TemporalType.TIMESTAMP)
    private Date updatedAt;

    // Relationships
    @OneToMany(mappedBy = "customer", cascade = CascadeType.ALL, orphanRemoval = true)
    private Set<OrderEntity> orders = new HashSet<>();

    public CustomerEntity() {
        // Default constructor required by JPA
    }

    public CustomerEntity(String customerId, String firstName, String lastName, String email) {
        this.customerId = customerId;
        this.firstName = firstName;
        this.lastName = lastName;
        this.email = email;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getCustomerId() {
        return customerId;
    }

    public void setCustomerId(String customerId) {
        this.customerId = customerId;
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

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public Date getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(Date createdAt) {
        this.createdAt = createdAt;
    }

    public Date getUpdatedAt() {
        return updatedAt;
    }

    public void setUpdatedAt(Date updatedAt) {
        this.updatedAt = updatedAt;
    }

    public Set<OrderEntity> getOrders() {
        return orders;
    }

    public void setOrders(Set<OrderEntity> orders) {
        this.orders = orders;
    }

    @Override
    public String toString() {
        return "CustomerEntity{" +
                "id=" + id +
                ", customerId='" + customerId + '\'' +
                ", firstName='" + firstName + '\'' +
                ", lastName='" + lastName + '\'' +
                ", email='" + email + '\'' +
                '}';
    }
}

### Explanation:
- **Annotations**:
  - `@Entity`: Marks the class as a JPA entity.
  - `@Table(name = "CUSTOMER")`: Specifies the table name in the database.
  - `@Id` and `@GeneratedValue(strategy = GenerationType.IDENTITY)`: Defines the primary key of the entity and sets the auto-increment strategy.
  - `@Column(nullable = false, unique = true)` or `@Column(unique = true)`: Ensures that certain fields are not null and/or unique in the database.

- **Fields**:
  - `id`: The primary key for the customer.
  - `customerId`, `firstName`, `lastName`, `email`: Customer profile attributes.
  - `createdAt` and `updatedAt`: Timestamps to track when the record was created or last updated.

- **Relationships**:
  - `orders`: A set of orders associated with a customer. Use `cascade = CascadeType.ALL, orphanRemoval = true` for proper handling of child entities.

### Notes:
- Ensure that your database schema matches the entity definitions.
- Consider adding validation annotations (e.g., from Hibernate Validator) if necessary.
- For performance and query optimization, ensure indexes are set on fields used in queries frequently.