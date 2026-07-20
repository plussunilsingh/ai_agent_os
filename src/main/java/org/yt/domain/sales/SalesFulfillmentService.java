package com.example.domain.order.fulfillment;

import com.example.domain.common.exceptions.ServiceException;
import com.example.domain.order.OrderRepository;
import com.example.domain.product.ProductRepository;
import com.example.domain.shipping.ShippingRepository;
import com.example.infrastructure.jpa.entities.OrderEntity;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import javax.persistence.EntityManager;
import javax.persistence.PersistenceContext;
import java.util.List;
import java.util.Optional;

@Service
public class SalesFulfillmentService {

    @Autowired
    private OrderRepository orderRepository;

    @Autowired
    private ProductRepository productRepository;

    @Autowired
    private ShippingRepository shippingRepository;

    @PersistenceContext
    private EntityManager entityManager;

    @Transactional
    public void processOrder(OrderEntity order) throws ServiceException {
        if (order == null || !validateOrder(order)) {
            throw new ServiceException("Invalid or missing order data.");
        }

        // Ensure all products are available
        for (var item : order.getItems()) {
            var product = productRepository.findById(item.getProductId())
                    .orElseThrow(() -> new ServiceException("Product not found: " + item.getProductId()));
            if (product.getStock() < item.getQuantity()) {
                throw new ServiceException(String.format("Insufficient stock for product %s", item.getProductId()));
            }
        }

        // Process order
        orderRepository.save(order);

        // Deduct from stock
        for (var item : order.getItems()) {
            var product = productRepository.findById(item.getProductId())
                    .orElseThrow(() -> new ServiceException("Product not found: " + item.getProductId()));
            product.setStock(product.getStock() - item.getQuantity());
            productRepository.save(product);
        }

        // Schedule shipping
        var shippingEntity = new ShippingEntity();
        shippingEntity.setOrder(order);
        shippingRepository.save(shippingEntity);

        // Persist changes to the database
        entityManager.flush();
    }

    private boolean validateOrder(OrderEntity order) {
        return order != null && !order.getItems().isEmpty() && order.getCustomer() != null;
    }
}

### Explanation:

1. **Dependencies**: The class is annotated with `@Service` and depends on repositories for orders, products, and shipping.
2. **Transaction Management**: Method `processOrder` is marked as transactional to ensure atomic operations.
3. **Validation**: The order is validated before processing.
4. **Product Stock Check**: Ensures that the required quantity of each product in the order is available.
5. **Database Operations**:
   - Saves the order and updates the product stock levels.
   - Creates a new shipping record linked to the processed order.
6. **Error Handling**: Throws `ServiceException` for invalid or missing data, insufficient stock, or other issues.
7. **Persistence Context**: Injects the EntityManager to handle database operations directly.

This code is designed to be production-ready and follows best practices for service layer implementation in a Spring application.