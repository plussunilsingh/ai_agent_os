package com.example.domain.order.fulfillment;

import jakarta.persistence.*;
import java.util.Date;
import java.util.Set;

@Entity
@Table(name = "SHIPMENT")
public class ShipmentEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, length = 255)
    private String shipmentReferenceNumber;

    @Column(nullable = false)
    private Date shipmentDate;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "ORDER_ID", nullable = false)
    private OrderEntity order;

    @OneToMany(mappedBy = "shipment", cascade = CascadeType.ALL, orphanRemoval = true)
    private Set<ShipmentItemEntity> items;

    @Column(nullable = false, length = 255)
    private String trackingNumber;

    @Enumerated(EnumType.STRING)
    private ShipmentStatus status;

    // Constructors
    public ShipmentEntity() {}

    public ShipmentEntity(String shipmentReferenceNumber, Date shipmentDate, OrderEntity order,
                          Set<ShipmentItemEntity> items, String trackingNumber, ShipmentStatus status) {
        this.shipmentReferenceNumber = shipmentReferenceNumber;
        this.shipmentDate = shipmentDate;
        this.order = order;
        this.items = items;
        this.trackingNumber = trackingNumber;
        this.status = status;
    }

    // Getters and Setters
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getShipmentReferenceNumber() {
        return shipmentReferenceNumber;
    }

    public void setShipmentReferenceNumber(String shipmentReferenceNumber) {
        this.shipmentReferenceNumber = shipmentReferenceNumber;
    }

    public Date getShipmentDate() {
        return shipmentDate;
    }

    public void setShipmentDate(Date shipmentDate) {
        this.shipmentDate = shipmentDate;
    }

    public OrderEntity getOrder() {
        return order;
    }

    public void setOrder(OrderEntity order) {
        this.order = order;
    }

    public Set<ShipmentItemEntity> getItems() {
        return items;
    }

    public void setItems(Set<ShipmentItemEntity> items) {
        this.items = items;
    }

    public String getTrackingNumber() {
        return trackingNumber;
    }

    public void setTrackingNumber(String trackingNumber) {
        this.trackingNumber = trackingNumber;
    }

    public ShipmentStatus getStatus() {
        return status;
    }

    public void setStatus(ShipmentStatus status) {
        this.status = status;
    }
}

### Explanation:
- **Entity Annotations**: 
  - `@Entity` and `@Table(name = "SHIPMENT")`: Define the entity and its table name.
  - `@Id @GeneratedValue(strategy = GenerationType.IDENTITY)`: Define the primary key with auto-increment.
  - `@ManyToOne(fetch = FetchType.LAZY)` for order reference, which is a one-to-one relationship in terms of order fulfillment.
  - `@OneToMany(mappedBy = "shipment", cascade = CascadeType.ALL, orphanRemoval = true)`: Define a many-to-one relationship with `ShipmentItemEntity` and configure cascading operations.

- **Fields**:
  - `shipmentReferenceNumber`: Unique identifier for the shipment.
  - `shipmentDate`: Date when the shipment was created.
  - `order`: Reference to the associated order entity.
  - `items`: Set of items in this shipment, represented by `ShipmentItemEntity`.
  - `trackingNumber`: Tracking number for logistics tracking.
  - `status`: Enum representing the current status of the shipment.

- **Constructors**:
  - Default constructor and parameterized constructor.

- **Getters and Setters**: 
  - Provide access to fields while maintaining encapsulation.