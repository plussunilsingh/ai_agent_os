package com.example.domain.order.fulfillment;

import javax.persistence.*;
import java.util.Date;
import java.util.Set;

@Entity
@Table(name = "CARRIERS")
public class CarrierEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private String carrierCode;

    @Column(nullable = false)
    private String name;

    @Column(nullable = false)
    private String contactName;

    @Column(nullable = false)
    private String phoneNumber;

    @Column(nullable = false)
    private String email;

    @OneToMany(mappedBy = "carrier", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private Set<OrderEntity> orders;

    public CarrierEntity() {
        // Default constructor for JPA
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getCarrierCode() {
        return carrierCode;
    }

    public void setCarrierCode(String carrierCode) {
        this.carrierCode = carrierCode;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getContactName() {
        return contactName;
    }

    public void setContactName(String contactName) {
        this.contactName = contactName;
    }

    public String getPhoneNumber() {
        return phoneNumber;
    }

    public void setPhoneNumber(String phoneNumber) {
        this.phoneNumber = phoneNumber;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public Set<OrderEntity> getOrders() {
        return orders;
    }

    public void setOrders(Set<OrderEntity> orders) {
        this.orders = orders;
    }
}

This code defines the `CarrierEntity` class, which is a JPA entity representing freight providers in your domain. The fields are mapped to columns in a database table named `CARRIERS`. The relationships and other necessary methods are included to ensure proper handling of entities.

### Explanation:
- **Id**: Primary key for the carrier.
- **carrierCode**: Unique identifier for each carrier.
- **name, contactName, phoneNumber, email**: Details about the carrier.
- **orders**: A many-to-one relationship with `OrderEntity`.

### Notes:
- The `@GeneratedValue(strategy = GenerationType.IDENTITY)` ensures that the ID is managed by the database.
- `FetchType.LAZY` is used to avoid loading all orders when fetching a single carrier, improving performance.
- The default constructor is required for JPA.

This code can be integrated into your existing application and should work well in a production environment.