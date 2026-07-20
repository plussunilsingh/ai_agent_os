package com.example.domain.security;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.Table;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Entity
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Table(name = "security_roles")
public class RoleEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String roleName;

    private boolean enabled;

    // Getters and Setters

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getRoleName() {
        return roleName;
    }

    public void setRoleName(String roleName) {
        this.roleName = roleName;
    }

    public boolean isEnabled() {
        return enabled;
    }

    public void setEnabled(boolean enabled) {
        this.enabled = enabled;
    }
}

This code defines a `RoleEntity` class mapped to the `security_roles` table in a database. The entity uses JPA annotations for mapping and includes Lombok annotations to simplify the boilerplate code. The class is designed to be production-ready, with proper encapsulation and default constructors where necessary.

### Explanation:
- **@Entity**: Marks this class as a JPA entity.
- **@Data**: Provides `toString()`, `equals()`, `hashCode()`, and all getters & setters for the fields.
- **@NoArgsConstructor** and **@AllArgsConstructor**: Generate no-arg and fully parameterized constructors, respectively.
- **@Builder**: Generates builder methods to create instances of this class in a fluent manner.
- **@Table(name = "security_roles")**: Maps the entity to the `security_roles` table.

### Usage:
This entity can be used in various parts of your application where you need to represent or manipulate role data, such as security checks, user roles management, etc.