package com.example.domain.manufacturing;

import javax.persistence.*;
import java.time.LocalDateTime;
import java.util.List;

@Entity
@Table(name = "YIELD_METRIC")
public class YieldMetricEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private LocalDateTime timestamp;

    @Column(nullable = false)
    private double efficiency;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "LINE_ID", nullable = false)
    private ProductionLineEntity productionLine;

    @OneToMany(mappedBy = "yieldMetric", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<YieldDetailEntity> details;

    // Constructors
    public YieldMetricEntity() {
        // Default constructor for JPA
    }

    public YieldMetricEntity(LocalDateTime timestamp, double efficiency, ProductionLineEntity productionLine) {
        this.timestamp = timestamp;
        this.efficiency = efficiency;
        this.productionLine = productionLine;
    }

    // Getters and Setters

    @Override
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public LocalDateTime getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(LocalDateTime timestamp) {
        this.timestamp = timestamp;
    }

    public double getEfficiency() {
        return efficiency;
    }

    public void setEfficiency(double efficiency) {
        this.efficiency = efficiency;
    }

    public ProductionLineEntity getProductionLine() {
        return productionLine;
    }

    public void setProductionLine(ProductionLineEntity productionLine) {
        this.productionLine = productionLine;
    }

    public List<YieldDetailEntity> getDetails() {
        return details;
    }

    public void setDetails(List<YieldDetailEntity> details) {
        this.details = details;
    }
}

This code defines the `YieldMetricEntity` class as a JPA entity for tracking efficiency metrics in a manufacturing context. The class includes:

- A unique identifier (`id`) to uniquely identify each record.
- Fields for timestamp and efficiency, which are crucial for monitoring production line performance.
- A `ProductionLineEntity` relationship to link the metric with the relevant production line.
- A list of `YieldDetailEntity` objects that can store additional details related to specific yield metrics.

The constructors ensure proper initialization, while getters and setters provide access to the fields. The `@Id` and `@GeneratedValue` annotations are used to define the primary key and its generation strategy, respectively. The `@ManyToOne` annotation establishes a one-to-many relationship with `ProductionLineEntity`, and the `@OneToMany` annotation defines a many-to-one relationship with `YieldDetailEntity`.