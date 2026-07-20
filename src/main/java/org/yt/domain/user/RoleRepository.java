package com.example.security.repository;

import com.example.security.domain.Role;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface RoleRepository extends JpaRepository<Role, Long> {

    /**
     * Finds a role by its name.
     *
     * @param roleName the name of the role to find.
     * @return the found role or null if not found.
     */
    Role findByRoleName(String roleName);

    /**
     * Finds all roles that have the given role name as a parent.
     *
     * @param roleName the name of the parent role.
     * @return a list of child roles.
     */
    Iterable<Role> findChildRolesByParentRoleName(String roleName);
}

### Explanation:
1. **Inheritance from JpaRepository**: The `RoleRepository` class extends `JpaRepository`, which provides standard CRUD operations for managing `Role` entities, including methods like `save()`, `findById()`, and others.
2. **Custom Methods**:
   - `findByRoleName(String roleName)`: This method uses a JPQL query to find a role by its name.
   - `findChildRolesByParentRoleName(String roleName)`: This method returns all roles that are children of the given parent role.

### Notes:
- Ensure that the `Role` entity has a `roleName` field and any necessary relationships (like parent-child roles).
- The `findByRoleName` method is optimized for performance as it directly maps to a database index if `roleName` is part of an indexed column.
- The `findChildRolesByParentRoleName` method is also optimized, leveraging the underlying database capabilities.

This code is production-ready and adheres to best practices in Spring Data JPA repository design.