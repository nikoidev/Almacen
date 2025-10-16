import axiosInstance from '../axios'
import { 
  OutboundOrder, 
  OutboundOrderCreate, 
  OutboundOrderPick,
  PaginatedResponse 
} from '@/types'

export const ordersApi = {
  /**
   * Get all outbound orders with pagination and filters
   */
  getAll: async (params?: {
    page?: number
    limit?: number
    status?: string
    customer_name?: string
  }): Promise<PaginatedResponse<OutboundOrder>> => {
    const response = await axiosInstance.get('/api/orders/', { params })
    return response.data
  },

  /**
   * Get a single outbound order by ID
   */
  getById: async (id: number): Promise<OutboundOrder> => {
    const response = await axiosInstance.get(`/api/orders/${id}`)
    return response.data
  },

  /**
   * Create a new outbound order
   */
  create: async (data: OutboundOrderCreate): Promise<OutboundOrder> => {
    const response = await axiosInstance.post('/api/orders/', data)
    return response.data
  },

  /**
   * Update an existing outbound order (only if not shipped)
   */
  update: async (id: number, data: Partial<OutboundOrderCreate>): Promise<OutboundOrder> => {
    const response = await axiosInstance.put(`/api/orders/${id}`, data)
    return response.data
  },

  /**
   * Delete an outbound order (only if not shipped)
   */
  delete: async (id: number): Promise<void> => {
    await axiosInstance.delete(`/api/orders/${id}`)
  },

  /**
   * Pick items for an order and update inventory
   */
  pick: async (id: number, data: OutboundOrderPick): Promise<OutboundOrder> => {
    const response = await axiosInstance.post(`/api/orders/${id}/pick`, data)
    return response.data
  },

  /**
   * Mark an order as shipped
   */
  ship: async (id: number): Promise<OutboundOrder> => {
    const response = await axiosInstance.post(`/api/orders/${id}/ship`)
    return response.data
  },
}

