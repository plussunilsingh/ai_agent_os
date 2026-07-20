// dispatchApiClient.ts

import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { map, catchError } from 'rxjs/operators';

import { SalesOrderFulfillment } from '../models/sales-order-fulfillment.model';
import { ApiResponse } from '../models/api-response.model';

@Injectable({
  providedIn: 'root'
})
export class DispatchApiClient {
  private apiUrl = 'https://api.botanix.com/dispatch/v1'; // Replace with actual API URL

  constructor(private http: HttpClient) {}

  /**
   * Fetches sales order fulfillment details.
   * @param orderId The ID of the sales order to fetch.
   * @returns An Observable that emits a SalesOrderFulfillment model or an error.
   */
  getSalesOrderFulfillment(orderId: string): Observable<ApiResponse<SalesOrderFulfillment>> {
    const url = `${this.apiUrl}/orders/${orderId}`;

    return this.http.get<ApiResponse<SalesOrderFulfillment>>(url)
      .pipe(
        map(response => response),
        catchError(this.handleError)
      );
  }

  /**
   * Updates the status of a sales order fulfillment.
   * @param orderId The ID of the sales order to update.
   * @param status The new status for the order.
   * @returns An Observable that emits a boolean indicating success or an error.
   */
  updateSalesOrderFulfillmentStatus(orderId: string, status: string): Observable<boolean> {
    const url = `${this.apiUrl}/orders/${orderId}/status`;
    const body = { status };

    return this.http.put<ApiResponse<boolean>>(url, body)
      .pipe(
        map(response => response.data),
        catchError(this.handleError)
      );
  }

  /**
   * Handles errors and returns a default error message.
   * @param error The caught error.
   * @returns An Observable that emits a default error message or the caught error.
   */
  private handleError(error: any): Observable<never> {
    console.error('An error occurred:', error);
    return of(false); // Return false to indicate failure
  }
}

### Explanation:
- **Imports**: The necessary Angular and RxJS imports are included for HTTP requests, observables, and error handling.
- **Service Class**: `DispatchApiClient` is defined with methods to fetch and update sales order fulfillment details.
- **API Methods**:
  - `getSalesOrderFulfillment`: Fetches the details of a specific sales order based on its ID.
  - `updateSalesOrderFulfillmentStatus`: Updates the status of a sales order.
- **Error Handling**: A private method, `handleError`, is used to handle HTTP errors and return a default error message.

### Notes:
- Replace the placeholder API URL (`https://api.botanix.com/dispatch/v1`) with your actual API endpoint.
- Ensure that the models (`SalesOrderFulfillment` and `ApiResponse`) are defined in the appropriate module or imported as needed.