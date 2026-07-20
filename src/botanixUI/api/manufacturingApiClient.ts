// manufacturingApiClient.ts

import { Injectable } from '@nestjs/common';
import axios, { AxiosResponse } from 'axios';

@Injectable()
export class ManufacturingApiClient {
    private readonly apiUrl = 'https://api.botanix.com/v1';

    constructor(private readonly httpOptions: any) {}

    /**
     * Fetches work orders for a given status.
     * @param status The status of the work order to fetch.
     * @returns A promise that resolves with an array of work orders.
     */
    async getWorkOrdersByStatus(status: string): Promise<any[]> {
        const response = await this.httpGet(`/work-orders/${status}`);
        return response.data;
    }

    /**
     * Fetches telemetry data for a specific machine.
     * @param machineId The ID of the machine to fetch telemetry for.
     * @returns A promise that resolves with an array of telemetry entries.
     */
    async getMachineTelemetry(machineId: string): Promise<any[]> {
        const response = await this.httpGet(`/machines/${machineId}/telemetry`);
        return response.data;
    }

    /**
     * Sends a request to the server using HTTP GET method.
     * @param url The relative URL path for the API endpoint.
     * @returns A promise that resolves with the AxiosResponse object.
     */
    private httpGet(url: string): Promise<AxiosResponse> {
        return axios.get(`${this.apiUrl}/${url}`, this.httpOptions);
    }
}

This TypeScript file defines a `ManufacturingApiClient` class responsible for making API requests to fetch work orders and machine telemetry data. The client uses the Axios library for HTTP requests, which is widely used in Node.js applications due to its simplicity and effectiveness.

### Key Points:
1. **Service Injection**: The class injects an `httpOptions` object that can be used to configure Axios, such as setting headers or interceptors.
2. **Method Documentation**: Each public method includes a JSDoc comment with a brief description of what the method does, its parameters, and return type.
3. **Error Handling**: While basic error handling is not included here, in production code, you would want to handle errors more robustly by checking for HTTP status codes and providing meaningful error messages or rejections.

### Usage Example:
import { ManufacturingApiClient } from './manufacturingApiClient';

const options = {
    headers: {
        Authorization: `Bearer ${process.env.API_TOKEN}`
    }
};

const client = new ManufacturingApiClient(options);

async function main() {
    try {
        const workOrders = await client.getWorkOrdersByStatus('in-progress');
        console.log(workOrders);
        
        const telemetryData = await client.getMachineTelemetry('machine-123');
        console.log(telemetryData);
    } catch (error) {
        console.error(error);
    }
}

main();

This example demonstrates how to use the `ManufacturingApiClient` to fetch work orders and machine telemetry data.