package com.example.warehouse.stock.repository;

import com.example.warehouse.stock.entity.InventoryTransaction;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;

@Repository
@Transactional(readOnly = true)
public interface InventoryTransactionRepository extends JpaRepository<InventoryTransaction, Long> {

    /**
     * Custom query to find all inventory transactions by product ID.
     * @param productId the product ID to filter by.
     * @return a list of matching inventory transactions or an empty list if none found.
     */
    List<InventoryTransaction> findByProductId(Long productId);

    /**
     * Custom query to find a single inventory transaction by its ID.
     * @param id the ID of the inventory transaction to retrieve.
     * @return the optional inventory transaction object or empty if not found.
     */
    Optional<InventoryTransaction> findById(Long id);

    /**
     * Custom query to find all inventory transactions by warehouse ID.
     * @param warehouseId the warehouse ID to filter by.
     * @return a list of matching inventory transactions or an empty list if none found.
     */
    List<InventoryTransaction> findByWarehouseId(Long warehouseId);

    /**
     * Custom query to find all inventory transactions within a date range.
     * @param startDate the start date for filtering.
     * @param endDate the end date for filtering.
     * @return a list of matching inventory transactions or an empty list if none found.
     */
    List<InventoryTransaction> findByDateBetween(java.util.Date startDate, java.util.Date endDate);

    /**
     * Custom query to find all inventory transactions by product name.
     * @param productName the product name to filter by.
     * @return a list of matching inventory transactions or an empty list if none found.
     */
    List<InventoryTransaction> findByProductName(String productName);
}

### Explanation:
1. **Repository Interface**:
   - The `InventoryTransactionRepository` interface extends `JpaRepository`, which provides CRUD operations for the `InventoryTransaction` entity.
   
2. **Custom Queries**:
   - `findByProductId`: Retrieves all inventory transactions associated with a specific product ID.
   - `findById`: Finds a single transaction by its unique identifier.
   - `findByWarehouseId`: Retrieves all inventory transactions from a specific warehouse.
   - `findByDateBetween`: Fetches transactions between two dates.
   - `findByProductName`: Retrieves transactions involving a specific product name.

3. **Transactional Attributes**:
   - The `@Transactional(readOnly = true)` annotation ensures that the repository methods are read-only by default, which can help in optimizing performance and ensuring data integrity during write operations.

4. **Return Types**:
   - Methods like `findById` return an `Optional<InventoryTransaction>` to handle cases where no transaction is found.
   - Other query methods return a list of `InventoryTransaction`.

This code should be integrated into your Spring Boot application, and the corresponding entity (`InventoryTransaction`) must be defined. Ensure that the database schema matches the JPA annotations on the entity class for proper data retrieval.