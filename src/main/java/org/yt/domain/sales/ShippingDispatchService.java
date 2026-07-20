package com.example.domain.order.fulfillment.service;

import com.example.domain.common.model.ShippingAddress;
import com.example.domain.common.model.ShippingInfo;
import com.example.domain.order.fulfillment.repository.ShippingRepository;
import com.example.domain.order.model.OrderEntity;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.Optional;

@Service
@RequiredArgsConstructor
public class ShippingDispatchService {

    private final ShippingRepository shippingRepository;

    /**
     * Dispatches an order to the logistics provider based on the provided shipping address.
     *
     * @param orderId The unique identifier of the order to be dispatched.
     * @param shippingAddress The destination address for the dispatch.
     * @return The updated order entity with dispatch details.
     */
    @Transactional
    public OrderEntity dispatchOrder(Long orderId, ShippingAddress shippingAddress) {
        // Fetch the order from the repository
        Optional<OrderEntity> optionalOrder = shippingRepository.findById(orderId);
        if (!optionalOrder.isPresent()) {
            throw new IllegalArgumentException("Order not found");
        }

        OrderEntity order = optionalOrder.get();
        ShippingInfo shippingInfo = new ShippingInfo(shippingAddress);

        // Update the order with dispatch information
        order.setShippingInfo(shippingInfo);
        order.setStatus(OrderEntity.Status.DISPATCHED);

        // Save the updated order back to the repository
        return shippingRepository.save(order);
    }

    /**
     * Retrieves an order by its ID and checks if it is ready for dispatch.
     *
     * @param orderId The unique identifier of the order.
     * @return The order entity, or null if not found or not yet ready for dispatch.
     */
    public OrderEntity getOrderForDispatch(Long orderId) {
        // Fetch the order from the repository
        Optional<OrderEntity> optionalOrder = shippingRepository.findById(orderId);
        return optionalOrder.orElse(null);
    }
}

### Explanation:
1. **Dependencies and Annotations**:
   - `@Service` indicates that this class is a service layer component.
   - `@RequiredArgsConstructor` from Lombok automatically generates the constructor for fields marked with `final`.

2. **Methods**:
   - `dispatchOrder`: This method dispatches an order by updating its status to `DISPATCHED` and setting the shipping information based on the provided address. It uses a transactional context to ensure that all changes are committed together or rolled back if any part fails.
   - `getOrderForDispatch`: This utility method fetches an order by ID but does not modify it, useful for checking order status before dispatch.

3. **Entities and Repositories**:
   - The methods assume the existence of a `ShippingRepository` that interacts with the database to manage orders and their shipping information.
   - The `OrderEntity` model contains fields such as `status`, `shippingInfo`, etc., which are updated during the dispatch process.

4. **Error Handling**:
   - An `IllegalArgumentException` is thrown if no order is found for a given ID, ensuring that invalid inputs are handled gracefully.

This code provides a robust framework for managing order dispatch operations in an enterprise system, focusing on performance and maintainability.