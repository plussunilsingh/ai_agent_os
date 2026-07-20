import axios from 'axios';
import { Logger } from './Logger'; // Assuming a Logger service is available

export class HttpClient {
    private static instance: HttpClient;
    private axiosInstance: any;

    private constructor() {
        this.axiosInstance = axios.create({
            baseURL: 'https://api.botanix.com', // Replace with actual base URL
            timeout: 30000, // Default timeout in milliseconds
            headers: {
                'Content-Type': 'application/json',
            },
        });

        this.injectBearerToken();
    }

    public static getInstance(): HttpClient {
        if (!HttpClient.instance) {
            HttpClient.instance = new HttpClient();
        }
        return HttpClient.instance;
    }

    private injectBearerToken() {
        const token = localStorage.getItem('botanix-token'); // Replace with actual storage mechanism
        if (token) {
            this.axiosInstance.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        }
    }

    public async get<T>(url: string, params?: any): Promise<T> {
        return this.executeRequest('GET', url, params);
    }

    public async post<T>(url: string, data?: any): Promise<T> {
        return this.executeRequest('POST', url, data);
    }

    public async put<T>(url: string, data?: any): Promise<T> {
        return this.executeRequest('PUT', url, data);
    }

    public async delete(url: string): Promise<void> {
        await this.executeRequest('DELETE', url);
    }

    private async executeRequest(method: string, url: string, data?: any): Promise<any> {
        const start = Date.now();

        try {
            let response;
            if (method === 'GET' || method === 'DELETE') {
                response = await this.axiosInstance.request({ method, url });
            } else {
                response = await this.axiosInstance.request({ method, url, data: JSON.stringify(data) });
            }

            const latency = Date.now() - start;
            if (latency < 20) {
                Logger.log(`HTTP ${method.toUpperCase()} request to ${url} completed in sub-20ms latency.`);
            } else {
                Logger.log(`HTTP ${method.toUpperCase()} request to ${url} took: ${latency} ms`);
            }

            return response.data;
        } catch (error) {
            const latency = Date.now() - start;
            Logger.error(`HTTP ${method.toUpperCase()} request to ${url} failed in ${latency} ms`, error);
            throw error;
        }
    }
}

### Explanation:
1. **Singleton Pattern**: The `HttpClient` class is designed as a singleton, ensuring that only one instance of the HTTP client exists throughout the application.
2. **Axios Configuration**: Axios is configured with a base URL and default headers.
3. **Bearer Token Injection**: The bearer token is injected into each request header if available in local storage (or any other mechanism).
4. **HTTP Methods**: `get`, `post`, `put`, and `delete` methods are provided to handle different HTTP operations.
5. **Latency Logging**: After the request, the latency is logged, with a special message for sub-20ms requests.
6. **Error Handling**: Errors are caught and logged appropriately.

This code can be further extended or modified based on specific requirements such as error handling strategies, additional headers, or more sophisticated logging mechanisms.