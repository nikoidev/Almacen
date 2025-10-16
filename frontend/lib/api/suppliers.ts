import axiosInstance from '../axios'
import { Supplier, SupplierCreate, SupplierUpdate, PaginatedResponse } from '@/types'

export const suppliersApi = {
  /**
   * Get all suppliers with pagination and filters
   */
  getAll: async (params?: {
    page?: number
    limit?: number
    search?: string
  }): Promise<PaginatedResponse<Supplier>> => {
    const response = await axiosInstance.get('/api/suppliers/', { params })
    return response.data
  },

  /**
   * Get a single supplier by ID
   */
  getById: async (id: number): Promise<Supplier> => {
    const response = await axiosInstance.get(`/api/suppliers/${id}`)
    return response.data
  },

  /**
   * Create a new supplier
   */
  create: async (data: SupplierCreate): Promise<Supplier> => {
    const response = await axiosInstance.post('/api/suppliers/', data)
    return response.data
  },

  /**
   * Update an existing supplier
   */
  update: async (id: number, data: SupplierUpdate): Promise<Supplier> => {
    const response = await axiosInstance.put(`/api/suppliers/${id}`, data)
    return response.data
  },

  /**
   * Delete a supplier
   */
  delete: async (id: number): Promise<void> => {
    await axiosInstance.delete(`/api/suppliers/${id}`)
  },
}

