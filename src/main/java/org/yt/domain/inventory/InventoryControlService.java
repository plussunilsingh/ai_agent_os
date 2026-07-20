package com.example.warehouse.services;

import com.example.warehouse.entities.Product;
import com.example.warehouse.repositories.ProductRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
public class InventoryControlService {

    private final ProductRepository productRepository;

    public InventoryControlService(ProductRepository productRepository) {
        this.productRepository = productRepository;
    }

    /**
     * Retrieves all products in the inventory.
     *
     * @return List of all products
     */
    @Transactional(readOnly = true)
    public List<Product> getAllProducts() {
        return productRepository.findAll();
    }

    /**
     * Finds a product by its ID.
     *
     * @param productId The ID of the product to find.
     * @return The found Product or null if not found.
     */
    @Transactional(readOnly = true)
    public Product getProductById(Long productId) {
        return productRepository.findById(productId).orElse(null);
    }

    /**
     * Updates the stock quantity for a given product.
     *
     * @param productId  The ID of the product to update.
     * @param newQuantity The new stock quantity.
     * @return The updated Product entity or null if not found.
     */
    @Transactional
    public Product updateStockQuantity(Long productId, int newQuantity) {
        return productRepository.findById(productId)
                .map(product -> {
                    product.setQuantity(newQuantity);
                    return productRepository.save(product);
                })
                .orElse(null);
    }

    /**
     * Deletes a product from the inventory by its ID.
     *
     * @param productId The ID of the product to delete.
     */
    @Transactional
    public void deleteProduct(Long productId) {
        productRepository.deleteById(productId);
    }

    /**
     * Retrieves products with stock quantity below a certain threshold.
     *
     * @param threshold The minimum stock quantity threshold.
     * @return List of products that have stock below the threshold.
     */
    @Transactional(readOnly = true)
    public List<Product> getLowStockProducts(int threshold) {
        return productRepository.findByQuantityLessThan(threshold);
    }
}

### Explanation:
- **Dependencies**: The `ProductRepository` is injected to interact with the database.
- **Methods**:
  - `getAllProducts`: Retrieves all products from the repository.
  - `getProductById`: Finds a product by its ID, returning null if not found.
  - `updateStockQuantity`: Updates the stock quantity of a product and saves it back to the database. Returns the updated entity or null if not found.
  - `deleteProduct`: Deletes a product from the repository by its ID.
  - `getLowStockProducts`: Retrieves products with a stock quantity below a specified threshold.

### Notes:
- The methods are annotated with `@Transactional` for proper handling of database transactions, ensuring data integrity and consistency.
- The `readOnly = true` annotation is used where applicable to optimize read operations by allowing the use of prepared statements instead of full transactions.