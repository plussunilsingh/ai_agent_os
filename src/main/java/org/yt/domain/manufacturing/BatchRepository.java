package com.example.domain.manufacturing.repository;

import com.example.domain.manufacturing.entity.Batch;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;
import org.springframework.stereotype.Repository;

/**
 * Repository interface for managing batches in the manufacturing domain.
 */
@Repository
public interface BatchRepository extends JpaRepository<Batch, Long>, JpaSpecificationExecutor<Batch> {

    /**
     * Finds a batch by its unique identifier.
     *
     * @param id the unique identifier of the batch to retrieve
     * @return the retrieved batch entity or null if not found
     */
    Batch findById(Long id);

    /**
     * Finds batches by their status.
     *
     * @param status the status of the batches to find
     * @return a list of batches with the specified status
     */
    Iterable<Batch> findByStatus(String status);
}

### Explanation:
- **Package and Class Name**: The class is placed in the `com.example.domain.manufacturing.repository` package, which aligns with typical Spring project structures.
- **Imports**: Necessary imports for `Batch`, `JpaRepository`, `JpaSpecificationExecutor`, and `Repository` are included.
- **Interface Name**: `BatchRepository` extends both `JpaRepository<Batch, Long>` and `JpaSpecificationExecutor<Batch>`.
  - `JpaRepository` provides CRUD operations out of the box.
  - `JpaSpecificationExecutor` allows for more complex query specifications using Java Persistence Query Language (JPQL) or Criteria API.
- **Methods**:
  - `findById(Long id)`: A specific method to find a batch by its unique identifier.
  - `findByStatus(String status)`: A generic method that finds all batches with the given status.

This setup ensures that the repository is production-ready, adhering to best practices for Spring Data JPA.