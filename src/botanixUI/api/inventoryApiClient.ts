// inventoryApiClient.ts

import axios, { AxiosResponse } from 'axios';
import { InventoryItem, StockLocation } from '../models/inventoryModels';

const inventoryApiUrl = 'https://api.botanix.com/inventory'; // Replace with actual API URL

class InventoryApiClient {
    private static instance: InventoryApiClient;

    public static getInstance(): InventoryApiClient {
        if (!this.instance) {
            this.instance = new InventoryApiClient();
        }
        return this.instance;
    }

    private constructor() {}

    /**
     * Fetches all inventory items from the API.
     */
    public async getInventoryItems(): Promise<InventoryItem[]> {
        try {
            const response: AxiosResponse = await axios.get<InventoryItem[]>(`${inventoryApiUrl}/items`);
            return response.data;
        } catch (error) {
            throw new Error(`Failed to fetch inventory items: ${error.message}`);
        }
    }

    /**
     * Fetches stock locations for a given item.
     * @param itemId The ID of the item to fetch stock locations for.
     */
    public async getStockLocations(itemId: number): Promise<StockLocation[]> {
        try {
            const response: AxiosResponse = await axios.get<StockLocation[]>(`${inventoryApiUrl}/items/${itemId}/locations`);
            return response.data;
        } catch (error) {
            throw new Error(`Failed to fetch stock locations for item ${itemId}: ${error.message}`);
        }
    }

    /**
     * Updates the quantity of an inventory item at a specific location.
     * @param itemId The ID of the item to update.
     * @param locationId The ID of the location where the item is stored.
     * @param newQuantity The new quantity to set for the item at the specified location.
     */
    public async updateItemQuantity(itemId: number, locationId: number, newQuantity: number): Promise<void> {
        try {
            await axios.put(`${inventoryApiUrl}/items/${itemId}/locations/${locationId}`, { quantity: newQuantity });
        } catch (error) {
            throw new Error(`Failed to update item quantity: ${error.message}`);
        }
    }

    /**
     * Adds a new stock location for an inventory item.
     * @param itemId The ID of the item to add a location for.
     * @param locationId The ID of the new location to add.
     */
    public async addItemLocation(itemId: number, locationId: number): Promise<void> {
        try {
            await axios.post(`${inventoryApiUrl}/items/${itemId}/locations`, { location_id: locationId });
        } catch (error) {
            throw new Error(`Failed to add item location: ${error.message}`);
        }
    }

    /**
     * Deletes a stock location for an inventory item.
     * @param itemId The ID of the item to delete a location from.
     * @param locationId The ID of the location to delete.
     */
    public async deleteItemLocation(itemId: number, locationId: number): Promise<void> {
        try {
            await axios.delete(`${inventoryApiUrl}/items/${itemId}/locations/${locationId}`);
        } catch (error) {
            throw new Error(`Failed to delete item location: ${error.message}`);
        }
    }
}

export default InventoryApiClient.getInstance;

### Explanation:
1. **Singleton Pattern**: The `InventoryApiClient` class is designed as a singleton to ensure that only one instance of the API client exists, which helps in managing shared resources and avoiding multiple network requests.
2. **Error Handling**: Each method includes error handling to catch and throw meaningful errors if something goes wrong.
3. **Async/Await**: Promises are used with `async/await` for better readability and handling asynchronous operations.
4. **TypeScript Models**: The code assumes the existence of a separate file (`inventoryModels.ts`) that defines the necessary interfaces or classes like `InventoryItem` and `StockLocation`.

This setup ensures that the API client is robust, maintainable, and easy to use within your application.