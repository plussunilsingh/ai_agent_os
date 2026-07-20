package com.example.supplychain.repository;

import com.example.supplychain.entity.Inspection;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

/**
 * Repository interface for managing Inspections.
 */
@Repository
public interface InspectionRepository extends JpaRepository<Inspection, Long> {

    /**
     * Custom query to find inspections by product ID and status.
     *
     * @param productId the product ID to filter by.
     * @param status the inspection status to filter by.
     * @return a list of inspections matching the criteria.
     */
    public Iterable<Inspection> findByProductIdAndStatus(Long productId, String status);

    /**
     * Custom query to find latest inspections for each product.
     *
     * @return a list of latest inspections grouped by product ID.
     */
    public Iterable<Inspection> findDistinctByOrderByCreationDateDesc();
}

### Explanation:
- **Repository Interface**: This interface extends `JpaRepository`, providing CRUD operations out-of-the-box. It includes specific query methods for custom filtering and ordering.
  
- **Custom Query Methods**:
  - `findByProductIdAndStatus`: A method that allows finding inspections by product ID and status, returning a list of matching inspections.
  - `findDistinctByOrderByCreationDateDesc`: A method to find the latest inspection record for each product based on creation date.

### Usage Example:

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class InspectionService {

    private final InspectionRepository inspectionRepository;

    @Autowired
    public InspectionService(InspectionRepository inspectionRepository) {
        this.inspectionRepository = inspectionRepository;
    }

    /**
     * Find all inspections for a given product and status.
     *
     * @param productId the product ID to filter by.
     * @param status the inspection status to filter by.
     * @return a list of inspections matching the criteria.
     */
    public Iterable<Inspection> findInspectionsByProductIdAndStatus(Long productId, String status) {
        return inspectionRepository.findByProductIdAndStatus(productId, status);
    }

    /**
     * Find the latest inspection for each product.
     *
     * @return a list of latest inspections grouped by product ID.
     */
    public Iterable<Inspection> findLatestInspectionsByProduct() {
        return inspectionRepository.findDistinctByOrderByCreationDateDesc();
    }
}

### Notes:
- Ensure that `Inspection` entity is correctly defined with fields such as `productId`, `status`, and `creationDate`.
- Use proper validation and error handling in a real application.
- The provided code assumes the use of Spring Boot and JPA.