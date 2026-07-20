package com.example.domain.orderfulfillment.repository;

import com.example.domain.orderfulfillment.entity.Customer;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

/**
 * Repository interface for managing customer data using Spring Data JPA.
 */
@Repository
public interface CustomerRepository extends JpaRepository<Customer, Long> {

    /**
     * Finds a customer by email address.
     *
     * @param email the email address of the customer to find
     * @return the found customer or null if not found
     */
    Customer findByEmail(String email);

    /**
     * Finds customers whose names contain a given search term, case-insensitive.
     *
     * @param searchTerm the search term to filter by
     * @return a list of matching customers
     */
    @Query("SELECT c FROM Customer c WHERE LOWER(c.name) LIKE CONCAT('%',LOWER(?1),'%')")
    java.util.List<Customer> findByNameContainingIgnoreCase(String searchTerm);

    /**
     * Finds all customers who have placed at least one order.
     *
     * @return a list of customers with orders
     */
    @Query("SELECT DISTINCT c FROM Customer c JOIN c.orders o WHERE o.id IS NOT NULL")
    java.util.List<Customer> findAllWithOrders();

    /**
     * Counts the number of customers in the database.
     *
     * @return the count of all customers
     */
    @Query(value = "SELECT COUNT(*) FROM customer", nativeQuery = true)
    long countAllCustomers();
}

### Explanation:
1. **Imports**: The necessary imports are provided to ensure that the repository can interact with Spring Data JPA.
2. **Interface Definition**: `CustomerRepository` extends `JpaRepository`, which provides basic CRUD operations for the `Customer` entity.
3. **Custom Methods**:
   - `findByEmail`: A method to find a customer by their email address, using Spring Data's query derivation capabilities.
   - `findByNameContainingIgnoreCase`: Uses JPQL to perform a case-insensitive search on the customer name.
   - `findAllWithOrders`: Finds all customers who have placed at least one order. This is achieved using a JOIN between the `Customer` and `Order` entities.
   - `countAllCustomers`: A native query method to count all customers in the database, which returns an integer.

This code is designed for production use, ensuring clarity, performance, and maintainability.