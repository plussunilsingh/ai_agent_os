package org.yt.service;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.yt.dto.AdminUserRequest;
import org.yt.model.AdminUser;
import org.yt.model.Role;

import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;

class AdminUserServiceTest {

    private AdminUserService adminUserService;

    @BeforeEach
    void setUp() {
        adminUserService = new AdminUserService();
    }

    @Test
    void testInitialSeedDataExists() {
        List<AdminUser> users = adminUserService.getAllUsers();
        assertFalse(users.isEmpty());
        assertEquals(Role.SUPER_ADMIN, users.get(0).getRole());
    }

    @Test
    void testCreateUserSuccess() {
        AdminUserRequest request = new AdminUserRequest("johndoe", "john@yt.org", Role.ADMIN);
        AdminUser created = adminUserService.createUser(request);

        assertNotNull(created.getId());
        assertEquals("johndoe", created.getUsername());
        assertEquals("john@yt.org", created.getEmail());
        assertEquals(Role.ADMIN, created.getRole());
    }

    @Test
    void testCreateUserDuplicateEmailThrowsException() {
        AdminUserRequest request1 = new AdminUserRequest("user1", "dup@yt.org", Role.ADMIN);
        adminUserService.createUser(request1);

        AdminUserRequest request2 = new AdminUserRequest("user2", "dup@yt.org", Role.MODERATOR);
        assertThrows(RuntimeException.class, () -> adminUserService.createUser(request2));
    }

    @Test
    void testUpdateUserSuccess() {
        AdminUserRequest createReq = new AdminUserRequest("user_old", "old@yt.org", Role.MODERATOR);
        AdminUser created = adminUserService.createUser(createReq);

        AdminUserRequest updateReq = new AdminUserRequest("user_new", "new@yt.org", Role.ADMIN);
        AdminUser updated = adminUserService.updateUser(created.getId(), updateReq);

        assertEquals("user_new", updated.getUsername());
        assertEquals("new@yt.org", updated.getEmail());
        assertEquals(Role.ADMIN, updated.getRole());
    }

    @Test
    void testDeleteUserSuccess() {
        AdminUserRequest request = new AdminUserRequest("todelete", "delete@yt.org", Role.AUDITOR);
        AdminUser created = adminUserService.createUser(request);

        boolean deleted = adminUserService.deleteUser(created.getId());
        assertTrue(deleted);

        Optional<AdminUser> fetched = adminUserService.getUserById(created.getId());
        assertFalse(fetched.isPresent());
    }
}
