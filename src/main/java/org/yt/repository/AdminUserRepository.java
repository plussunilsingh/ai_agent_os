package org.yt.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.yt.entity.AdminUserEntity;

public interface AdminUserRepository extends JpaRepository<AdminUserEntity, String> {
    AdminUserEntity findByEmail(String email);
}