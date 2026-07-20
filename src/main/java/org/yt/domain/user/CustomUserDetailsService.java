package com.example.security;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;
import javax.persistence.EntityManager;
import javax.persistence.PersistenceContext;
import java.util.Optional;

@Service("customUserDetailsService")
public class CustomUserDetailsService implements UserDetailsService {

    @PersistenceContext
    private EntityManager entityManager;

    @Autowired
    private UserRepository userRepository;

    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        Optional<User> userOptional = userRepository.findByUsername(username);
        return userOptional.orElseThrow(() -> new UsernameNotFoundException("User not found with username: " + username));
    }

    /**
     * Custom method to fetch the user by username using JPQL for better performance.
     */
    private User findUserByJPQL(String username) {
        String jpql = "SELECT u FROM User u WHERE u.username = :username";
        return entityManager.createQuery(jpql, User.class)
                .setParameter("username", username)
                .getResultList().stream()
                .findFirst()
                .orElse(null);
    }

    /**
     * Custom method to fetch the user by username using native query for performance optimization.
     */
    private User findUserByNativeQuery(String username) {
        String sql = "SELECT * FROM users WHERE username = ?";
        return entityManager.createNativeQuery(sql, User.class)
                .setParameter(1, username)
                .getSingleResult();
    }

    /**
     * Method to get user by ID using native query.
     */
    private User getUserById(Long userId) {
        String sql = "SELECT * FROM users WHERE id = ?";
        return entityManager.createNativeQuery(sql, User.class)
                .setParameter(1, userId)
                .getSingleResult();
    }
}


### Explanation:
- **EntityManager**: Injected to interact with the database.
- **UserRepository**: A custom repository interface for `User` entities.
- **loadUserByUsername**: This method is overridden from `UserDetailsService` and uses the `userRepository` to fetch a user by username. If no user is found, it throws a `UsernameNotFoundException`.
- **findUserByJPQL**: A custom method that performs a JPQL query to find a user by username.
- **findUserByNativeQuery**: A custom method that performs a native SQL query to find a user by username for performance optimization.
- **getUserById**: A method to fetch a user by ID using a native query.

### Notes:
- Ensure `User` entity and `UserRepository` are correctly defined.
- Adjust the package name, class names, and other identifiers as per your project structure.