package com.example.domain.supplychain.repository;

import com.example.domain.supplychain.model.Material;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface MaterialRepository extends JpaRepository<Material, Long> {

    @Query("SELECT m FROM Material m WHERE m.status = 'ACTIVE'")
    List<Material> findActiveMaterials();

    @Query("SELECT m FROM Material m WHERE m.id = :id")
    Optional<Material> findById(Long id);

    @Query(value = "SELECT * FROM materials WHERE status = 'ACTIVE'", nativeQuery = true)
    List<Material> findActiveMaterialsNativeQuery();
}

### Explanation:
1. **Imports and Package Declaration:**
   - The `com.example.domain.supplychain.model.Material` is the entity class for `Material`.
   - `JpaRepository` provides basic CRUD operations.
   - `@Repository` annotation marks this as a Spring Data repository.

2. **Methods:**
   - `findActiveMaterials`: A JPQL query to find all active materials.
   - `findById`: A method that uses the primary key (ID) to fetch an entity.
   - `findActiveMaterialsNativeQuery`: A native SQL query to find all active materials, which can be useful for performance optimization in certain scenarios.

### Notes:
- Ensure that the `Material` class is properly defined with necessary fields and annotations like `@Entity`, `@Id`, etc.
- Adjust package names according to your project structure.