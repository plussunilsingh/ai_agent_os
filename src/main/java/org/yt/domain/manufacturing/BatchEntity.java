package com.example.domain.manufacturing;

import javax.persistence.*;
import java.util.Date;
import java.util.List;

/**
 * JPA Entity representing a batch of manufactured products.
 */
@Entity
@Table(name = "BATCHES")
public class BatchEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, length = 50)
    private String batchNumber;

    @Column(nullable = false)
    private Date startDate;

    @Column(nullable = false)
    private Date endDate;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "PRODUCT_ID", nullable = false)
    private ProductEntity product;

    @OneToMany(mappedBy = "batch", cascade = {CascadeType.PERSIST, CascadeType.MERGE}, fetch = FetchType.LAZY)
    private List<LotEntryEntity> lotEntries;

    // Constructors
    public BatchEntity() {
    }

    public BatchEntity(String batchNumber, Date startDate, Date endDate) {
        this.batchNumber = batchNumber;
        this.startDate = startDate;
        this.endDate = endDate;
    }

    // Getters and Setters
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getBatchNumber() {
        return batchNumber;
    }

    public void setBatchNumber(String batchNumber) {
        this.batchNumber = batchNumber;
    }

    public Date getStartDate() {
        return startDate;
    }

    public void setStartDate(Date startDate) {
        this.startDate = startDate;
    }

    public Date getEndDate() {
        return endDate;
    }

    public void setEndDate(Date endDate) {
        this.endDate = endDate;
    }

    public ProductEntity getProduct() {
        return product;
    }

    public void setProduct(ProductEntity product) {
        this.product = product;
    }

    public List<LotEntryEntity> getLotEntries() {
        return lotEntries;
    }

    public void setLotEntries(List<LotEntryEntity> lotEntries) {
        this.lotEntries = lotEntries;
    }
}

This code defines a `BatchEntity` class that represents a batch of manufactured products in the domain. It includes necessary JPA annotations, constructors, and getters/setters for proper database interaction. The entity is optimized for performance with lazy loading strategies where applicable.