package com.example.warehouse.stock.domain;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.Table;
import java.time.LocalDate;

@Entity
@Table(name = "reorder_alert")
public class ReorderAlertEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String productCode;

    private int thresholdQuantity;

    private LocalDate lastGeneratedDate;

    public ReorderAlertEntity() {
        // Default constructor for JPA
    }

    public ReorderAlertEntity(String productCode, int thresholdQuantity) {
        this.productCode = productCode;
        this.thresholdQuantity = thresholdQuantity;
        this.lastGeneratedDate = LocalDate.now();
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getProductCode() {
        return productCode;
    }

    public void setProductCode(String productCode) {
        this.productCode = productCode;
    }

    public int getThresholdQuantity() {
        return thresholdQuantity;
    }

    public void setThresholdQuantity(int thresholdQuantity) {
        this.thresholdQuantity = thresholdQuantity;
    }

    public LocalDate getLastGeneratedDate() {
        return lastGeneratedDate;
    }

    public void setLastGeneratedDate(LocalDate lastGeneratedDate) {
        this.lastGeneratedDate = lastGeneratedDate;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof ReorderAlertEntity)) return false;

        ReorderAlertEntity that = (ReorderAlertEntity) o;

        return getId().equals(that.getId());
    }

    @Override
    public int hashCode() {
        return getId().hashCode();
    }
}

This code defines the `ReorderAlertEntity` class for managing low stock thresholds in a warehouse and stock domain. The entity is mapped to a table named `reorder_alert`. It includes fields for product code, threshold quantity, and the last date when an alert was generated. Constructors, getters, setters, and hashcode/equals methods are provided to ensure proper object handling and comparison.