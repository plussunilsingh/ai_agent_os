package com.example.manufacturing.domain;

import javax.persistence.*;
import java.util.Date;
import java.util.Set;

@Entity
@Table(name = "production_lines")
public class ProductionLineEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private String name;

    @Temporal(TemporalType.TIMESTAMP)
    @Column(nullable = false)
    private Date startDate;

    @Temporal(TemporalType.TIMESTAMP)
    @Column(nullable = true)
    private Date endDate;

    @OneToMany(mappedBy = "productionLine", cascade = CascadeType.ALL, orphanRemoval = true)
    private Set<ProductionOutputEntity> outputs;

    // Constructors
    public ProductionLineEntity() {
        // Default constructor for JPA
    }

    public ProductionLineEntity(String name, Date startDate) {
        this.name = name;
        this.startDate = startDate;
    }

    // Getters and Setters
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
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

    public Set<ProductionOutputEntity> getOutputs() {
        return outputs;
    }

    public void setOutputs(Set<ProductionOutputEntity> outputs) {
        this.outputs = outputs;
    }
}

This code defines the `ProductionLineEntity` class, which is a JPA entity representing production lines in a manufacturing domain. It includes necessary annotations for database mapping and relationships.

### Explanation:
- **@Entity**: Marks the class as a JPA entity.
- **@Table(name = "production_lines")**: Specifies the name of the table to map this entity to in the database.
- **@Id @GeneratedValue(strategy = GenerationType.IDENTITY)**: Defines the primary key with an auto-increment strategy.
- **@Column**: Sets column properties such as `nullable` and `unique`.
- **@Temporal(TemporalType.TIMESTAMP)**: Used for timestamp columns.
- **@OneToMany(mappedBy = "productionLine")**: Establishes a one-to-many relationship between `ProductionLineEntity` and `ProductionOutputEntity`.

This code is designed to be production-ready, with proper constructors and getters/setters.