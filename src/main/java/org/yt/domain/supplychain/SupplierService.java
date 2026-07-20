package com.example.domain.supplychain.service;

import com.example.domain.supplychain.entity.Supplier;
import com.example.domain.supplychain.repository.SupplierRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.List;
import java.util.Optional;

@Service
public class SupplierService {

    @Autowired
    private SupplierRepository supplierRepository;

    /**
     * Fetches a list of all suppliers from the database.
     *
     * @return List of Supplier entities.
     */
    public List<Supplier> getAllSuppliers() {
        return supplierRepository.findAll();
    }

    /**
     * Fetches a specific supplier by ID.
     *
     * @param id the ID of the supplier to fetch.
     * @return Optional containing the Supplier entity if found, otherwise empty.
     */
    public Optional<Supplier> getSupplierById(Long id) {
        return supplierRepository.findById(id);
    }

    /**
     * Saves or updates a supplier in the database.
     *
     * @param supplier the Supplier entity to save or update.
     * @return The saved or updated Supplier entity.
     */
    public Supplier saveSupplier(Supplier supplier) {
        return supplierRepository.save(supplier);
    }

    /**
     * Deletes a supplier from the database by ID.
     *
     * @param id the ID of the supplier to delete.
     */
    public void deleteSupplier(Long id) {
        supplierRepository.deleteById(id);
    }
}

package com.example.domain.supplychain.repository;

import com.example.domain.supplychain.entity.Supplier;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface SupplierRepository extends JpaRepository<Supplier, Long> {
    // Custom query methods can be added here if needed.
}

This code snippet provides a `SupplierService` class that manages supplier operations such as fetching all suppliers, getting a specific supplier by ID, saving or updating a supplier, and deleting a supplier. The service layer is responsible for business logic, while the repository handles data persistence.

The `SupplierRepository` interface extends `JpaRepository`, which provides CRUD operations out of the box. This setup ensures that the code is clean, maintainable, and leverages Spring Data JPA's powerful features.