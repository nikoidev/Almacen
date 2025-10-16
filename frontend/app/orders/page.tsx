'use client'

import { useState, useEffect } from 'react'
import { ordersApi } from '@/lib/api/orders'
import { OutboundOrder } from '@/types'
import toast from 'react-hot-toast'
import { TruckIcon, ClockIcon } from '@heroicons/react/24/outline'

export default function OrdersPage() {
  const [orders, setOrders] = useState<OutboundOrder[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchOrders()
  }, [])

  const fetchOrders = async () => {
    try {
      setLoading(true)
      const response = await ordersApi.getAll({})
      setOrders(response.items)
    } catch (error) {
      toast.error('Error al cargar pedidos')
    } finally {
      setLoading(false)
    }
  }

  const getStatusBadge = (status: string) => {
    const colors = {
      PENDING: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200',
      IN_PICKING: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
      PACKED: 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200',
      SHIPPED: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
    }
    return colors[status as keyof typeof colors] || colors.PENDING
  }

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Pedidos de Salida</h1>
        <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
          Gestiona los pedidos de salida a clientes
        </p>
      </div>

      <div className="bg-white dark:bg-gray-800 rounded-lg shadow overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
          <thead className="bg-gray-50 dark:bg-gray-900">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">ID</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Cliente</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Estado</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Fecha Creación</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Fecha Envío</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
            {loading ? (
              <tr>
                <td colSpan={5} className="px-6 py-4 text-center text-gray-500">Cargando...</td>
              </tr>
            ) : orders.length === 0 ? (
              <tr>
                <td colSpan={5} className="px-6 py-4 text-center text-gray-500">No hay pedidos</td>
              </tr>
            ) : (
              orders.map((order) => (
                <tr key={order.id} className="hover:bg-gray-50 dark:hover:bg-gray-700">
                  <td className="px-6 py-4 text-sm font-medium text-gray-900 dark:text-white">#{order.id}</td>
                  <td className="px-6 py-4 text-sm text-gray-900 dark:text-white">{order.customer_name}</td>
                  <td className="px-6 py-4">
                    <span className={`px-2 py-1 text-xs font-semibold rounded-full ${getStatusBadge(order.status)}`}>
                      {order.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-500 dark:text-gray-400">
                    {new Date(order.created_at).toLocaleDateString()}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-500 dark:text-gray-400">
                    {order.shipped_at ? new Date(order.shipped_at).toLocaleDateString() : '-'}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      <div className="mt-6 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-700 rounded-lg p-4">
        <div className="flex items-start">
          <TruckIcon className="w-5 h-5 text-blue-600 dark:text-blue-400 mt-0.5 mr-3" />
          <div>
            <h3 className="text-sm font-medium text-blue-800 dark:text-blue-200">Funcionalidad completa en desarrollo</h3>
            <p className="mt-1 text-sm text-blue-700 dark:text-blue-300">
              La creación y procesamiento de pedidos (picking y envío) estará disponible próximamente.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

