package org.yt.repository;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.yt.model.AdminUser;
import org.yt.repository.AdminUserRepository;

import static org.junit.jupiter.api.Assertions.*;

@DataJpaTest
public class AdminRepositoryTest {

    @Autowired
    private AdminUserRepository adminUserRepository;

    @Test
    public void testCreateAdminUser() {
        // Arrange
        AdminUser adminUser = new AdminUser();
        adminUser.setUsername("testUser");
        adminUser.setPassword("password123");

        // Act
        AdminUser savedUser = adminUserRepository.save(adminUser);

        // Assert
        assertNotNull(savedUser.getId());
    }

    @Test
    public void testReadAdminUser() {
        // Arrange (assuming the user is created in the previous test)
        Long userId = 1L; // Replace with actual ID after saving

        // Act
        AdminUser retrievedUser = adminUserRepository.findById(userId).orElse(null);

        // Assert
        assertNotNull(retrievedUser);
        assertEquals("testUser", retrievedUser.getUsername());
    }

    @Test
    public void testUpdateAdminUser() {
        // Arrange (assuming the user is created in the previous test)
        Long userId = 1L; // Replace with actual ID after saving

        // Act
        AdminUser adminUser = adminUserRepository.findById(userId).orElse(null);
        assertNotNull(adminUser);

        adminUser.setUsername("updatedTestUser");
        AdminUser updatedUser = adminUserRepository.save(adminUser);

        // Assert
        assertEquals("updatedTestUser", updatedUser.getUsername());
    }

    @Test
    public void testDeleteAdminUser() {
        // Arrange (assuming the user is created in the previous test)
        Long userId = 1L; // Replace with actual ID after saving

        // Act
        AdminUser adminUser = adminUserRepository.findById(userId).orElse(null);
        assertNotNull(adminUser);

        adminUserRepository.delete(adminUser);

        // Assert
        assertNull(adminUserRepository.findById(userId).orElse(null));
    }
}