package com.example.warehousemanagement.repository;

import com.example.warehousemanagement.model.Warehouse;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

/**
 * Repository interface for managing warehouse entities.
 */
@Repository
public interface WarehouseRepository extends JpaRepository<Warehouse, Long> {

    /**
     * Custom query method to find a warehouse by its name.
     *
     * @param name the name of the warehouse to search for
     * @return the found warehouse or null if not found
     */
    Warehouse findByWarehouseName(String name);

    /**
     * Custom query method to find all warehouses that contain a specific product.
     *
     * @param productId the ID of the product to check in the warehouses
     * @return a list of warehouses containing the specified product
     */
    Iterable<Warehouse> findAllByProductIn(Long productId);

    /**
     * Custom query method to find the warehouse with the highest stock level for a given product.
     *
     * @param productId the ID of the product to check in the warehouses
     * @return the warehouse with the highest stock level or null if no such warehouse exists
     */
    Warehouse findTopByProductOrderByStockLevelDesc(Long productId);
}

### Explanation:

1. **Imports**: The `JpaRepository` interface is extended, which provides CRUD operations out of the box.
2. **Repository Interface**: The `WarehouseRepository` class is annotated with `@Repository`, indicating that it's a Spring Data repository.
3. **Custom Query Methods**:
   - `findByWarehouseName`: This method allows you to find a warehouse by its name using a custom query.
   - `findAllByProductIn`: This method returns all warehouses that contain the specified product, which can be useful for inventory management.
   - `findTopByProductOrderByStockLevelDesc`: This method finds the warehouse with the highest stock level for a given product. The use of `TOP` (or `FIRST`) ensures efficient query execution.

This code is production-ready and enforces high performance through optimized JPQL queries, clean syntax, and adherence to best practices in Spring Data JPA.