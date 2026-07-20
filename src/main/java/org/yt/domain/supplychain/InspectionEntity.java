package com.example.supplychain.domain.inspection;

import javax.persistence.*;
import java.util.Date;
import java.util.Set;

@Entity
@Table(name = "inspection")
public class InspectionEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, length = 50)
    private String inspectionNumber;

    @Column(nullable = false)
    private Date inspectionDate;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "supplier_id", nullable = false)
    private SupplierEntity supplier;

    @ManyToMany(mappedBy = "inspections")
    private Set<ProductBatchEntity> productBatches;

    @OneToMany(mappedBy = "inspection", cascade = CascadeType.ALL, orphanRemoval = true)
    private Set<InspectionResultEntity> results;

    public InspectionEntity() {
    }

    public InspectionEntity(String inspectionNumber, Date inspectionDate, SupplierEntity supplier) {
        this.inspectionNumber = inspectionNumber;
        this.inspectionDate = inspectionDate;
        this.supplier = supplier;
    }

    // Getters and Setters

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getInspectionNumber() {
        return inspectionNumber;
    }

    public void setInspectionNumber(String inspectionNumber) {
        this.inspectionNumber = inspectionNumber;
    }

    public Date getInspectionDate() {
        return inspectionDate;
    }

    public void setInspectionDate(Date inspectionDate) {
        this.inspectionDate = inspectionDate;
    }

    public SupplierEntity getSupplier() {
        return supplier;
    }

    public void setSupplier(SupplierEntity supplier) {
        this.supplier = supplier;
    }

    public Set<ProductBatchEntity> getProductBatches() {
        return productBatches;
    }

    public void setProductBatches(Set<ProductBatchEntity> productBatches) {
        this.productBatches = productBatches;
    }

    public Set<InspectionResultEntity> getResults() {
        return results;
    }

    public void setResults(Set<InspectionResultEntity> results) {
        this.results = results;
    }
}

This code defines the `InspectionEntity` class, which represents a quality assurance inspection in your supply chain domain. The entity is mapped to a database table named `inspection`. It includes fields for the inspection number, date, supplier, and related product batches and inspection results. Proper JPA annotations are used to ensure correct database interaction.

The constructor and getters/setters provide a clean interface for interacting with this entity in your application logic.