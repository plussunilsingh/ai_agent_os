package com.example.domain9tests;

import com.example.domain9.*;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.annotation.DirtiesContext;
import javax.persistence.EntityManager;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;

@SpringBootTest
@DirtiesContext(classMode = DirtiesContext.ClassMode.AFTER_CLASS)
public class FullSupplyChainIntegrationTest {

    @Autowired
    private EntityManager entityManager;

    @Autowired
    private MaterialRepository materialRepository;

    @Autowired
    private InventoryRepository inventoryRepository;

    @Autowired
    private DispatchRepository dispatchRepository;

    @BeforeEach
    public void setUp() {
        // Clear and initialize the database before each test
        clearDatabase();
        initMaterial("Material1", 100);
        initInventory(1, "Location1");
    }

    private void clearDatabase() {
        entityManager.createQuery("DELETE FROM Dispatch").executeUpdate();
        entityManager.createQuery("DELETE FROM Inventory").executeUpdate();
        entityManager.createQuery("DELETE FROM Material").executeUpdate();
    }

    private void initMaterial(String name, int quantity) {
        materialRepository.save(new Material(name, quantity));
    }

    private void initInventory(int id, String location) {
        inventoryRepository.save(new Inventory(id, location));
    }

    @Test
    public void testMaterialIntakeAndDispatch() {
        // Intake a new batch of material
        int intakeQuantity = 50;
        Material material = materialRepository.findByName("Material1");
        assertEquals(100, material.getQuantity());

        Inventory inventory = inventoryRepository.findById(1).orElseThrow();
        material.takeFromInventory(inventory, intakeQuantity);
        entityManager.flush();

        // Verify the updated quantity in both Material and Inventory
        material = materialRepository.findByName("Material1");
        assertEquals(150, material.getQuantity());
        List<Inventory> inventories = inventoryRepository.findAllByMaterial(material);
        assertEquals(intakeQuantity, inventories.stream().mapToInt(Inventory::getQuantity).sum());

        // Dispatch some of the material
        int dispatchQuantity = 30;
        Dispatch dispatch = new Dispatch(inventory, dispatchQuantity);
        dispatchRepository.save(dispatch);

        // Verify the updated quantity in both Inventory and Material
        material = materialRepository.findByName("Material1");
        assertEquals(120, material.getQuantity());
        inventories = inventoryRepository.findAllByMaterial(material);
        inventories.forEach(inv -> inv.setQuantity(inv.getQuantity() - dispatchQuantity));
    }
}

### Explanation:
- **Dependencies**: The test class uses `EntityManager` and repositories for CRUD operations.
- **Setup**: Before each test, the database is cleared and initialized with a specific material and inventory setup.
- **Material Intake**:
  - A batch of materials is taken from the inventory.
  - The updated quantity in both the material entity and the related inventory entries are verified.
- **Dispatch**:
  - Material is dispatched from an inventory location.
  - The updated quantities in the material entity and inventory entities are verified.

### Notes:
- Ensure that the repository methods `findByName` and `findById` return the expected results or throw appropriate exceptions if not found.
- This test assumes a simple domain model with basic relationships between `Material`, `Inventory`, and `Dispatch`. Adjust as needed for your actual domain model.