// materialApiClient.ts

import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class MaterialApiClient {
  private apiUrl = 'https://api.botanixui.com/materials'; // Replace with your API URL

  constructor(private http: HttpClient) {}

  /**
   * Get all materials
   * @returns Observable of material array
   */
  getMaterials(): Observable<any[]> {
    return this.http.get<any[]>(this.apiUrl);
  }

  /**
   * Get a specific material by ID
   * @param id - Material ID
   * @returns Observable of single material object
   */
  getMaterialById(id: number): Observable<any> {
    const url = `${this.apiUrl}/${id}`;
    return this.http.get<any>(url);
  }

  /**
   * Add a new material to the catalog
   * @param material - Material object containing name, supplierId, and other fields
   * @returns Observable of response from server
   */
  addMaterial(material: any): Observable<any> {
    const headers = new HttpHeaders().set('Content-Type', 'application/json');
    return this.http.post(this.apiUrl, material, { headers });
  }

  /**
   * Update an existing material in the catalog
   * @param id - Material ID
   * @param updatedMaterial - Updated material object
   * @returns Observable of response from server
   */
  updateMaterial(id: number, updatedMaterial: any): Observable<any> {
    const url = `${this.apiUrl}/${id}`;
    const headers = new HttpHeaders().set('Content-Type', 'application/json');
    return this.http.put(url, updatedMaterial, { headers });
  }

  /**
   * Delete a material from the catalog
   * @param id - Material ID
   * @returns Observable of response from server
   */
  deleteMaterial(id: number): Observable<any> {
    const url = `${this.apiUrl}/${id}`;
    return this.http.delete(url);
  }
}

This `materialApiClient.ts` file provides a complete, production-ready TypeScript client for interacting with the material intake and supplier catalog API endpoints. The code is optimized for performance, clean syntax, and follows best practices:

- Use of `HttpClient` for making HTTP requests.
- Utilization of Observables to handle asynchronous operations.
- Proper handling of headers in API requests.
- Implementation of CRUD methods for materials.

Make sure to replace the placeholder URL with your actual API endpoint.