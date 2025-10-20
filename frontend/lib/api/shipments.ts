import axiosInstance from '../axios'
import { 
  InboundShipment, 
  InboundShipmentCreate, 
  InboundShipmentReceive,
  PaginatedResponse 
} from '@/types'

export const shipmentsApi = {
  /**
   * Get all inbound shipments with pagination and filters
   */
  getAll: async (params?: {
    page?: number
    limit?: number
    status?: string
    supplier_id?: number
  }): Promise<PaginatedResponse<InboundShipment>> => {
    const response = await axiosInstance.get('/api/shipments/', { params })
    return response.data
  },

  /**
   * Get a single inbound shipment by ID
   */
  getById: async (id: number): Promise<InboundShipment> => {
    const response = await axiosInstance.get(`/api/shipments/${id}`)
    return response.data
  },

  /**
   * Create a new inbound shipment
   */
  create: async (data: InboundShipmentCreate): Promise<InboundShipment> => {
    const response = await axiosInstance.post('/api/shipments/', data)
    return response.data
  },

  /**
   * Update an existing inbound shipment (only if not completed)
   */
  update: async (id: number, data: Partial<InboundShipmentCreate>): Promise<InboundShipment> => {
    const response = await axiosInstance.put(`/api/shipments/${id}`, data)
    return response.data
  },

  /**
   * Delete an inbound shipment (only if not completed)
   */
  delete: async (id: number): Promise<void> => {
    await axiosInstance.delete(`/api/shipments/${id}`)
  },

  /**
   * Receive a shipment and update inventory
   */
  receive: async (id: number, data: InboundShipmentReceive): Promise<InboundShipment> => {
    const response = await axiosInstance.post(`/api/shipments/${id}/receive`, data)
    return response.data
  },
}

