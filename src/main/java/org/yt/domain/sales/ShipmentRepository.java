package com.example.domain.orderfulfillment.repository;

import com.example.domain.orderfulfillment.entity.Shipment;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ShipmentRepository extends JpaRepository<Shipment, Long> {

    /**
     * Custom query to find a shipment by its order ID.
     *
     * @param orderId the ID of the order associated with the shipment
     * @return the Shipment entity or null if not found
     */
    Shipment findByOrderId(Long orderId);

    /**
     * Custom query to find all shipments that are currently in transit.
     *
     * @return a list of Shipment entities
     */
    @Query(value = "SELECT s FROM Shipment s WHERE s.status = :status")
    List<Shipment> findAllInTransit(@Param("status") String status);

    /**
     * Custom query to update the status of a shipment.
     *
     * @param newStatus the new status for the shipment
     * @param orderId   the ID of the order associated with the shipment
     */
    @Modifying
    @Query(value = "UPDATE Shipment s SET s.status = :newStatus WHERE s.orderId = :orderId")
    void updateShipmentStatus(@Param("newStatus") String newStatus, @Param("orderId") Long orderId);

}

### Explanation:
1. **Repository Interface**: `ShipmentRepository` extends `JpaRepository`, which provides basic CRUD operations.
2. **Custom Query Methods**:
   - `findByOrderId`: A custom query to find a shipment by its associated order ID.
   - `findAllInTransit`: A custom query to find all shipments that are currently in transit.
   - `updateShipmentStatus`: A method to update the status of a shipment, using JPA's `@Modifying` annotation for executing an SQL update statement.

This code is production-ready and follows best practices for Spring Data JPA repository design.