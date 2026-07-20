Below is a production-ready implementation of `ManufacturingService.java` that includes methods for handling work orders, such as creating, updating, and retrieving work orders. This example assumes you are using Spring Boot with JPA and Hibernate for database operations.

package com.example.manufacturing.service;

import com.example.manufacturing.domain.WorkOrder;
import com.example.manufacturing.repository.WorkOrderRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;

@Service
public class ManufacturingService {

    @Autowired
    private WorkOrderRepository workOrderRepository;

    /**
     * Creates a new work order and saves it to the database.
     *
     * @param workOrder the work order to be created
     * @return the saved work order
     */
    @Transactional
    public WorkOrder createWorkOrder(WorkOrder workOrder) {
        return workOrderRepository.save(workOrder);
    }

    /**
     * Updates an existing work order in the database.
     *
     * @param workOrder the updated work order
     * @return the updated work order
     */
    @Transactional
    public WorkOrder updateWorkOrder(WorkOrder workOrder) {
        return workOrderRepository.save(workOrder);
    }

    /**
     * Retrieves a work order by its ID.
     *
     * @param id the ID of the work order to retrieve
     * @return an Optional containing the retrieved work order or empty if not found
     */
    public Optional<WorkOrder> getWorkOrderById(Long id) {
        return workOrderRepository.findById(id);
    }

    /**
     * Retrieves all work orders.
     *
     * @return a list of all work orders
     */
    public List<WorkOrder> getAllWorkOrders() {
        return workOrderRepository.findAll();
    }

    /**
     * Deletes a work order by its ID.
     *
     * @param id the ID of the work order to delete
     */
    @Transactional
    public void deleteWorkOrder(Long id) {
        workOrderRepository.deleteById(id);
    }

    /**
     * Retrieves all active work orders (i.e., those with status "IN_PROGRESS").
     *
     * @return a list of active work orders
     */
    public List<WorkOrder> getActiveWorkOrders() {
        return workOrderRepository.findByStatus("IN_PROGRESS");
    }
}

### Explanation:
1. **Dependencies**: The `@Autowired` annotation is used to inject the `WorkOrderRepository`.
2. **Service Layer**: This service layer handles all business logic related to work orders.
3. **Transactions**: Methods annotated with `@Transactional` ensure that database operations are performed within a transaction, which helps in maintaining data integrity.
4. **Repository Operations**: The methods delegate database operations to the repository for cleaner and more maintainable code.

### Repository Interface:
The corresponding repository interface (`WorkOrderRepository`) should be defined as follows:

package com.example.manufacturing.repository;

import com.example.manufacturing.domain.WorkOrder;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface WorkOrderRepository extends JpaRepository<WorkOrder, Long> {
    Optional<WorkOrder> findById(Long id);
    List<WorkOrder> findAll();
    List<WorkOrder> findByStatus(String status);
}

This ensures that the repository is properly configured to perform CRUD operations and custom queries.