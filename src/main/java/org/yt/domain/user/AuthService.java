package com.example.auth.domain.security;

import com.example.auth.domain.user.User;
import com.example.auth.domain.user.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class AuthService {

    private final UserRepository userRepository;

    @Autowired
    public AuthService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    /**
     * Authenticates the user and creates a session.
     *
     * @param username the username to authenticate
     * @param password the password to authenticate
     * @return the UserDetails object if authentication is successful, otherwise null
     */
    @Transactional
    public UserDetails authenticateUser(String username, String password) {
        User user = userRepository.findByUsername(username);

        if (user != null && user.getPassword().equals(password)) {
            return new CustomUserDetails(user);
        } else {
            return null;
        }
    }

    /**
     * Finds a user by their username.
     *
     * @param username the username to find
     * @return the User object if found, otherwise throws UsernameNotFoundException
     */
    @Transactional(readOnly = true)
    public User findUserByUsername(String username) {
        return userRepository.findByUsername(username)
                .orElseThrow(() -> new UsernameNotFoundException("User not found: " + username));
    }
}

// CustomUserDetails class for UserDetails implementation
class CustomUserDetails implements org.springframework.security.core.userdetails.UserDetails {

    private final User user;

    public CustomUserDetails(User user) {
        this.user = user;
    }

    @Override
    public String getPassword() {
        return user.getPassword();
    }

    @Override
    public String getUsername() {
        return user.getUsername();
    }

    @Override
    public boolean isAccountNonExpired() {
        return true; // or implement real logic if needed
    }

    @Override
    public boolean isAccountNonLocked() {
        return true; // or implement real logic if needed
    }

    @Override
    public boolean isCredentialsNonExpired() {
        return true; // or implement real logic if needed
    }

    @Override
    public boolean isEnabled() {
        return user.isEnabled();
    }
}

### Explanation:
1. **AuthService**: This service handles authentication.
   - `authenticateUser`: Authenticates the user by comparing the provided username and password with the stored credentials.
   - `findUserByUsername`: Finds a user by their username, throwing an exception if not found.

2. **CustomUserDetails**: Implements `UserDetails` interface for Spring Security to use. It contains methods like `getPassword`, `getUsername`, etc., which are required by Spring Security.

### Notes:
- Ensure that the `UserRepository` is properly configured and secured.
- The `password` comparison should ideally be done using a secure hashing mechanism, but this example uses plain comparison for simplicity.
- The `CustomUserDetails` class can be extended to include more details or methods as required by Spring Security.