'use client'

import { useEffect, useState } from 'react'
import { dashboardApi } from '@/lib/api/dashboard'
import { DashboardSummary } from '@/types'
import { BarChart, Bar, PieChart, Pie, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell } from 'recharts'
import { CubeIcon, ArchiveBoxIcon, CurrencyDollarIcon, ExclamationTriangleIcon } from '@heroicons/react/24/outline'

export const dynamic = 'force-dynamic'

const COLORS = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#EC4899']

export default function DashboardPage() {
  const [summary, setSummary] = useState<DashboardSummary | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchSummary()
  }, [])

  const fetchSummary = async () => {
    try {
      setLoading(true)
      const data = await dashboardApi.getSummary()
      setSummary(data)
    } catch (error) {
      console.error('Failed to fetch dashboard:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-gray-500 dark:text-gray-400">Cargando dashboard...</div>
      </div>
    )
  }

  if (!summary) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-gray-500 dark:text-gray-400">No hay datos disponibles</div>
      </div>
    )
  }

  const kpis = [
    {
      title: 'Total Productos',
      value: summary.total_products,
      icon: CubeIcon,
      color: 'bg-blue-500',
    },
    {
      title: 'Unidades en Stock',
      value: summary.total_stock_units.toLocaleString(),
      icon: ArchiveBoxIcon,
      color: 'bg-green-500',
    },
    {
      title: 'Valor del Inventario',
      value: `$${summary.total_stock_value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`,
      icon: CurrencyDollarIcon,
      color: 'bg-purple-500',
    },
    {
      title: 'Productos Bajo Stock',
      value: summary.low_stock_products_count,
      icon: ExclamationTriangleIcon,
      color: 'bg-red-500',
    },
  ]

  return (
    <div className="space-y-6">
      {/* KPIs */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {kpis.map((kpi) => (
          <div key={kpi.title} className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-400">{kpi.title}</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white mt-1">{kpi.value}</p>
              </div>
              <div className={`${kpi.color} p-3 rounded-lg`}>
                <kpi.icon className="w-6 h-6 text-white" />
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Movimientos y Top Productos */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Movimientos últimos 30 días */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            Movimientos (Últimos 30 días)
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={summary.movements_last_30_days}>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
              <XAxis dataKey="date" stroke="#9CA3AF" tick={{ fontSize: 12 }} />
              <YAxis stroke="#9CA3AF" />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#1F2937',
                  border: 'none',
                  borderRadius: '8px',
                  color: '#F9FAFB',
                }}
              />
              <Legend />
              <Line type="monotone" dataKey="inbound" stroke="#10B981" name="Entradas" strokeWidth={2} />
              <Line type="monotone" dataKey="outbound" stroke="#EF4444" name="Salidas" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
          <div className="mt-4 flex justify-around text-sm">
            <div>
              <span className="text-gray-600 dark:text-gray-400">Total Entradas: </span>
              <span className="font-semibold text-green-600 dark:text-green-400">
                {summary.total_inbound_30_days}
              </span>
            </div>
            <div>
              <span className="text-gray-600 dark:text-gray-400">Total Salidas: </span>
              <span className="font-semibold text-red-600 dark:text-red-400">
                {summary.total_outbound_30_days}
              </span>
            </div>
          </div>
        </div>

        {/* Top 5 Productos */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            Top 5 Productos por Stock
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={summary.top_products_by_stock} layout="horizontal">
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
              <XAxis type="number" stroke="#9CA3AF" />
              <YAxis dataKey="name" type="category" width={100} stroke="#9CA3AF" tick={{ fontSize: 12 }} />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#1F2937',
                  border: 'none',
                  borderRadius: '8px',
                  color: '#F9FAFB',
                }}
              />
              <Bar dataKey="total_stock" fill="#3B82F6" name="Stock Total" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Stock por Categoría y Alertas */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Stock por Categoría */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            Distribución por Categoría
          </h3>
          {summary.stock_by_category.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={summary.stock_by_category}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ category, percent }) => `${category} (${(percent * 100).toFixed(0)}%)`}
                  outerRadius={100}
                  fill="#8884d8"
                  dataKey="total_units"
                >
                  {summary.stock_by_category.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#1F2937',
                    border: 'none',
                    borderRadius: '8px',
                    color: '#F9FAFB',
                  }}
                />
              </PieChart>
            </ResponsiveContainer>
          ) : (
            <div className="flex items-center justify-center h-[300px] text-gray-500 dark:text-gray-400">
              No hay datos de categorías
            </div>
          )}
        </div>

        {/* Alertas de Bajo Stock */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            Alertas de Bajo Stock
          </h3>
          {summary.low_stock_alerts.length > 0 ? (
            <div className="space-y-3 max-h-[300px] overflow-y-auto">
              {summary.low_stock_alerts.map((alert) => (
                <div
                  key={alert.product_id}
                  className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-3"
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <p className="text-sm font-medium text-gray-900 dark:text-white">
                        {alert.name}
                      </p>
                      <p className="text-xs text-gray-600 dark:text-gray-400">SKU: {alert.sku}</p>
                    </div>
                    <div className="text-right">
                      <p className="text-sm font-semibold text-red-600 dark:text-red-400">
                        {alert.current_stock} / {alert.min_stock_level}
                      </p>
                      <p className="text-xs text-red-600 dark:text-red-400">
                        Falta: {alert.difference}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="flex items-center justify-center h-[300px] text-gray-500 dark:text-gray-400">
              <div className="text-center">
                <ExclamationTriangleIcon className="w-12 h-12 mx-auto mb-2 text-green-500" />
                <p>No hay productos con bajo stock</p>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Utilización del Almacén */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
          Utilización del Almacén
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <p className="text-sm text-gray-600 dark:text-gray-400">Capacidad Total</p>
            <p className="text-xl font-bold text-gray-900 dark:text-white">
              {summary.warehouse_utilization.total_capacity.toLocaleString()} unidades
            </p>
          </div>
          <div>
            <p className="text-sm text-gray-600 dark:text-gray-400">Ocupado</p>
            <p className="text-xl font-bold text-blue-600 dark:text-blue-400">
              {summary.warehouse_utilization.occupied_units.toLocaleString()} unidades
            </p>
          </div>
          <div>
            <p className="text-sm text-gray-600 dark:text-gray-400">Disponible</p>
            <p className="text-xl font-bold text-green-600 dark:text-green-400">
              {summary.warehouse_utilization.available_capacity.toLocaleString()} unidades
            </p>
          </div>
          <div>
            <p className="text-sm text-gray-600 dark:text-gray-400">Utilización</p>
            <p className="text-xl font-bold text-purple-600 dark:text-purple-400">
              {summary.warehouse_utilization.utilization_percentage.toFixed(1)}%
            </p>
          </div>
        </div>
        <div className="mt-4">
          <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-4">
            <div
              className="bg-gradient-to-r from-blue-500 to-purple-600 h-4 rounded-full transition-all duration-500"
              style={{ width: `${summary.warehouse_utilization.utilization_percentage}%` }}
            />
          </div>
        </div>
      </div>
    </div>
  )
}
