package com.example.domain.security.repository;

import com.example.domain.security.model.Permission;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

/**
 * Repository interface for managing and querying permissions.
 */
@Repository
public interface PermissionRepository extends JpaRepository<Permission, Long> {

    /**
     * Finds a permission by its name.
     *
     * @param permissionName the name of the permission to find.
     * @return Optional containing the found permission or empty if not found.
     */
    Optional<Permission> findByPermissionName(String permissionName);

    /**
     * Checks if a user has a specific permission.
     *
     * @param userName the username of the user to check.
     * @param permissionName the name of the permission to check for.
     * @return true if the user has the permission, false otherwise.
     */
    boolean hasPermission(String userName, String permissionName);

    /**
     * Finds permissions by their names as a single query using JPQL.
     *
     * @param permissionNames an array of permission names to find.
     * @return a list of matching Permission entities or empty if none found.
     */
    default Iterable<Permission> findPermissionsByNames(String... permissionNames) {
        String jpql = "SELECT p FROM Permission p WHERE p.permissionName IN :permissionNames";
        return this.createQuery(jpql, (root, query, cb) -> cb.in(root.get("permissionName")).value(permissionNames)).getResultList();
    }

    /**
     * Custom query method to find permissions by their names.
     *
     * @param permissionNames the names of the permissions to find.
     * @return a TypedQuery for finding permissions by name.
     */
    default javax.persistence.TypedQuery<Permission> createQuery(String jpql, javax.persistence.criteria.CriteriaBuilder cb, javax.persistence.criteria.Root<Permission> root) {
        javax.persistence.criteria.CriteriaQuery<Permission> query = cb.createQuery(Permission.class);
        query.from(root);
        return this.getEntityManager().createQuery(query.where(cb.in(root.get("permissionName")).value(jpql.split(", "))));
    }
}

This code provides a `PermissionRepository` interface that extends Spring Data JPA's `JpaRepository`. It includes methods to find permissions by name and check if a user has a specific permission. Additionally, it includes a method to find multiple permissions using JPQL in a single query for better performance.

Make sure you have the necessary entities (`Permission`) and configuration set up properly in your Spring Boot application.