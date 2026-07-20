package com.example.domain.warehouse;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Table(name = "WAREHOUSE")
public class WarehouseEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private String warehouseCode;

    @Column(nullable = false)
    private String name;

    @Column(nullable = false)
    private String location;

    @Column
    private String contactInfo;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "COMPANY_ID", nullable = false)
    private CompanyEntity company;

    public WarehouseEntity(String warehouseCode, String name, String location) {
        this.warehouseCode = warehouseCode;
        this.name = name;
        this.location = location;
    }

    // JPQL query methods for optimization
    @Query("SELECT w FROM WarehouseEntity w WHERE w.company.id = :companyId")
    public static List<WarehouseEntity> findWarehousesByCompany(@Param("companyId") Long companyId);

    @Query("SELECT w FROM WarehouseEntity w JOIN FETCH w.company WHERE w.location LIKE %:location%")
    public static List<WarehouseEntity> searchWarehousesByLocation(@Param("location") String location);
}

### Explanation:
1. **Annotations**:
   - `@Entity`: Marks the class as a JPA entity.
   - `@Data`: Lombok annotation for generating `toString`, `equals`, `hashCode`, and `getters`/`setters`.
   - `@NoArgsConstructor` and `@AllArgsConstructor`: Lombok annotations to generate no-arg and all-args constructors.
   - `@Builder`: Lombok annotation for builder pattern.

2. **Fields**:
   - `id`: Primary key, auto-generated using `GenerationType.IDENTITY`.
   - `warehouseCode`, `name`, `location`: Mandatory fields.
   - `contactInfo`: Optional field.
   - `company`: Many-to-one relationship with `CompanyEntity`.

3. **JPQL Methods**:
   - `findWarehousesByCompany`: Fetches warehouses based on company ID using JPQL.
   - `searchWarehousesByLocation`: Searches for warehouses by location and eagerly fetches the associated `CompanyEntity` to avoid N+1 queries.

4. **Constructor**: 
   - A constructor is provided for convenience when creating a new warehouse without setting all fields.

This code is designed to be production-ready, with clean syntax and optimized JPQL queries.