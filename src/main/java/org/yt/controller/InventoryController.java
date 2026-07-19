package org.yt.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.Map;

@RestController
@RequestMapping("/api/admin")
public class InventoryController {

    // Mock service to handle inventory operations
    private final InventoryService inventoryService;

    public InventoryController(InventoryService inventoryService) {
        this.inventoryService = inventoryService;
    }

    @GetMapping("/inventory")
    public ResponseEntity<ApiResponse<Map<Long, Integer>>> getInventory() {
        Map<Long, Integer> inventoryData = inventoryService.getInventory();
        return ResponseEntity.ok(new ApiResponse<>(true, "Inventory fetched successfully", inventoryData));
    }

    @PutMapping("/inventory/{itemId}")
    public ResponseEntity<ApiResponse<Integer>> updateInventory(
            @PathVariable Long itemId,
            @RequestParam int quantity
    ) {
        boolean updated = inventoryService.updateInventory(itemId, quantity);
        return updated ? 
               ResponseEntity.ok(new ApiResponse<>(true, "Inventory updated successfully", quantity)) : 
               ResponseEntity.notFound().build();
    }

    // Simple API Response class
    public static class ApiResponse<T> {
        private boolean success;
        private String message;
        private T data;

        public ApiResponse(boolean success, String message, T data) {
            this.success = success;
            this.message = message;
            this.data = data;
        }

        // Getters for ApiResponse fields
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
}

This code defines a `InventoryController` class with two endpoints: one for getting the inventory status and another for updating an item's quantity. The service is assumed to be provided via dependency injection, and a simple `ApiResponse<T>` class is used to encapsulate response details.