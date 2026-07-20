package com.example.demo.controller;

import com.example.demo.dto.LoginRequest;
import com.example.demo.dto.RegisterRequest;
import com.example.demo.entity.User;
import com.example.demo.repository.UserRepository;
import com.example.demo.service.AuthService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.web.bind.annotation.*;

import java.util.Optional;

@RestController
@RequestMapping("/api/auth")
public class AuthController {

    @Autowired
    private AuthService authService;

    @Autowired
    private UserRepository userRepository;

    /**
     * Login endpoint.
     *
     * @param loginRequest the login request containing username and password
     * @return a response entity with an authentication token or an error message
     */
    @PostMapping("/login")
    public ResponseEntity<String> login(@Valid @RequestBody LoginRequest loginRequest) {
        try {
            String token = authService.login(loginRequest.getUsername(), loginRequest.getPassword());
            return ResponseEntity.ok(token);
        } catch (UsernameNotFoundException e) {
            return ResponseEntity.badRequest().body("User not found");
        }
    }

    /**
     * Register endpoint.
     *
     * @param registerRequest the registration request containing username, password, and email
     * @return a response entity with success message or an error message
     */
    @PostMapping("/register")
    public ResponseEntity<String> register(@Valid @RequestBody RegisterRequest registerRequest) {
        try {
            authService.register(registerRequest.getUsername(), registerRequest.getPassword(), registerRequest.getEmail());
            return ResponseEntity.ok("User registered successfully");
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(e.getMessage());
        }
    }

    /**
     * Method to save user entity.
     *
     * @param user the user entity
     */
    private void saveUser(User user) {
        userRepository.save(user);
    }
}

### Explanation:
1. **Dependencies**: The `@Autowired` annotations are used to inject dependencies like `AuthService` and `UserRepository`.
2. **Endpoints**:
   - `POST /api/auth/login`: Handles the login process.
   - `POST /api/auth/register`: Handles user registration.
3. **Error Handling**: Basic error handling is included for cases where a username is not found during login or when an exception occurs during registration.

### Notes:
- Ensure that `AuthService` and `UserRepository` are well-optimized and handle database operations efficiently.
- You can add more detailed validation and security measures as needed, such as password hashing, email verification, etc.