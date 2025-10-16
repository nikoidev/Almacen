import axiosInstance from '../axios'
import { Product, ProductCreate, ProductUpdate, PaginatedResponse } from '@/types'

export const productsApi = {
  /**
   * Get all products with pagination and filters
   */
  getAll: async (params?: {
    page?: number
    limit?: number
    search?: string
    category?: string
  }): Promise<PaginatedResponse<Product>> => {
    const response = await axiosInstance.get('/api/products/', { params })
    return response.data
  },

  /**
   * Get a single product by ID
   */
  getById: async (id: number): Promise<Product> => {
    const response = await axiosInstance.get(`/api/products/${id}`)
    return response.data
  },

  /**
   * Create a new product
   */
  create: async (data: ProductCreate): Promise<Product> => {
    const response = await axiosInstance.post('/api/products/', data)
    return response.data
  },

  /**
   * Update an existing product
   */
  update: async (id: number, data: ProductUpdate): Promise<Product> => {
    const response = await axiosInstance.put(`/api/products/${id}`, data)
    return response.data
  },

  /**
   * Delete a product
   */
  delete: async (id: number): Promise<void> => {
    await axiosInstance.delete(`/api/products/${id}`)
  },

  /**
   * Get all available product categories
   */
  getCategories: async (): Promise<string[]> => {
    const response = await axiosInstance.get('/api/products/categories')
    return response.data
  },
}

