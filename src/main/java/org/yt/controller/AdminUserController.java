package org.yt.controller;

import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.yt.common.ApiResponse;
import org.yt.dto.AdminUserRequest;
import org.yt.model.AdminUser;
import org.yt.service.AdminUserService;

import java.util.List;

@RestController
@RequestMapping("/api/admin/users")
public class AdminUserController {

    private final AdminUserService adminUserService;

    public AdminUserController(AdminUserService adminUserService) {
        this.adminUserService = adminUserService;
    }

    @GetMapping
    public ResponseEntity<ApiResponse<List<AdminUser>>> getAllUsers() {
        List<AdminUser> users = adminUserService.getAllUsers();
        return ResponseEntity.ok(ApiResponse.success("Admin users retrieved successfully", users));
    }

    @GetMapping("/{id}")
    public ResponseEntity<ApiResponse<AdminUser>> getUserById(@PathVariable String id) {
        AdminUser user = adminUserService.getUserById(id)
                .orElseThrow(() -> new RuntimeException("Admin user not found with id: " + id));
        return ResponseEntity.ok(ApiResponse.success("Admin user retrieved", user));
    }

    @PostMapping
    public ResponseEntity<ApiResponse<AdminUser>> createUser(@Valid @RequestBody AdminUserRequest request) {
        AdminUser created = adminUserService.createUser(request);
        return new ResponseEntity<>(ApiResponse.success("Admin user created successfully", created), HttpStatus.CREATED);
    }

    @PutMapping("/{id}")
    public ResponseEntity<ApiResponse<AdminUser>> updateUser(@PathVariable String id, @Valid @RequestBody AdminUserRequest request) {
        AdminUser updated = adminUserService.updateUser(id, request);
        return ResponseEntity.ok(ApiResponse.success("Admin user updated successfully", updated));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<ApiResponse<Boolean>> deleteUser(@PathVariable String id) {
        boolean deleted = adminUserService.deleteUser(id);
        return ResponseEntity.ok(ApiResponse.success("Admin user deleted successfully", deleted));
    }
}
