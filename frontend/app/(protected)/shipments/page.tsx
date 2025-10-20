'use client'

import { useState, useEffect } from 'react'
import { shipmentsApi } from '@/lib/api/shipments'
import { suppliersApi } from '@/lib/api/suppliers'
import { productsApi } from '@/lib/api/products'
import { locationsApi } from '@/lib/api/locations'
import { InboundShipment, Supplier, Product, Location, InboundShipmentCreate, InboundShipmentReceive } from '@/types'
import toast from 'react-hot-toast'
import { 
  PlusIcon, 
  EyeIcon, 
  CheckCircleIcon, 
  XMarkIcon,
  TruckIcon,
  ClockIcon,
  CheckIcon
} from '@heroicons/react/24/outline'

export default function ShipmentsPage() {
  const [shipments, setShipments] = useState<InboundShipment[]>([])
  const [suppliers, setSuppliers] = useState<Supplier[]>([])
  const [products, setProducts] = useState<Product[]>([])
  const [locations, setLocations] = useState<Location[]>([])
  const [loading, setLoading] = useState(true)
  const [showCreateModal, setShowCreateModal] = useState(false)
  const [showDetailModal, setShowDetailModal] = useState(false)
  const [showReceiveModal, setShowReceiveModal] = useState(false)
  const [selectedShipment, setSelectedShipment] = useState<InboundShipment | null>(null)

  // Create form state
  const [createForm, setCreateForm] = useState<{
    supplier_id: number | null
    expected_at: string
    items: Array<{
      product_id: number | null
      quantity_expected: number
      location_id: number | null
    }>
  }>({
    supplier_id: null,
    expected_at: new Date().toISOString().split('T')[0],
    items: []
  })

  // Receive form state
  const [receiveForm, setReceiveForm] = useState<{
    items: Array<{
      id: number
      quantity_received: number
    }>
  }>({ items: [] })

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      setLoading(true)
      const [shipmentsRes, suppliersRes, productsRes, locationsRes] = await Promise.all([
        shipmentsApi.getAll({}),
        suppliersApi.getAll({}),
        productsApi.getAll({}),
        locationsApi.getAll({})
      ])
      setShipments(shipmentsRes.items)
      setSuppliers(suppliersRes.items)
      setProducts(productsRes.items)
      setLocations(locationsRes.items)
    } catch (error) {
      toast.error('Error al cargar datos')
    } finally {
      setLoading(false)
    }
  }

  const handleCreateShipment = async () => {
    try {
      if (!createForm.supplier_id || createForm.items.length === 0) {
        toast.error('Debes seleccionar un proveedor y agregar al menos un producto')
        return
      }

      const invalidItems = createForm.items.filter(
        item => !item.product_id || !item.location_id || item.quantity_expected <= 0
      )
      if (invalidItems.length > 0) {
        toast.error('Todos los productos deben tener cantidad y ubicación válidas')
        return
      }

      const data: InboundShipmentCreate = {
        supplier_id: createForm.supplier_id,
        expected_at: createForm.expected_at,
        items: createForm.items.map(item => ({
          product_id: item.product_id!,
          quantity_expected: item.quantity_expected,
          location_id: item.location_id!
        }))
      }

      await shipmentsApi.create(data)
      toast.success('Recepción creada exitosamente')
      setShowCreateModal(false)
      resetCreateForm()
      fetchData()
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Error al crear recepción')
    }
  }

  const handleReceiveShipment = async () => {
    try {
      if (!selectedShipment) return

      const data: InboundShipmentReceive = {
        items: receiveForm.items
      }

      await shipmentsApi.receive(selectedShipment.id, data)
      toast.success('Mercancía recibida y agregada al inventario')
      setShowReceiveModal(false)
      setSelectedShipment(null)
      fetchData()
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Error al recibir mercancía')
    }
  }

  const openDetailModal = (shipment: InboundShipment) => {
    setSelectedShipment(shipment)
    setShowDetailModal(true)
  }

  const openReceiveModal = (shipment: InboundShipment) => {
    setSelectedShipment(shipment)
    setReceiveForm({
      items: shipment.items?.map(item => ({
        id: item.id,
        quantity_received: item.quantity_expected
      })) || []
    })
    setShowReceiveModal(true)
  }

  const resetCreateForm = () => {
    setCreateForm({
      supplier_id: null,
      expected_at: new Date().toISOString().split('T')[0],
      items: []
    })
  }

  const addProductToCreate = () => {
    setCreateForm({
      ...createForm,
      items: [
        ...createForm.items,
        { product_id: null, quantity_expected: 1, location_id: null }
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
  }

  const updateReceiveItem = (itemId: number, quantity: number) => {
    setReceiveForm({
      items: receiveForm.items.map(item =>
        item.id === itemId ? { ...item, quantity_received: quantity } : item
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
      IN_PROCESS: {
        color: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
        icon: TruckIcon,
        text: 'En Proceso'
      },
      COMPLETED: {
        color: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
        icon: CheckCircleIcon,
        text: 'Completado'
      }
    }
    return badges[status as keyof typeof badges] || badges.PENDING
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Recepciones de Mercancía</h1>
          <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
            Gestiona las recepciones de productos de proveedores
          </p>
        </div>
        <button
          onClick={() => setShowCreateModal(true)}
          className="flex items-center px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg transition-colors"
        >
          <PlusIcon className="w-5 h-5 mr-2" />
          Nueva Recepción
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
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Proveedor</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Estado</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Fecha Esperada</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Fecha Recibida</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Acciones</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
              {shipments.length === 0 ? (
                <tr>
                  <td colSpan={6} className="px-6 py-12 text-center text-gray-500">
                    No hay recepciones registradas
                  </td>
                </tr>
              ) : (
                shipments.map((shipment) => {
                  const badge = getStatusBadge(shipment.status)
                  const BadgeIcon = badge.icon
                  return (
                    <tr key={shipment.id} className="hover:bg-gray-50 dark:hover:bg-gray-700">
                      <td className="px-6 py-4 text-sm font-medium text-gray-900 dark:text-white">
                        #{shipment.id}
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-900 dark:text-white">
                        {shipment.supplier?.name || `Proveedor #${shipment.supplier_id}`}
                      </td>
                      <td className="px-6 py-4">
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${badge.color}`}>
                          <BadgeIcon className="w-4 h-4 mr-1" />
                          {badge.text}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-500 dark:text-gray-400">
                        {new Date(shipment.expected_at).toLocaleDateString()}
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-500 dark:text-gray-400">
                        {shipment.received_at ? new Date(shipment.received_at).toLocaleDateString() : '-'}
                      </td>
                      <td className="px-6 py-4 text-right text-sm space-x-2">
                        <button
                          onClick={() => openDetailModal(shipment)}
                          className="text-primary-600 hover:text-primary-900 dark:text-primary-400"
                          title="Ver detalle"
                        >
                          <EyeIcon className="w-5 h-5" />
                        </button>
                        {shipment.status !== 'COMPLETED' && (
                          <button
                            onClick={() => openReceiveModal(shipment)}
                            className="text-green-600 hover:text-green-900 dark:text-green-400"
                            title="Recibir mercancía"
                          >
                            <CheckCircleIcon className="w-5 h-5" />
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
                  Nueva Recepción de Mercancía
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
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Proveedor *
                    </label>
                    <select
                      value={createForm.supplier_id || ''}
                      onChange={(e) => setCreateForm({ ...createForm, supplier_id: Number(e.target.value) })}
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                      required
                    >
                      <option value="">Seleccionar proveedor</option>
                      {suppliers.map(supplier => (
                        <option key={supplier.id} value={supplier.id}>{supplier.name}</option>
                      ))}
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Fecha Esperada *
                    </label>
                    <input
                      type="date"
                      value={createForm.expected_at}
                      onChange={(e) => setCreateForm({ ...createForm, expected_at: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                      required
                    />
                  </div>
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
                      {createForm.items.map((item, index) => (
                        <div key={index} className="flex gap-2 items-end">
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
                              value={item.quantity_expected}
                              onChange={(e) => updateCreateItem(index, 'quantity_expected', Number(e.target.value))}
                              placeholder="Cantidad"
                              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white text-sm"
                            />
                          </div>
                          <div className="flex-1">
                            <select
                              value={item.location_id || ''}
                              onChange={(e) => updateCreateItem(index, 'location_id', Number(e.target.value))}
                              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white text-sm"
                            >
                              <option value="">Ubicación</option>
                              {locations.map(location => (
                                <option key={location.id} value={location.id}>
                                  {location.code}
                                </option>
                              ))}
                            </select>
                          </div>
                          <button
                            type="button"
                            onClick={() => removeProductFromCreate(index)}
                            className="p-2 text-red-600 hover:text-red-700 dark:text-red-400"
                          >
                            <XMarkIcon className="w-5 h-5" />
                          </button>
                        </div>
                      ))}
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
                    onClick={handleCreateShipment}
                    className="px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg"
                  >
                    Crear Recepción
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Detail Modal */}
      {showDetailModal && selectedShipment && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white dark:bg-gray-800 rounded-lg max-w-3xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-xl font-bold text-gray-900 dark:text-white">
                  Detalle de Recepción #{selectedShipment.id}
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
                    <label className="text-sm font-medium text-gray-500 dark:text-gray-400">Proveedor</label>
                    <p className="text-gray-900 dark:text-white">
                      {selectedShipment.supplier?.name || `Proveedor #${selectedShipment.supplier_id}`}
                    </p>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-500 dark:text-gray-400">Estado</label>
                    <div className="mt-1">
                      {(() => {
                        const badge = getStatusBadge(selectedShipment.status)
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
                    <label className="text-sm font-medium text-gray-500 dark:text-gray-400">Fecha Esperada</label>
                    <p className="text-gray-900 dark:text-white">
                      {new Date(selectedShipment.expected_at).toLocaleDateString()}
                    </p>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-500 dark:text-gray-400">Fecha Recibida</label>
                    <p className="text-gray-900 dark:text-white">
                      {selectedShipment.received_at ? new Date(selectedShipment.received_at).toLocaleDateString() : '-'}
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
                          <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 dark:text-gray-400">Ubicación</th>
                          <th className="px-4 py-2 text-right text-xs font-medium text-gray-500 dark:text-gray-400">Esperado</th>
                          <th className="px-4 py-2 text-right text-xs font-medium text-gray-500 dark:text-gray-400">Recibido</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
                        {selectedShipment.items?.map((item) => (
                          <tr key={item.id}>
                            <td className="px-4 py-3 text-sm text-gray-900 dark:text-white">
                              {item.product?.name || `Producto #${item.product_id}`}
                            </td>
                            <td className="px-4 py-3 text-sm text-gray-500 dark:text-gray-400">
                              {item.location?.code || `Ubicación #${item.location_id}`}
                            </td>
                            <td className="px-4 py-3 text-sm text-right text-gray-900 dark:text-white">
                              {item.quantity_expected}
                            </td>
                            <td className="px-4 py-3 text-sm text-right text-gray-900 dark:text-white">
                              {item.quantity_received || '-'}
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

      {/* Receive Modal */}
      {showReceiveModal && selectedShipment && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white dark:bg-gray-800 rounded-lg max-w-3xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-xl font-bold text-gray-900 dark:text-white">
                  Recibir Mercancía - Recepción #{selectedShipment.id}
                </h2>
                <button
                  onClick={() => setShowReceiveModal(false)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  <XMarkIcon className="w-6 h-6" />
                </button>
              </div>

              <div className="mb-4 p-4 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-700 rounded-lg">
                <p className="text-sm text-blue-800 dark:text-blue-200">
                  Ingresa la cantidad recibida para cada producto. El inventario se actualizará automáticamente.
                </p>
              </div>

              <div className="space-y-4">
                <div className="bg-gray-50 dark:bg-gray-900 rounded-lg overflow-hidden">
                  <table className="min-w-full">
                    <thead className="bg-gray-100 dark:bg-gray-800">
                      <tr>
                        <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 dark:text-gray-400">Producto</th>
                        <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 dark:text-gray-400">Ubicación</th>
                        <th className="px-4 py-2 text-right text-xs font-medium text-gray-500 dark:text-gray-400">Esperado</th>
                        <th className="px-4 py-2 text-right text-xs font-medium text-gray-500 dark:text-gray-400">Recibido</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
                      {selectedShipment.items?.map((item) => {
                        const receiveItem = receiveForm.items.find(ri => ri.id === item.id)
                        return (
                          <tr key={item.id}>
                            <td className="px-4 py-3 text-sm text-gray-900 dark:text-white">
                              {item.product?.name || `Producto #${item.product_id}`}
                            </td>
                            <td className="px-4 py-3 text-sm text-gray-500 dark:text-gray-400">
                              {item.location?.code || `Ubicación #${item.location_id}`}
                            </td>
                            <td className="px-4 py-3 text-sm text-right text-gray-900 dark:text-white">
                              {item.quantity_expected}
                            </td>
                            <td className="px-4 py-3 text-right">
                              <input
                                type="number"
                                min="0"
                                max={item.quantity_expected}
                                value={receiveItem?.quantity_received || 0}
                                onChange={(e) => updateReceiveItem(item.id, Number(e.target.value))}
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
                    onClick={() => setShowReceiveModal(false)}
                    className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700"
                  >
                    Cancelar
                  </button>
                  <button
                    onClick={handleReceiveShipment}
                    className="flex items-center px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg"
                  >
                    <CheckIcon className="w-5 h-5 mr-2" />
                    Recibir Mercancía
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
