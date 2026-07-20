package com.example.domain.user.security.dto;

import lombok.Data;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;

/**
 * Data Transfer Object (DTO) used for updating a user's role.
 */
@Data
public class RoleUpdateDTO {

    /**
     * The unique identifier of the role being updated.
     */
    @NotNull(message = "Role ID cannot be null")
    private Long roleId;

    /**
     * The new name of the role. This field is optional and only needed if the role's name needs to be changed.
     */
    @NotBlank(message = "Role name cannot be blank", groups = UpdateRoleName.class)
    private String roleName;

    /**
     * A flag indicating whether this update should also cascade updates to related entities (e.g., users).
     * This field is optional and defaults to false if not provided.
     */
    private boolean cascadeUpdate;

    // Groups are used for validation conditional on certain criteria
    @interface UpdateRoleName {
    }
}

### Explanation:
- **Lombok**: The `@Data` annotation from Lombok automatically generates the necessary boilerplate code like getters, setters, and constructor.
- **Validation Annotations**:
  - `@NotNull`: Ensures that the role ID is not null.
  - `@NotBlank`: Ensures that the role name is not blank when updating the role's name. This group annotation (`UpdateRoleName`) can be used to conditionally apply this validation.
- **Cascading Update Flag**: A boolean field to indicate if related entities should also be updated.

### Usage Example:
When using this DTO, you would typically validate it based on whether you are updating just the role or if you need to update associated users as well:

RoleUpdateDTO roleUpdateDTO = new RoleUpdateDTO();
roleUpdateDTO.setRoleId(1L);
roleUpdateDTO.setRoleName("Manager");
roleUpdateDTO.setCascadeUpdate(true);

// Validate and process DTO
if (validator.validate(roleUpdateDTO, UpdateRoleName.class)) {
    // Proceed with updating the role and possibly cascading updates to users.
} else {
    // Handle validation errors
}

This setup ensures that your DTO is both clean and robust for use in a production environment.