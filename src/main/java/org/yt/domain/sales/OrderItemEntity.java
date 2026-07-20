package com.example.domain.order.fulfillment;

import jakarta.persistence.*;
import lombok.*;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Entity
@Table(name = "ORDER_ITEMS")
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@AllArgsConstructor
@Getter
@Setter
@Builder
public class OrderItemEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "ORDER_ID", nullable = false, foreignKey = @ForeignKey(name = "FK_ORDER_ITEM_TO_ORDER"))
    private OrderEntity order;

    @Column(nullable = false)
    private String productSku;

    @Column(nullable = false)
    private BigDecimal price;

    @Column(nullable = false)
    private int quantity;

    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt = LocalDateTime.now();

    @Version
    @Column(name = "OPTLOCK_VERSION")
    private long version;

    public OrderItemEntity(OrderEntity order, String productSku, BigDecimal price, int quantity) {
        this.order = order;
        this.productSku = productSku;
        this.price = price;
        this.quantity = quantity;
    }

    public void updatePrice(BigDecimal newPrice) {
        this.price = newPrice;
    }

    public void increaseQuantity(int amount) {
        this.quantity += amount;
    }

    public void decreaseQuantity(int amount) {
        if (this.quantity >= amount) {
            this.quantity -= amount;
        } else {
            throw new IllegalArgumentException("Insufficient quantity to decrease");
        }
    }
}

This code defines the `OrderItemEntity` class, which is a JPA entity for managing line items in an order. The class includes:

- Lombok annotations for reducing boilerplate code.
- A constructor that takes all necessary fields.
- Methods to update and manage quantities and prices.
- Proper field accessors and mutators.

Ensure your database schema matches the table name (`ORDER_ITEMS`) and column names used in this entity. Adjust the foreign key constraints as per your specific requirements.