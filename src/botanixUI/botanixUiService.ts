// src/botanixUiService.ts

import axios from 'axios';

interface User {
    id: string;
    username: string;
    email: string;
}

class BotanixUiService {
    private static instance: BotanixUiService;

    private constructor() {}

    public static getInstance(): BotanixUiService {
        if (!BotanixUiService.instance) {
            BotanixUiService.instance = new BotanixUiService();
        }
        return BotanixUiService.instance;
    }

    async fetchUsersFromJavaAdminApi(): Promise<User[]> {
        try {
            const response = await axios.get<User[]>('http://localhost:8080/api/admin/users');
            return response.data;
        } catch (error) {
            throw new Error(`Failed to fetch users from Java Admin API: ${error.message}`);
        }
    }

    async fetchUsersFromAISESOSApi(): Promise<User[]> {
        try {
            const response = await axios.get<User[]>('http://localhost:8000/api/v1/botanix');
            return response.data;
        } catch (error) {
            throw new Error(`Failed to fetch users from AI-SE OS API: ${error.message}`);
        }
    }
}

export default BotanixUiService.getInstance();