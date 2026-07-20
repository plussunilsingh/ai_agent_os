package com.example.domain.supplychain.service;

import com.example.domain.supplychain.entity.MaterialIntake;
import com.example.domain.supplychain.repository.MaterialIntakeRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
public class MaterialIntakeService {

    @Autowired
    private MaterialIntakeRepository materialIntakeRepository;

    /**
     * Save a new material intake record.
     *
     * @param materialIntake the material intake entity to save
     * @return the saved material intake entity
     */
    @Transactional
    public MaterialIntake saveMaterialIntake(MaterialIntake materialIntake) {
        return materialIntakeRepository.save(materialIntake);
    }

    /**
     * Get all material intakes.
     *
     * @return list of material intakes
     */
    public List<MaterialIntake> getAllMaterialIntakes() {
        return materialIntakeRepository.findAll();
    }

    /**
     * Find material intake by ID.
     *
     * @param id the ID of the material intake to find
     * @return the found material intake entity, or null if not found
     */
    public MaterialIntake getMaterialIntakeById(Long id) {
        return materialIntakeRepository.findById(id).orElse(null);
    }

    /**
     * Find material intakes by supplier ID.
     *
     * @param supplierId the ID of the supplier to filter by
     * @return list of material intakes from the specified supplier
     */
    public List<MaterialIntake> getMaterialIntakesBySupplierId(Long supplierId) {
        return materialIntakeRepository.findBySupplierId(supplierId);
    }

    /**
     * Find material intakes by product ID.
     *
     * @param productId the ID of the product to filter by
     * @return list of material intakes for the specified product
     */
    public List<MaterialIntake> getMaterialIntakesByProductId(Long productId) {
        return materialIntakeRepository.findByProductId(productId);
    }

    /**
     * Delete a material intake record.
     *
     * @param id the ID of the material intake to delete
     */
    @Transactional
    public void deleteMaterialIntake(Long id) {
        materialIntakeRepository.deleteById(id);
    }
}

### Explanation:
- **Service Layer**: The `MaterialIntakeService` class is responsible for business logic operations related to material intakes.
- **Repositories**: It uses a `MaterialIntakeRepository`, which should be implemented using Spring Data JPA with appropriate CRUD methods. The repository will handle the persistence layer.
- **Transactions**: Methods that interact directly with the database are marked with `@Transactional` to ensure data integrity and consistency.
- **Query Optimization**: JPQL queries within the repository (e.g., `findBySupplierId`, `findByProductId`) are optimized for performance, assuming indexes are properly set on the corresponding fields.

This code is production-ready and adheres to clean coding practices.