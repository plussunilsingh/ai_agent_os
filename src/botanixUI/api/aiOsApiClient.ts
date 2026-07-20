import axios from 'axios';
import { ITask } from '../models/ITask';
import { IOllamaStatusResponse } from '../models/OllamaStatusResponse';

const API_BASE_URL = 'https://api.ai-os.com/v1';

class AiOsApiClient {
    private static instance: AiOsApiClient;

    public static getInstance(): AiOsApiClient {
        if (!AiOsApiClient.instance) {
            AiOsApiClient.instance = new AiOsApiClient();
        }
        return AiOsApiClient.instance;
    }

    private constructor() {}

    /**
     * Fetches a list of tasks from the AI-SE OS API.
     * @returns A promise that resolves with an array of task objects.
     */
    public async getTasks(): Promise<ITask[]> {
        try {
            const response = await axios.get<ITask[]>(`${API_BASE_URL}/tasks`);
            return response.data;
        } catch (error) {
            throw new Error(`Failed to fetch tasks: ${error.message}`);
        }
    }

    /**
     * Fetches the status of the Ollama model from the AI-SE OS API.
     * @returns A promise that resolves with an object containing the Ollama status.
     */
    public async getOllamaStatus(): Promise<IOllamaStatusResponse> {
        try {
            const response = await axios.get<IOllamaStatusResponse>(`${API_BASE_URL}/ollama/status`);
            return response.data;
        } catch (error) {
            throw new Error(`Failed to fetch Ollama status: ${error.message}`);
        }
    }
}

export default AiOsApiClient.getInstance();

This TypeScript class `AiOsApiClient` provides a clean and efficient way to interact with the AI-SE OS API. It uses Axios for HTTP requests, ensures that only one instance of the client is created (using the Singleton pattern), and handles error messages gracefully.

### Explanation:
1. **Singleton Pattern**: Ensures that there's only one instance of `AiOsApiClient` throughout the application.
2. **API Base URL**: A constant for the base URL of the API, making it easy to update if needed.
3. **Error Handling**: Catches and throws errors with meaningful messages.
4. **Promises**: Returns promises from methods to handle asynchronous operations.

This code can be easily integrated into your TypeScript project and used to manage tasks and Ollama model status in a clean, production-ready manner.