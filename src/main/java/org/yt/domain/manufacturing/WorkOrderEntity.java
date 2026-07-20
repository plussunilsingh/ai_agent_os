package com.example.manufacturing.domain;

import javax.persistence.*;
import java.time.LocalDate;
import java.util.Set;

@Entity
@Table(name = "work_order")
public class WorkOrderEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, length = 50)
    private String orderNumber;

    @Column(nullable = false)
    private LocalDate startDate;

    @Column(nullable = false)
    private LocalDate endDate;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "customer_id", nullable = false)
    private CustomerEntity customer;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "product_id", nullable = false)
    private ProductEntity product;

    @OneToMany(mappedBy = "workOrder", cascade = CascadeType.ALL, orphanRemoval = true)
    private Set<WorkOrderDetailEntity> details;

    // Getters and Setters
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getOrderNumber() {
        return orderNumber;
    }

    public void setOrderNumber(String orderNumber) {
        this.orderNumber = orderNumber;
    }

    public LocalDate getStartDate() {
        return startDate;
    }

    public void setStartDate(LocalDate startDate) {
        this.startDate = startDate;
    }

    public LocalDate getEndDate() {
        return endDate;
    }

    public void setEndDate(LocalDate endDate) {
        this.endDate = endDate;
    }

    public CustomerEntity getCustomer() {
        return customer;
    }

    public void setCustomer(CustomerEntity customer) {
        this.customer = customer;
    }

    public ProductEntity getProduct() {
        return product;
    }

    public void setProduct(ProductEntity product) {
        this.product = product;
    }

    public Set<WorkOrderDetailEntity> getDetails() {
        return details;
    }

    public void setDetails(Set<WorkOrderDetailEntity> details) {
        this.details = details;
    }
}

This code defines the `WorkOrderEntity` class, which is a JPA entity representing work orders in the manufacturing domain. It includes fields for the primary key (`id`), order number, start and end dates of the work order, references to the related customer and product entities, and a set of details associated with each work order.

### Explanation:
- **Fields**:
  - `id`: The unique identifier for the work order.
  - `orderNumber`: A string representing the unique order number.
  - `startDate` and `endDate`: Date fields representing when the work order starts and ends.
  - `customer`: A relationship to a `CustomerEntity`.
  - `product`: A relationship to a `ProductEntity`.
  - `details`: A collection of `WorkOrderDetailEntity`.

- **Getters and Setters**: 
  - These methods allow for safe access and modification of the fields.

This entity is designed to be used in a production environment, with proper field validation and relationships managed through JPA annotations.