import axiosInstance from '../axios'
import { DashboardSummary } from '@/types'

export const dashboardApi = {
  /**
   * Get complete dashboard summary with all metrics and analytics
   */
  getSummary: async (): Promise<DashboardSummary> => {
    const response = await axiosInstance.get('/api/dashboard/summary')
    return response.data
  },
}

