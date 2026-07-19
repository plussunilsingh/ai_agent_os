package org.yt.service;

import org.springframework.stereotype.Service;
import org.yt.dto.AdminUserRequest;
import org.yt.model.AdminUser;
import org.yt.model.Role;

import java.util.*;
import java.util.concurrent.ConcurrentHashMap;

@Service
public class AdminUserService {

    private final Map<String, AdminUser> userStore = new ConcurrentHashMap<>();

    public AdminUserService() {
        // Initialize default seed data
        AdminUser root = new AdminUser(UUID.randomUUID().toString(), "admin_root", "root@yt.org", Role.SUPER_ADMIN);
        userStore.put(root.getId(), root);
    }

    public List<AdminUser> getAllUsers() {
        return new ArrayList<>(userStore.values());
    }

    public Optional<AdminUser> getUserById(String id) {
        return Optional.ofNullable(userStore.get(id));
    }

    public AdminUser createUser(AdminUserRequest request) {
        // Check duplicate email
        boolean emailExists = userStore.values().stream()
                .anyMatch(u -> u.getEmail().equalsIgnoreCase(request.getEmail()));
        if (emailExists) {
            throw new RuntimeException("Admin user with email '" + request.getEmail() + "' already exists");
        }

        String newId = UUID.randomUUID().toString();
        AdminUser user = new AdminUser(newId, request.getUsername(), request.getEmail(), request.getRole());
        userStore.put(newId, user);
        return user;
    }

    public AdminUser updateUser(String id, AdminUserRequest request) {
        AdminUser existing = userStore.get(id);
        if (existing == null) {
            throw new RuntimeException("Admin user not found with id: " + id);
        }

        existing.setUsername(request.getUsername());
        existing.setEmail(request.getEmail());
        existing.setRole(request.getRole());
        userStore.put(id, existing);
        return existing;
    }

    public boolean deleteUser(String id) {
        if (!userStore.containsKey(id)) {
            throw new RuntimeException("Admin user not found with id: " + id);
        }
        userStore.remove(id);
        return true;
    }
}
