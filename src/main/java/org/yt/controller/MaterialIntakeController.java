package org.yt.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/admin")
public class MaterialIntakeController {

    @PostMapping("/materials/intake")
    public ResponseEntity<ApiResponse<Void>> intakeMaterial() {
        // Logic to handle material intake
        return ResponseEntity.ok(new ApiResponse<>(true, "Material intake registered successfully"));
    }

    @GetMapping("/materials/intake")
    public ResponseEntity<ApiResponse<String>> getMaterialsIntakeStatus() {
        // Logic to fetch the status of materials intake
        String status = "Current intake status";
        return ResponseEntity.ok(new ApiResponse<>(true, "Success", status));
    }
}

class ApiResponse<T> {
    private boolean success;
    private String message;
    private T data;

    public ApiResponse(boolean success, String message) {
        this.success = success;
        this.message = message;
    }

    public ApiResponse(boolean success, String message, T data) {
        this(success, message);
        this.data = data;
    }

    // Getters
    public boolean isSuccess() {
        return success;
    }

    public String getMessage() {
        return message;
    }

    public T getData() {
        return data;
    }
}