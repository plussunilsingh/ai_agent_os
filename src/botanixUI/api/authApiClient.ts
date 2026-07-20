// authApiClient.ts

import axios from 'axios';
import { UserLoginResponse, UserRegistrationResponse } from './types';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:3000/api/auth';

class AuthApiClient {
    private axiosInstance = axios.create({
        baseURL: API_URL,
        headers: {
            'Content-Type': 'application/json',
        },
    });

    /**
     * Registers a new user.
     * @param username - The username of the new user.
     * @param email - The email address of the new user.
     * @param password - The password of the new user.
     * @returns A promise that resolves with the registration response.
     */
    async register(username: string, email: string, password: string): Promise<UserRegistrationResponse> {
        const response = await this.axiosInstance.post('/register', { username, email, password });
        return response.data;
    }

    /**
     * Logs in an existing user.
     * @param username - The username of the user to log in.
     * @param password - The password of the user to log in.
     * @returns A promise that resolves with the login response containing a JWT token.
     */
    async login(username: string, password: string): Promise<UserLoginResponse> {
        const response = await this.axiosInstance.post('/login', { username, password });
        return response.data;
    }

    /**
     * Logs out an existing user by revoking their session.
     * @returns A promise that resolves with the logout response.
     */
    async logout(): Promise<void> {
        await this.axiosInstance.post('/logout');
    }
}

export default new AuthApiClient();

### Explanation:
1. **Dependencies**: The `axios` library is used for HTTP requests, and custom types are defined in a separate file (`authApiClient.types.ts`) or included where needed.
2. **Environment Variable**: The base URL of the API is set using an environment variable to allow easy deployment across different environments (e.g., development, staging, production).
3. **Axios Configuration**: An Axios instance is created with a custom base URL and headers.
4. **Register Method**: A method to register a new user with username, email, and password.
5. **Login Method**: A method to log in an existing user with username and password, returning the JWT token upon successful authentication.
6. **Logout Method**: A method to log out a user by revoking their session.

### Types
You should define the `UserRegistrationResponse` and `UserLoginResponse` types as follows:

// authApiClient.types.ts

export interface UserRegistrationResponse {
    id: string;
    username: string;
    email: string;
    token: string; // Assuming a JWT token is returned
}

export interface UserLoginResponse {
    id: string;
    username: string;
    email: string;
    token: string; // Assuming a JWT token is returned
}

This setup ensures that the API client is robust, maintainable, and easy to use within your application.