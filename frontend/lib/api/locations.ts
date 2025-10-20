import axiosInstance from '../axios'
import { Location, LocationCreate, LocationUpdate, PaginatedResponse } from '@/types'

export const locationsApi = {
  /**
   * Get all locations with pagination and filters
   */
  getAll: async (params?: {
    page?: number
    limit?: number
    search?: string
  }): Promise<PaginatedResponse<Location>> => {
    const response = await axiosInstance.get('/api/locations/', { params })
    return response.data
  },

  /**
   * Get a single location by ID
   */
  getById: async (id: number): Promise<Location> => {
    const response = await axiosInstance.get(`/api/locations/${id}`)
    return response.data
  },

  /**
   * Create a new location
   */
  create: async (data: LocationCreate): Promise<Location> => {
    const response = await axiosInstance.post('/api/locations/', data)
    return response.data
  },

  /**
   * Update an existing location
   */
  update: async (id: number, data: LocationUpdate): Promise<Location> => {
    const response = await axiosInstance.put(`/api/locations/${id}`, data)
    return response.data
  },

  /**
   * Delete a location
   */
  delete: async (id: number): Promise<void> => {
    await axiosInstance.delete(`/api/locations/${id}`)
  },

  /**
   * Get available capacity for a location
   */
  getAvailableCapacity: async (id: number): Promise<{ available_capacity: number }> => {
    const response = await axiosInstance.get(`/api/locations/${id}/available-capacity`)
    return response.data
  },
}

