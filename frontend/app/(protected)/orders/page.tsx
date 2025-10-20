'use client'

import { useState, useEffect } from 'react'
import { ordersApi } from '@/lib/api/orders'
import { productsApi } from '@/lib/api/products'
import { inventoryApi } from '@/lib/api/inventory'
import { OutboundOrder, Product, InventoryByProduct, OutboundOrderCreate, OutboundOrderPick } from '@/types'
import toast from 'react-hot-toast'
import { 
  PlusIcon, 
  EyeIcon, 
  TruckIcon,
  ClockIcon,
  CubeIcon,
  CheckIcon,
  XMarkIcon
} from '@heroicons/react/24/outline'

export default function OrdersPage() {
  const [orders, setOrders] = useState<OutboundOrder[]>([])
  const [products, setProducts] = useState<Product[]>([])
  const [loading, setLoading] = useState(true)
  const [showCreateModal, setShowCreateModal] = useState(false)
  const [showDetailModal, setShowDetailModal] = useState(false)
  const [showPickModal, setShowPickModal] = useState(false)
  const [selectedOrder, setSelectedOrder] = useState<OutboundOrder | null>(null)
  const [productInventory, setProductInventory] = useState<{[key: number]: InventoryByProduct}>({})

  // Create form state
  const [createForm, setCreateForm] = useState<{
    customer_name: string
    items: Array<{
      product_id: number | null
      quantity_ordered: number
    }>
  }>({
    customer_name: '',
    items: []
  })

  // Pick form state
  const [pickForm, setPickForm] = useState<{
    items: Array<{
      id: number
      quantity_picked: number
    }>
  }>({ items: [] })

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      setLoading(true)
      const [ordersRes, productsRes] = await Promise.all([
        ordersApi.getAll({}),
        productsApi.getAll({})
      ])
      setOrders(ordersRes.items)
      setProducts(productsRes.items)
    } catch (error) {
      toast.error('Error al cargar datos')
    } finally {
      setLoading(false)
    }
  }

  const fetchProductInventory = async (productId: number) => {
    try {
      const inventory = await inventoryApi.getByProduct(productId)
      setProductInventory(prev => ({ ...prev, [productId]: inventory }))
    } catch (error) {
      console.error(`Error al cargar inventario del producto ${productId}`)
    }
  }

  const handleCreateOrder = async () => {
    try {
      if (!createForm.customer_name || createForm.items.length === 0) {
        toast.error('Debes ingresar un cliente y agregar al menos un producto')
        return
      }

      const invalidItems = createForm.items.filter(
        item => !item.product_id || item.quantity_ordered <= 0
      )
      if (invalidItems.length > 0) {
        toast.error('Todos los productos deben tener cantidad válida')
        return
      }

      const data: OutboundOrderCreate = {
        customer_name: createForm.customer_name,
        items: createForm.items.map(item => ({
          product_id: item.product_id!,
          quantity_ordered: item.quantity_ordered
        }))
      }

      await ordersApi.create(data)
      toast.success('Pedido creado exitosamente')
      setShowCreateModal(false)
      resetCreateForm()
      fetchData()
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Error al crear pedido')
    }
  }

  const handlePickOrder = async () => {
    try {
      if (!selectedOrder) return

      const data: OutboundOrderPick = {
        items: pickForm.items
      }

      await ordersApi.pick(selectedOrder.id, data)
      toast.success('Picking realizado. Inventario actualizado.')
      setShowPickModal(false)
      setSelectedOrder(null)
      fetchData()
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Error al realizar picking')
    }
  }

  const handleShipOrder = async (orderId: number) => {
    try {
      await ordersApi.ship(orderId)
      toast.success('Pedido marcado como enviado')
      fetchData()
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Error al marcar como enviado')
    }
  }

  const openDetailModal = (order: OutboundOrder) => {
    setSelectedOrder(order)
    setShowDetailModal(true)
  }

  const openPickModal = async (order: OutboundOrder) => {
    setSelectedOrder(order)
    
    // Fetch inventory for all products in the order
    if (order.items) {
      for (const item of order.items) {
        await fetchProductInventory(item.product_id)
      }
    }

    setPickForm({
      items: order.items?.map(item => ({
        id: item.id,
        quantity_picked: item.quantity_ordered
      })) || []
    })
    setShowPickModal(true)
  }

  const resetCreateForm = () => {
    setCreateForm({
      customer_name: '',
      items: []
    })
  }

  const addProductToCreate = () => {
    setCreateForm({
      ...createForm,
      items: [
        ...createForm.items,
        { product_id: null, quantity_ordered: 1 }
      ]
    })
  }

  const removeProductFromCreate = (index: number) => {
    setCreateForm({
      ...createForm,
      items: createForm.items.filter((_, i) => i !== index)
    })
  }

  const updateCreateItem = (index: number, field: string, value: any) => {
    const newItems = [...createForm.items]
    newItems[index] = { ...newItems[index], [field]: value }
    setCreateForm({ ...createForm, items: newItems })
    
    // Fetch inventory when product is selected
    if (field === 'product_id' && value) {
      fetchProductInventory(Number(value))
    }
  }

  const updatePickItem = (itemId: number, quantity: number) => {
    setPickForm({
      items: pickForm.items.map(item =>
        item.id === itemId ? { ...item, quantity_picked: quantity } : item
      )
    })
  }

  const getStatusBadge = (status: string) => {
    const badges = {
      PENDING: {
        color: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200',
        icon: ClockIcon,
        text: 'Pendiente'
      },
      IN_PICKING: {
        color: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
        icon: CubeIcon,
        text: 'En Picking'
      },
      PACKED: {
        color: 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200',
        icon: CheckIcon,
        text: 'Empacado'
      },
      SHIPPED: {
        color: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
        icon: TruckIcon,
        text: 'Enviado'
      }
    }
    return badges[status as keyof typeof badges] || badges.PENDING
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Pedidos de Salida</h1>
          <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
            Gestiona los pedidos de salida a clientes
          </p>
        </div>
        <button
          onClick={() => setShowCreateModal(true)}
          className="flex items-center px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg transition-colors"
        >
          <PlusIcon className="w-5 h-5 mr-2" />
          Nuevo Pedido
        </button>
      </div>

      {loading ? (
        <div className="flex justify-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-600"></div>
        </div>
      ) : (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow overflow-hidden">
          <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
            <thead className="bg-gray-50 dark:bg-gray-900">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">ID</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Cliente</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Estado</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Fecha Creación</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Fecha Envío</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Acciones</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
              {orders.length === 0 ? (
                <tr>
                  <td colSpan={6} className="px-6 py-12 text-center text-gray-500">
                    No hay pedidos registrados
                  </td>
                </tr>
              ) : (
                orders.map((order) => {
                  const badge = getStatusBadge(order.status)
                  const BadgeIcon = badge.icon
                  return (
                    <tr key={order.id} className="hover:bg-gray-50 dark:hover:bg-gray-700">
                      <td className="px-6 py-4 text-sm font-medium text-gray-900 dark:text-white">
                        #{order.id}
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-900 dark:text-white">
                        {order.customer_name}
                      </td>
                      <td className="px-6 py-4">
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${badge.color}`}>
                          <BadgeIcon className="w-4 h-4 mr-1" />
                          {badge.text}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-500 dark:text-gray-400">
                        {new Date(order.created_at).toLocaleDateString()}
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-500 dark:text-gray-400">
                        {order.shipped_at ? new Date(order.shipped_at).toLocaleDateString() : '-'}
                      </td>
                      <td className="px-6 py-4 text-right text-sm space-x-2">
                        <button
                          onClick={() => openDetailModal(order)}
                          className="text-primary-600 hover:text-primary-900 dark:text-primary-400"
                          title="Ver detalle"
                        >
                          <EyeIcon className="w-5 h-5" />
                        </button>
                        {order.status === 'PENDING' && (
                          <button
                            onClick={() => openPickModal(order)}
                            className="text-blue-600 hover:text-blue-900 dark:text-blue-400"
                            title="Realizar picking"
                          >
                            <CubeIcon className="w-5 h-5" />
                          </button>
                        )}
                        {order.status === 'PACKED' && (
                          <button
                            onClick={() => handleShipOrder(order.id)}
                            className="text-green-600 hover:text-green-900 dark:text-green-400"
                            title="Marcar como enviado"
                          >
                            <TruckIcon className="w-5 h-5" />
                          </button>
                        )}
                      </td>
                    </tr>
                  )
                })
              )}
            </tbody>
          </table>
        </div>
      )}

      {/* Create Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white dark:bg-gray-800 rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-xl font-bold text-gray-900 dark:text-white">
                  Nuevo Pedido de Salida
                </h2>
                <button
                  onClick={() => {
                    setShowCreateModal(false)
                    resetCreateForm()
                  }}
                  className="text-gray-400 hover:text-gray-600"
                >
                  <XMarkIcon className="w-6 h-6" />
                </button>
              </div>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Nombre del Cliente *
                  </label>
                  <input
                    type="text"
                    value={createForm.customer_name}
                    onChange={(e) => setCreateForm({ ...createForm, customer_name: e.target.value })}
                    placeholder="Ej: Empresa ABC S.A."
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                    required
                  />
                </div>

                <div>
                  <div className="flex justify-between items-center mb-2">
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                      Productos *
                    </label>
                    <button
                      type="button"
                      onClick={addProductToCreate}
                      className="text-sm text-primary-600 hover:text-primary-700 dark:text-primary-400"
                    >
                      + Agregar Producto
                    </button>
                  </div>

                  {createForm.items.length === 0 ? (
                    <p className="text-sm text-gray-500 dark:text-gray-400 text-center py-4 border border-dashed border-gray-300 dark:border-gray-600 rounded-lg">
                      No hay productos agregados
                    </p>
                  ) : (
                    <div className="space-y-2">
                      {createForm.items.map((item, index) => {
                        const inventory = item.product_id ? productInventory[item.product_id] : null
                        const availableStock = inventory ? inventory.total_quantity - inventory.reserved_quantity : 0
                        
                        return (
                          <div key={index} className="space-y-1">
                            <div className="flex gap-2 items-end">
                              <div className="flex-1">
                                <select
                                  value={item.product_id || ''}
                                  onChange={(e) => updateCreateItem(index, 'product_id', Number(e.target.value))}
                                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white text-sm"
                                >
                                  <option value="">Seleccionar producto</option>
                                  {products.map(product => (
                                    <option key={product.id} value={product.id}>
                                      {product.sku} - {product.name}
                                    </option>
                                  ))}
                                </select>
                              </div>
                              <div className="w-32">
                                <input
                                  type="number"
                                  min="1"
                                  max={availableStock}
                                  value={item.quantity_ordered}
                                  onChange={(e) => updateCreateItem(index, 'quantity_ordered', Number(e.target.value))}
                                  placeholder="Cantidad"
                                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white text-sm"
                                />
                              </div>
                              <button
                                type="button"
                                onClick={() => removeProductFromCreate(index)}
                                className="p-2 text-red-600 hover:text-red-700 dark:text-red-400"
                              >
                                <XMarkIcon className="w-5 h-5" />
                              </button>
                            </div>
                            {item.product_id && inventory && (
                              <p className="text-xs text-gray-500 dark:text-gray-400 ml-1">
                                Stock disponible: {availableStock} unidades
                              </p>
                            )}
                          </div>
                        )
                      })}
                    </div>
                  )}
                </div>

                <div className="flex justify-end space-x-3 pt-4 border-t border-gray-200 dark:border-gray-700">
                  <button
                    onClick={() => {
                      setShowCreateModal(false)
                      resetCreateForm()
                    }}
                    className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700"
                  >
                    Cancelar
                  </button>
                  <button
                    onClick={handleCreateOrder}
                    className="px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg"
                  >
                    Crear Pedido
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Detail Modal */}
      {showDetailModal && selectedOrder && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white dark:bg-gray-800 rounded-lg max-w-3xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-xl font-bold text-gray-900 dark:text-white">
                  Detalle de Pedido #{selectedOrder.id}
                </h2>
                <button
                  onClick={() => setShowDetailModal(false)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  <XMarkIcon className="w-6 h-6" />
                </button>
              </div>

              <div className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="text-sm font-medium text-gray-500 dark:text-gray-400">Cliente</label>
                    <p className="text-gray-900 dark:text-white">{selectedOrder.customer_name}</p>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-500 dark:text-gray-400">Estado</label>
                    <div className="mt-1">
                      {(() => {
                        const badge = getStatusBadge(selectedOrder.status)
                        const BadgeIcon = badge.icon
                        return (
                          <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${badge.color}`}>
                            <BadgeIcon className="w-4 h-4 mr-1" />
                            {badge.text}
                          </span>
                        )
                      })()}
                    </div>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-500 dark:text-gray-400">Fecha Creación</label>
                    <p className="text-gray-900 dark:text-white">
                      {new Date(selectedOrder.created_at).toLocaleDateString()}
                    </p>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-500 dark:text-gray-400">Fecha Envío</label>
                    <p className="text-gray-900 dark:text-white">
                      {selectedOrder.shipped_at ? new Date(selectedOrder.shipped_at).toLocaleDateString() : '-'}
                    </p>
                  </div>
                </div>

                <div>
                  <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-3">Productos</h3>
                  <div className="bg-gray-50 dark:bg-gray-900 rounded-lg overflow-hidden">
                    <table className="min-w-full">
                      <thead className="bg-gray-100 dark:bg-gray-800">
                        <tr>
                          <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 dark:text-gray-400">Producto</th>
                          <th className="px-4 py-2 text-right text-xs font-medium text-gray-500 dark:text-gray-400">Solicitado</th>
                          <th className="px-4 py-2 text-right text-xs font-medium text-gray-500 dark:text-gray-400">Pickeado</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
                        {selectedOrder.items?.map((item) => (
                          <tr key={item.id}>
                            <td className="px-4 py-3 text-sm text-gray-900 dark:text-white">
                              {item.product?.name || `Producto #${item.product_id}`}
                            </td>
                            <td className="px-4 py-3 text-sm text-right text-gray-900 dark:text-white">
                              {item.quantity_ordered}
                            </td>
                            <td className="px-4 py-3 text-sm text-right text-gray-900 dark:text-white">
                              {item.quantity_picked || '-'}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>

                <div className="flex justify-end pt-4 border-t border-gray-200 dark:border-gray-700">
                  <button
                    onClick={() => setShowDetailModal(false)}
                    className="px-4 py-2 bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-white rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600"
                  >
                    Cerrar
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Pick Modal */}
      {showPickModal && selectedOrder && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white dark:bg-gray-800 rounded-lg max-w-3xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-xl font-bold text-gray-900 dark:text-white">
                  Realizar Picking - Pedido #{selectedOrder.id}
                </h2>
                <button
                  onClick={() => setShowPickModal(false)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  <XMarkIcon className="w-6 h-6" />
                </button>
              </div>

              <div className="mb-4 p-4 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-700 rounded-lg">
                <p className="text-sm text-blue-800 dark:text-blue-200">
                  Ingresa la cantidad recolectada para cada producto. El inventario se actualizará y el stock será removido.
                </p>
              </div>

              <div className="space-y-4">
                <div className="bg-gray-50 dark:bg-gray-900 rounded-lg overflow-hidden">
                  <table className="min-w-full">
                    <thead className="bg-gray-100 dark:bg-gray-800">
                      <tr>
                        <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 dark:text-gray-400">Producto</th>
                        <th className="px-4 py-2 text-right text-xs font-medium text-gray-500 dark:text-gray-400">Solicitado</th>
                        <th className="px-4 py-2 text-right text-xs font-medium text-gray-500 dark:text-gray-400">Disponible</th>
                        <th className="px-4 py-2 text-right text-xs font-medium text-gray-500 dark:text-gray-400">Pickeado</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
                      {selectedOrder.items?.map((item) => {
                        const pickItem = pickForm.items.find(pi => pi.id === item.id)
                        const inventory = productInventory[item.product_id]
                        const availableStock = inventory ? inventory.total_quantity - inventory.reserved_quantity : 0
                        
                        return (
                          <tr key={item.id}>
                            <td className="px-4 py-3 text-sm text-gray-900 dark:text-white">
                              {item.product?.name || `Producto #${item.product_id}`}
                            </td>
                            <td className="px-4 py-3 text-sm text-right text-gray-900 dark:text-white">
                              {item.quantity_ordered}
                            </td>
                            <td className="px-4 py-3 text-sm text-right text-gray-500 dark:text-gray-400">
                              {availableStock}
                            </td>
                            <td className="px-4 py-3 text-right">
                              <input
                                type="number"
                                min="0"
                                max={Math.min(item.quantity_ordered, availableStock)}
                                value={pickItem?.quantity_picked || 0}
                                onChange={(e) => updatePickItem(item.id, Number(e.target.value))}
                                className="w-24 px-3 py-1 border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-white text-sm text-right"
                              />
                            </td>
                          </tr>
                        )
                      })}
                    </tbody>
                  </table>
                </div>

                <div className="flex justify-end space-x-3 pt-4 border-t border-gray-200 dark:border-gray-700">
                  <button
                    onClick={() => setShowPickModal(false)}
                    className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700"
                  >
                    Cancelar
                  </button>
                  <button
                    onClick={handlePickOrder}
                    className="flex items-center px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg"
                  >
                    <CubeIcon className="w-5 h-5 mr-2" />
                    Confirmar Picking
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
