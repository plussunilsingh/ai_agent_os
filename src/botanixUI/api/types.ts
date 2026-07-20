/**
 * types.ts
 *
 * This file defines the TypeScript interfaces for domain entities and ApiResponse envelopes.
 */

// Import necessary packages
import { ApiProperty } from '@nestjs/swagger';

// Define ApiResponse envelope interface
export interface ApiResponse<T> {
    code: number;
    message: string;
    data?: T | null;
}

/**
 * Domain entity interfaces
 */

// User Entity
export interface UserEntity {
    id: number;
    username: string;
    email: string;
    passwordHash: string; // This should be a hashed password, not plain text.
    createdAt: Date;
    updatedAt: Date;
}

// Product Entity
export interface ProductEntity {
    id: number;
    name: string;
    description: string;
    price: number;
    stockQuantity: number;
    imageUrl?: string | null;
    category: string;
    createdAt: Date;
    updatedAt: Date;
}

// Order Entity
export interface OrderEntity {
    id: number;
    userId: number;
    status: 'pending' | 'completed' | 'cancelled';
    totalAmount: number;
    orderDate: Date;
    deliveryAddress: string;
}

// Cart Entity
export interface CartEntity {
    id: number;
    productId: number;
    quantity: number;
    createdAt: Date;
    updatedAt: Date;
}

// OrderItem Entity
export interface OrderItemEntity {
    orderId: number;
    productId: number;
    quantity: number;
    pricePerUnit: number;
    totalAmount: number;
}

/**
 * ApiResponse Envelopes for each entity
 */

// User ApiResponse envelope
export interface UserApiResponse extends ApiResponse<UserEntity> {}

// Product ApiResponse envelope
export interface ProductApiResponse extends ApiResponse<ProductEntity> {}

// Order ApiResponse envelope
export interface OrderApiResponse extends ApiResponse<OrderEntity> {}

// Cart ApiResponse envelope
export interface CartApiResponse extends ApiResponse<CartEntity> {}

// OrderItem ApiResponse envelope
export interface OrderItemApiResponse extends ApiResponse<OrderItemEntity> {}

This code defines the necessary TypeScript interfaces for the entities and API responses in your BotanixUI domain. Each entity has a corresponding `ApiResponse` envelope to standardize the structure of responses returned from your API. This ensures consistency and clarity, which is crucial for maintaining a robust and maintainable codebase.