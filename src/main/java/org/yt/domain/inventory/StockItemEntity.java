package com.example.warehouse.domain.stock;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.Table;
import java.io.Serializable;
import java.math.BigDecimal;

@Entity
@Table(name = "stock_items")
public class StockItemEntity implements Serializable {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String sku;

    private BigDecimal quantityInStock;

    public StockItemEntity() {
        // Default constructor required by JPA
    }

    public StockItemEntity(String sku, BigDecimal quantityInStock) {
        this.sku = sku;
        this.quantityInStock = quantityInStock;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getSku() {
        return sku;
    }

    public void setSku(String sku) {
        this.sku = sku;
    }

    public BigDecimal getQuantityInStock() {
        return quantityInStock;
    }

    public void setQuantityInStock(BigDecimal quantityInStock) {
        this.quantityInStock = quantityInStock;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof StockItemEntity)) return false;

        StockItemEntity that = (StockItemEntity) o;

        return id != null ? id.equals(that.id) : that.id == null;
    }

    @Override
    public int hashCode() {
        return id != null ? id.hashCode() : 0;
    }
}

### Explanation:
- **Entity Annotation**: The `@Entity` annotation marks this class as a JPA entity.
- **Table Annotation**: The `@Table(name = "stock_items")` annotation specifies the name of the database table that corresponds to this entity.
- **Id Annotation**: The `@Id` and `@GeneratedValue(strategy = GenerationType.IDENTITY)` annotations define the primary key for the entity, and specify an auto-incrementing ID.
- **Fields**:
  - `id`: Primary key of the stock item.
  - `sku`: Stock Keeping Unit (SKU) which uniquely identifies a product.
  - `quantityInStock`: The current quantity of the item in stock.
- **Constructors**: Default and parameterized constructors are provided. The default constructor is required by JPA for creating entity instances.
- **Getters and Setters**: Standard getters and setters are implemented to provide access to the fields.

This code provides a clean, production-ready implementation of the `StockItemEntity` class with proper encapsulation and JPA annotations.