package com.example.warehouse.domain.entity;

import javax.persistence.*;
import java.time.LocalDateTime;
import java.util.UUID;

@Entity
@Table(name = "inventory_transactions")
public class InventoryTransactionEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private UUID transactionId;

    @Column(nullable = false)
    private LocalDateTime timestamp;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "product_id", nullable = false)
    private ProductEntity product;

    @Enumerated(EnumType.STRING)
    @Column(length = 20, nullable = false)
    private TransactionType transactionType;

    @Column(nullable = false)
    private int quantity;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "warehouse_id", nullable = false)
    private WarehouseEntity warehouse;

    public UUID getTransactionId() {
        return transactionId;
    }

    public void setTransactionId(UUID transactionId) {
        this.transactionId = transactionId;
    }

    public LocalDateTime getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(LocalDateTime timestamp) {
        this.timestamp = timestamp;
    }

    public ProductEntity getProduct() {
        return product;
    }

    public void setProduct(ProductEntity product) {
        this.product = product;
    }

    public TransactionType getTransactionType() {
        return transactionType;
    }

    public void setTransactionType(TransactionType transactionType) {
        this.transactionType = transactionType;
    }

    public int getQuantity() {
        return quantity;
    }

    public void setQuantity(int quantity) {
        this.quantity = quantity;
    }

    public WarehouseEntity getWarehouse() {
        return warehouse;
    }

    public void setWarehouse(WarehouseEntity warehouse) {
        this.warehouse = warehouse;
    }
}

enum TransactionType {
    INVENTORY_ADJUSTMENT,
    SALES_ORDER,
    PURCHASE_ORDER
}

### Explanation:
- **UUID**: `transactionId` is generated automatically and used as the primary key.
- **Timestamp**: `timestamp` records when the transaction occurred.
- **Product Entity Reference**: References a `ProductEntity` to track which product was involved in the transaction.
- **Transaction Type Enum**: `TransactionType` is an enumeration that includes possible types of transactions such as inventory adjustments, sales orders, and purchase orders.
- **Quantity**: The quantity of the item involved in the transaction.
- **Warehouse Entity Reference**: References a `WarehouseEntity` to track which warehouse the transaction occurred in.

This code provides a robust structure for managing stock ledger entries with appropriate JPA annotations and an enum for transaction types.