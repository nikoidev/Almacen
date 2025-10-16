'use client'

import { useState, useEffect } from 'react'
import { inventoryApi } from '@/lib/api/inventory'
import { productsApi } from '@/lib/api/products'
import { locationsApi } from '@/lib/api/locations'
import { Inventory, Product, Location, InventoryAdjust, InventoryMove } from '@/types'
import toast from 'react-hot-toast'
import { ExclamationTriangleIcon, ArrowsRightLeftIcon, PlusMinusIcon } from '@heroicons/react/24/outline'

export default function InventoryPage() {
  const [inventory, setInventory] = useState<Inventory[]>([])
  const [lowStockProducts, setLowStockProducts] = useState<any[]>([])
  const [products, setProducts] = useState<Product[]>([])
  const [locations, setLocations] = useState<Location[]>([])
  const [loading, setLoading] = useState(true)
  const [showAdjustModal, setShowAdjustModal] = useState(false)
  const [showMoveModal, setShowMoveModal] = useState(false)
  const [adjustData, setAdjustData] = useState<InventoryAdjust>({
    product_id: 0,
    location_id: 0,
    quantity_change: 0,
    reason: '',
  })
  const [moveData, setMoveData] = useState<InventoryMove>({
    product_id: 0,
    from_location_id: 0,
    to_location_id: 0,
    quantity: 0,
  })

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      setLoading(true)
      const [invResponse, lowStock, prodsResponse, locsResponse] = await Promise.all([
        inventoryApi.getAll({}),
        inventoryApi.getLowStock(),
        productsApi.getAll({}),
        locationsApi.getAll({}),
      ])
      setInventory(invResponse.items)
      setLowStockProducts(lowStock)
      setProducts(prodsResponse.items)
      setLocations(locsResponse.items)
    } catch (error) {
      toast.error('Error al cargar datos')
    } finally {
      setLoading(false)
    }
  }

  const handleAdjust = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await inventoryApi.adjust(adjustData)
      toast.success('Ajuste realizado')
      setShowAdjustModal(false)
      fetchData()
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Error al ajustar')
    }
  }

  const handleMove = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await inventoryApi.move(moveData)
      toast.success('Stock movido')
      setShowMoveModal(false)
      fetchData()
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Error al mover')
    }
  }

  return (
    <div>
      <div className="mb-6 flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Inventario</h1>
        <div className="space-x-3">
          <button
            onClick={() => setShowAdjustModal(true)}
            className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            <PlusMinusIcon className="w-5 h-5 mr-2" />
            Ajustar Stock
          </button>
          <button
            onClick={() => setShowMoveModal(true)}
            className="inline-flex items-center px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
          >
            <ArrowsRightLeftIcon className="w-5 h-5 mr-2" />
            Mover Stock
          </button>
        </div>
      </div>

      {/* Low Stock Alerts */}
      {lowStockProducts.length > 0 && (
        <div className="mb-6 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-700 rounded-lg p-4">
          <div className="flex items-center mb-2">
            <ExclamationTriangleIcon className="w-5 h-5 text-yellow-600 dark:text-yellow-400 mr-2" />
            <h3 className="text-sm font-medium text-yellow-800 dark:text-yellow-200">
              Productos con Stock Bajo ({lowStockProducts.length})
            </h3>
          </div>
          <div className="text-sm text-yellow-700 dark:text-yellow-300 space-y-1">
            {lowStockProducts.slice(0, 3).map((p) => (
              <div key={p.product_id}>
                • {p.name} ({p.sku}): {p.current_stock} unidades (mín: {p.min_stock_level})
              </div>
            ))}
            {lowStockProducts.length > 3 && (
              <div className="text-xs">... y {lowStockProducts.length - 3} más</div>
            )}
          </div>
        </div>
      )}

      {/* Inventory Table */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
          <thead className="bg-gray-50 dark:bg-gray-900">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Producto</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Ubicación</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Cantidad</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Reservado</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Disponible</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
            {loading ? (
              <tr>
                <td colSpan={5} className="px-6 py-4 text-center text-gray-500">Cargando...</td>
              </tr>
            ) : inventory.length === 0 ? (
              <tr>
                <td colSpan={5} className="px-6 py-4 text-center text-gray-500">No hay inventario</td>
              </tr>
            ) : (
              inventory.map((inv) => (
                <tr key={inv.id} className="hover:bg-gray-50 dark:hover:bg-gray-700">
                  <td className="px-6 py-4 text-sm font-medium text-gray-900 dark:text-white">
                    {inv.product?.name || `Producto #${inv.product_id}`}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-500 dark:text-gray-400">
                    {inv.location?.code || `Ubicación #${inv.location_id}`}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-900 dark:text-white">{inv.quantity}</td>
                  <td className="px-6 py-4 text-sm text-yellow-600 dark:text-yellow-400">{inv.reserved_quantity}</td>
                  <td className="px-6 py-4 text-sm text-green-600 dark:text-green-400">
                    {inv.quantity - inv.reserved_quantity}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Adjust Modal */}
      {showAdjustModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white dark:bg-gray-800 rounded-lg p-6 w-full max-w-md">
            <h2 className="text-xl font-bold mb-4 text-gray-900 dark:text-white">Ajustar Stock</h2>
            <form onSubmit={handleAdjust} className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">Producto *</label>
                <select
                  required
                  value={adjustData.product_id}
                  onChange={(e) => setAdjustData({ ...adjustData, product_id: parseInt(e.target.value) })}
                  className="w-full px-3 py-2 border rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                >
                  <option value="">Seleccionar...</option>
                  {products.map((p) => (
                    <option key={p.id} value={p.id}>{p.name} ({p.sku})</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Ubicación *</label>
                <select
                  required
                  value={adjustData.location_id}
                  onChange={(e) => setAdjustData({ ...adjustData, location_id: parseInt(e.target.value) })}
                  className="w-full px-3 py-2 border rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                >
                  <option value="">Seleccionar...</option>
                  {locations.map((l) => (
                    <option key={l.id} value={l.id}>{l.code}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Cambio de Cantidad * (positivo o negativo)</label>
                <input
                  type="number"
                  required
                  value={adjustData.quantity_change}
                  onChange={(e) => setAdjustData({ ...adjustData, quantity_change: parseInt(e.target.value) })}
                  className="w-full px-3 py-2 border rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Razón *</label>
                <textarea
                  required
                  value={adjustData.reason}
                  onChange={(e) => setAdjustData({ ...adjustData, reason: e.target.value })}
                  rows={3}
                  className="w-full px-3 py-2 border rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                />
              </div>
              <div className="flex justify-end space-x-3">
                <button type="button" onClick={() => setShowAdjustModal(false)} className="px-4 py-2 border rounded-lg">
                  Cancelar
                </button>
                <button type="submit" className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
                  Ajustar
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Move Modal */}
      {showMoveModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white dark:bg-gray-800 rounded-lg p-6 w-full max-w-md">
            <h2 className="text-xl font-bold mb-4 text-gray-900 dark:text-white">Mover Stock</h2>
            <form onSubmit={handleMove} className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">Producto *</label>
                <select
                  required
                  value={moveData.product_id}
                  onChange={(e) => setMoveData({ ...moveData, product_id: parseInt(e.target.value) })}
                  className="w-full px-3 py-2 border rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                >
                  <option value="">Seleccionar...</option>
                  {products.map((p) => (
                    <option key={p.id} value={p.id}>{p.name} ({p.sku})</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Desde Ubicación *</label>
                <select
                  required
                  value={moveData.from_location_id}
                  onChange={(e) => setMoveData({ ...moveData, from_location_id: parseInt(e.target.value) })}
                  className="w-full px-3 py-2 border rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                >
                  <option value="">Seleccionar...</option>
                  {locations.map((l) => (
                    <option key={l.id} value={l.id}>{l.code}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Hacia Ubicación *</label>
                <select
                  required
                  value={moveData.to_location_id}
                  onChange={(e) => setMoveData({ ...moveData, to_location_id: parseInt(e.target.value) })}
                  className="w-full px-3 py-2 border rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                >
                  <option value="">Seleccionar...</option>
                  {locations.map((l) => (
                    <option key={l.id} value={l.id}>{l.code}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Cantidad *</label>
                <input
                  type="number"
                  required
                  min="1"
                  value={moveData.quantity}
                  onChange={(e) => setMoveData({ ...moveData, quantity: parseInt(e.target.value) })}
                  className="w-full px-3 py-2 border rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                />
              </div>
              <div className="flex justify-end space-x-3">
                <button type="button" onClick={() => setShowMoveModal(false)} className="px-4 py-2 border rounded-lg">
                  Cancelar
                </button>
                <button type="submit" className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700">
                  Mover
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}

