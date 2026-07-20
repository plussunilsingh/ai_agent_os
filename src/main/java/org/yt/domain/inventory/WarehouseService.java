package com.example.domain.warehouse.service;

import com.example.domain.warehouse.entity.Warehouse;
import com.example.domain.warehouse.repository.WarehouseRepository;
import com.example.common.exception.ResourceNotFoundException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.List;

@Service
public class WarehouseService {

    private final WarehouseRepository warehouseRepository;

    @Autowired
    public WarehouseService(WarehouseRepository warehouseRepository) {
        this.warehouseRepository = warehouseRepository;
    }

    /**
     * Retrieves a list of all warehouses.
     *
     * @return List of all warehouses.
     */
    public List<Warehouse> getAllWarehouses() {
        return warehouseRepository.findAll();
    }

    /**
     * Finds a warehouse by its ID.
     *
     * @param id the ID of the warehouse to find.
     * @return the found Warehouse entity or throws an exception if not found.
     */
    public Warehouse getWarehouseById(Long id) {
        return warehouseRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Warehouse not found with ID: " + id));
    }

    /**
     * Saves a new warehouse or updates an existing one.
     *
     * @param warehouse the Warehouse entity to save or update.
     * @return the saved or updated Warehouse entity.
     */
    public Warehouse saveWarehouse(Warehouse warehouse) {
        return warehouseRepository.save(warehouse);
    }

    /**
     * Deletes a warehouse by its ID.
     *
     * @param id the ID of the warehouse to delete.
     */
    public void deleteWarehouse(Long id) {
        warehouseRepository.deleteById(id);
    }

    /**
     * Retrieves warehouses based on specific criteria using JPQL query optimization.
     *
     * @param location the location parameter for filtering.
     * @return List of warehouses matching the location criteria.
     */
    public List<Warehouse> findWarehousesByLocation(String location) {
        return warehouseRepository.findWarehousesByLocation(location);
    }
}

### Explanation:
1. **Service Layer**: The `WarehouseService` class is a service layer that interacts with the database through the `WarehouseRepository`.
2. **Dependency Injection**: The constructor injects the `WarehouseRepository` to manage interactions with the database.
3. **Methods**:
   - `getAllWarehouses()`: Retrieves all warehouses from the database.
   - `getWarehouseById(Long id)`: Finds a warehouse by its ID and throws an exception if not found.
   - `saveWarehouse(Warehouse warehouse)`: Saves or updates a warehouse in the database.
   - `deleteWarehouse(Long id)`: Deletes a warehouse by its ID.
   - `findWarehousesByLocation(String location)`: Uses JPQL to retrieve warehouses based on specific criteria, optimized for performance.

This code is designed to be clean, efficient, and production-ready.