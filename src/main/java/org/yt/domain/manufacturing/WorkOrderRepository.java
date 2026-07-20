package com.example.manufacturing.domain.workorder;

import com.example.manufacturing.domain.common.BaseEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface WorkOrderRepository extends JpaRepository<WorkOrder, Long> {
    // Custom query methods can be added here if needed
}

package com.example.manufacturing.domain.workorder;

import com.example.manufacturing.domain.common.BaseEntity;
import javax.persistence.*;
import java.util.Date;

@Entity
@Table(name = "work_order")
public class WorkOrder extends BaseEntity {

    @Column(nullable = false, unique = true)
    private String workOrderId;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "customer_id", nullable = false)
    private Customer customer;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "product_id", nullable = false)
    private Product product;

    @Column(nullable = false, columnDefinition = "TEXT")
    private String description;

    @Temporal(TemporalType.TIMESTAMP)
    @Column(name = "start_date", nullable = false)
    private Date startDate;

    @Temporal(TemporalType.TIMESTAMP)
    @Column(name = "end_date", nullable = true)
    private Date endDate;

    // Getters and Setters
}

package com.example.manufacturing.domain.workorder;

import javax.persistence.Entity;
import java.util.Date;

@Entity
@Table(name = "customer")
public class Customer extends BaseEntity {

    @Column(nullable = false, unique = true)
    private String customerId;

    @Column(nullable = false, columnDefinition = "TEXT")
    private String name;

    // Getters and Setters
}

package com.example.manufacturing.domain.workorder;

import javax.persistence.Entity;
import java.util.Date;

@Entity
@Table(name = "product")
public class Product extends BaseEntity {

    @Column(nullable = false, unique = true)
    private String productId;

    @Column(nullable = false, columnDefinition = "TEXT")
    private String name;

    // Getters and Setters
}

package com.example.manufacturing.domain.common;

import javax.persistence.MappedSuperclass;
import java.util.Date;

@MappedSuperclass
public abstract class BaseEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Temporal(TemporalType.TIMESTAMP)
    @Column(name = "created_date", nullable = false, updatable = false)
    private Date createdDate;

    // Getters and Setters

}

This code provides a `WorkOrderRepository` that extends `JpaRepository`, allowing for standard CRUD operations on the `WorkOrder` entity. The `WorkOrder` entity is mapped to a database table with appropriate fields, including relationships to `Customer` and `Product`. The `BaseEntity` class ensures common fields like `id` and `createdDate` are inherited by all entities.

If you need more specific query methods or further optimizations, please let me know!