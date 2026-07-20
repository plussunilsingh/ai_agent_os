package com.example.warehouse.domain.stock;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.Table;
import java.io.Serializable;

@Entity
@Table(name = "ZONE")
public class ZoneEntity implements Serializable {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "ZONE_NAME", nullable = false, unique = true)
    private String zoneName;

    @Column(name = "DESCRIPTION", length = 255)
    private String description;

    public ZoneEntity() {
        // Default constructor for JPA
    }

    public ZoneEntity(String zoneName) {
        this.zoneName = zoneName;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getZoneName() {
        return zoneName;
    }

    public void setZoneName(String zoneName) {
        this.zoneName = zoneName;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }
}

### Explanation:
- **Package Declaration**: The package declaration is included to organize the classes.
- **Entity Annotation**: `@Entity` marks the class as a JPA entity.
- **Table Annotation**: `@Table(name = "ZONE")` specifies the table name in the database.
- **Id and GeneratedValue Annotations**: `@Id` and `@GeneratedValue(strategy = GenerationType.IDENTITY)` are used to define the primary key of the entity, with an auto-generated strategy for ID generation.
- **Column Annotations**: These annotations map the fields to the corresponding columns in the database. The `@Column` annotation is used to specify column names, nullability, and length constraints.

This code provides a clean and production-ready implementation of the `ZoneEntity` class.