package com.example.domain.security;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.Table;

@Entity
@Table(name = "security_permissions")
public class PermissionEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String permissionName;

    public PermissionEntity() {
        // Default constructor for JPA
    }

    public PermissionEntity(String permissionName) {
        this.permissionName = permissionName;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getPermissionName() {
        return permissionName;
    }

    public void setPermissionName(String permissionName) {
        this.permissionName = permissionName;
    }
}

This code defines the `PermissionEntity` class, which maps to a table named `security_permissions`. The entity includes an ID for unique identification and a `permissionName` field to store the name of the permission. The constructor and getters/setters are provided to ensure proper object manipulation and persistence operations.

To optimize performance and ensure clean syntax, this code adheres to standard JPA practices and uses clear, concise methods.