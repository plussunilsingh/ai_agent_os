package com.example.domain.supplychain;

import javax.persistence.*;
import java.util.HashSet;
import java.util.Set;

@Entity
@Table(name = "material")
public class MaterialEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private String materialCode;

    @Column(nullable = false)
    private String name;

    @Column(nullable = false)
    private String description;

    @ManyToOne
    @JoinColumn(name = "supplier_id", nullable = false)
    private SupplierEntity supplier;

    @OneToMany(mappedBy = "material", cascade = CascadeType.ALL, orphanRemoval = true)
    private Set<BatchEntity> batches = new HashSet<>();

    public MaterialEntity() {
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getMaterialCode() {
        return materialCode;
    }

    public void setMaterialCode(String materialCode) {
        this.materialCode = materialCode;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public SupplierEntity getSupplier() {
        return supplier;
    }

    public void setSupplier(SupplierEntity supplier) {
        this.supplier = supplier;
    }

    public Set<BatchEntity> getBatches() {
        return batches;
    }

    public void setBatches(Set<BatchEntity> batches) {
        this.batches = batches;
    }
}

### Explanation:

1. **Package Declaration**: The package declaration (`com.example.domain.supplychain`) should match the project's structure.

2. **JPA Annotations**:
   - `@Entity`: Marks this class as a JPA entity.
   - `@Table(name = "material")`: Specifies that the entity is mapped to the database table named `material`.
   - `@Id` and `@GeneratedValue(strategy = GenerationType.IDENTITY)`: Specifies the primary key and its generation strategy.

3. **Fields**:
   - `id`: The unique identifier for each material.
   - `materialCode`: A unique code for the material, ensuring that no two materials have the same code.
   - `name`: The name of the material.
   - `description`: A brief description of the material.
   - `supplier`: A reference to the supplier entity. This is a many-to-one relationship as one material can be supplied by only one supplier at any given time, but multiple materials can be supplied by the same supplier.

4. **Relationships**:
   - `@OneToMany(mappedBy = "material", cascade = CascadeType.ALL, orphanRemoval = true)`: Defines a one-to-many relationship between `MaterialEntity` and `BatchEntity`. The `mappedBy` attribute points to the field in `BatchEntity` that references this entity.
   - `cascade = CascadeType.ALL` ensures that all CRUD operations on the parent (`MaterialEntity`) are cascaded to the children (`BatchEntity`).
   - `orphanRemoval = true` removes orphaned entities when they are removed from the set.

5. **Constructors and Getters/Setters**: Basic constructors and getters/setters for each field, ensuring that all properties can be accessed and modified as needed.

This code is designed to be production-ready, with proper naming conventions and annotations necessary for JPA entity mapping.