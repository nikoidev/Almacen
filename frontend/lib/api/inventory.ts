import axiosInstance from '../axios'
import { 
  Inventory, 
  InventoryAdjust, 
  InventoryMove, 
  InventoryByProduct,
  LowStockProduct,
  PaginatedResponse 
} from '@/types'

export const inventoryApi = {
  /**
   * Get all inventory entries with pagination and filters
   */
  getAll: async (params?: {
    page?: number
    limit?: number
    product_id?: number
    location_id?: number
  }): Promise<PaginatedResponse<Inventory>> => {
    const response = await axiosInstance.get('/api/inventory/', { params })
    return response.data
  },

  /**
   * Get inventory for a specific product across all locations
   */
  getByProduct: async (productId: number): Promise<InventoryByProduct> => {
    const response = await axiosInstance.get(`/api/inventory/product/${productId}`)
    return response.data
  },

  /**
   * Get products with low stock (below minimum level)
   */
  getLowStock: async (): Promise<LowStockProduct[]> => {
    const response = await axiosInstance.get('/api/inventory/low-stock')
    return response.data
  },

  /**
   * Adjust inventory quantity (manual adjustment)
   */
  adjust: async (data: InventoryAdjust): Promise<Inventory> => {
    const response = await axiosInstance.post('/api/inventory/adjust', data)
    return response.data
  },

  /**
   * Move stock from one location to another
   */
  move: async (data: InventoryMove): Promise<void> => {
    await axiosInstance.post('/api/inventory/move', data)
  },
}

