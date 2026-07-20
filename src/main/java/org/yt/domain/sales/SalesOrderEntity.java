package com.example.domain.order;

import javax.persistence.*;
import java.util.Date;
import java.util.List;

@Entity
@Table(name = "sales_orders")
public class SalesOrderEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, length = 255)
    private String orderId;

    @Column(nullable = false)
    private Date orderDate;

    @Column(nullable = false)
    private Double totalAmount;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "customer_id", nullable = false)
    private CustomerEntity customer;

    @OneToMany(mappedBy = "salesOrder", fetch = FetchType.EAGER, cascade = CascadeType.ALL, orphanRemoval = true)
    private List<SalesOrderItemEntity> items;

    @Column(nullable = false)
    private String status; // e.g., "NEW", "SHIPPED", "DELIVERED"

    public SalesOrderEntity() {
    }

    public SalesOrderEntity(String orderId, Date orderDate, Double totalAmount, CustomerEntity customer) {
        this.orderId = orderId;
        this.orderDate = orderDate;
        this.totalAmount = totalAmount;
        this.customer = customer;
    }

    // Getters and Setters
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getOrderId() {
        return orderId;
    }

    public void setOrderId(String orderId) {
        this.orderId = orderId;
    }

    public Date getOrderDate() {
        return orderDate;
    }

    public void setOrderDate(Date orderDate) {
        this.orderDate = orderDate;
    }

    public Double getTotalAmount() {
        return totalAmount;
    }

    public void setTotalAmount(Double totalAmount) {
        this.totalAmount = totalAmount;
    }

    public CustomerEntity getCustomer() {
        return customer;
    }

    public void setCustomer(CustomerEntity customer) {
        this.customer = customer;
    }

    public List<SalesOrderItemEntity> getItems() {
        return items;
    }

    public void setItems(List<SalesOrderItemEntity> items) {
        this.items = items;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }
}

### Explanation:
1. **Entity Annotation**: The `@Entity` annotation marks the class as a JPA entity.
2. **Table Mapping**: The `@Table` annotation maps the entity to a table named "sales_orders".
3. **Id Generation**: The `@Id` and `@GeneratedValue(strategy = GenerationType.IDENTITY)` annotations define the primary key for the entity.
4. **Columns**:
   - `orderId`: A unique identifier for each order.
   - `orderDate`: Date when the order was placed.
   - `totalAmount`: Total amount of the order.
   - `customer`: Reference to the customer who placed the order.
   - `status`: Current status of the order (e.g., NEW, SHIPPED, DELIVERED).
5. **Relationships**:
   - `@ManyToOne` and `@JoinColumn`: Establish a one-to-many relationship with `CustomerEntity`.
   - `@OneToMany` and `orphanRemoval = true`: Defines a many-to-one relationship with `SalesOrderItemEntity`, ensuring that orphaned items are removed when the parent order is deleted.
6. **Fetch Type**: The `fetch = FetchType.LAZY` ensures that the customer entity is loaded lazily, improving performance.
7. **Constructors and Getters/Setters**: Standard JavaBean constructors and accessors for easy object manipulation.

This code can be used as a foundation in a larger application to manage sales orders efficiently.