package com.example.domain1.repository;

import com.example.domain1.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface UserRepository extends JpaRepository<User, Long> {

    @Query("SELECT u FROM User u WHERE u.email = ?1 AND u.isActive = true")
    Optional<User> findByEmailAndActive(String email);

    @Query("SELECT u FROM User u JOIN FETCH u.roles r WHERE u.username = ?1")
    Optional<User> findUserWithRolesByUsername(String username);
}

### Explanation:
- **Repository Interface**: `UserRepository` extends `JpaRepository`, providing basic CRUD operations for the `User` entity.
- **Custom JPQL Queries**:
  - `findByEmailAndActive`: Retrieves a user by email if the account is active (`isActive = true`).
  - `findUserWithRolesByUsername`: Fetches the user and their associated roles in a single query using `JOIN FETCH`.

### Notes:
- Ensure that your `User` entity has fields such as `email`, `username`, and `isActive`.
- The `roles` field should be properly mapped with a many-to-many relationship if you are fetching roles.
- This code is designed to be used within the Spring Boot framework, assuming proper configuration for Spring Data JPA.