package com.example.ordersystem.repository;

import com.example.ordersystem.entity.SalesOrder;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface SalesOrderRepository extends JpaRepository<SalesOrder, Long> {

    /**
     * Find all sales orders by customer ID.
     *
     * @param customerId the customer ID
     * @return a list of SalesOrder entities
     */
    List<SalesOrder> findAllByCustomerId(Long customerId);

    /**
     * Find an order by its ID.
     *
     * @param id the ID of the sales order
     * @return the SalesOrder entity or null if not found
     */
    Optional<SalesOrder> findById(Long id);

    /**
     * Custom JPQL query to find orders that are overdue.
     *
     * @return a list of SalesOrder entities that are overdue
     */
    @Query("SELECT so FROM SalesOrder so WHERE so.orderDate < :dueDate AND so.status = 'PENDING'")
    List<SalesOrder> findByOverDueOrders(@javax.persistence.NamedStoredProcedureParameter(name = "dueDate", value = java.util.Date.class) java.util.Date dueDate);

    /**
     * Custom JPQL query to find orders that have been placed by a specific customer and are in the pending status.
     *
     * @param customerId the ID of the customer
     * @return a list of SalesOrder entities
     */
    @Query("SELECT so FROM SalesOrder so WHERE so.customerId = :customerId AND so.status = 'PENDING'")
    List<SalesOrder> findByCustomerAndStatus(Long customerId);
}

### Explanation:
1. **Generic Repository Interface**: The `SalesOrderRepository` extends `JpaRepository`, providing CRUD operations for the `SalesOrder` entity.
2. **Custom Queries**:
   - `findAllByCustomerId`: A method to find all sales orders associated with a specific customer ID.
   - `findById`: An optional method to retrieve an order by its unique identifier.
   - `findByOverDueOrders`: A custom JPQL query to identify overdue orders based on the order date and status.
   - `findByCustomerAndStatus`: Another custom JPQL query to find pending orders placed by a specific customer.

### Notes:
- Ensure that the `SalesOrder` entity has the appropriate fields (e.g., `orderDate`, `status`, `customerId`) for these queries to work correctly.
- The `@Query` annotation is used to define custom JPQL queries. Note that in real-world applications, you might need to parameterize these queries with actual date values or other parameters.

This code provides a robust foundation for managing sales orders within the order fulfillment domain using Spring Data JPA and JPQL.