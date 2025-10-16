'use client'

import { ReactNode } from 'react'
import Link from 'next/link'
import { usePathname, useRouter } from 'next/navigation'
import { useAuth } from '@/contexts/AuthContext'
import ThemeToggle from './ThemeToggle'
import {
  HomeIcon,
  UsersIcon,
  ShieldCheckIcon,
  KeyIcon,
  ArrowRightOnRectangleIcon,
  ClockIcon,
  UserCircleIcon,
  ChartBarIcon,
  CubeIcon,
  BuildingStorefrontIcon,
  MapPinIcon,
  ArchiveBoxIcon,
  ArrowDownTrayIcon,
  ArrowUpTrayIcon,
} from '@heroicons/react/24/outline'

interface LayoutProps {
  children: ReactNode
}

export default function Layout({ children }: LayoutProps) {
  const pathname = usePathname()
  const router = useRouter()
  const { user, logout } = useAuth()

  const handleLogout = () => {
    logout()
    router.push('/login')
  }

  // Navegación organizada por secciones
  const navigationSections = [
    {
      title: 'Dashboard',
      items: [
        { name: 'Inicio', href: '/dashboard', icon: ChartBarIcon },
      ]
    },
    {
      title: 'Gestión de Almacén',
      items: [
        { name: 'Inventario', href: '/inventory', icon: ArchiveBoxIcon },
        { name: 'Productos', href: '/products', icon: CubeIcon },
        { name: 'Proveedores', href: '/suppliers', icon: BuildingStorefrontIcon },
        { name: 'Ubicaciones', href: '/locations', icon: MapPinIcon },
        { name: 'Recepciones', href: '/shipments', icon: ArrowDownTrayIcon },
        { name: 'Pedidos', href: '/orders', icon: ArrowUpTrayIcon },
      ]
    },
    {
      title: 'Administración',
      items: [
        { name: 'Usuarios', href: '/users', icon: UsersIcon },
        { name: 'Roles', href: '/roles', icon: ShieldCheckIcon },
        { name: 'Permisos', href: '/permissions', icon: KeyIcon },
        { name: 'Actividad', href: '/audit-logs', icon: ClockIcon },
      ]
    }
  ]

  // Lista plana para encontrar el nombre de la página actual
  const allNavigationItems = navigationSections.flatMap(section => section.items)

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Sidebar */}
      <div className="fixed inset-y-0 left-0 w-64 bg-white dark:bg-gray-800 shadow-lg">
        <div className="flex flex-col h-full">
          {/* Logo */}
          <div className="flex items-center justify-between h-16 px-6 border-b border-gray-200 dark:border-gray-700">
            <div>
              <h1 className="text-xl font-bold text-gray-900 dark:text-white">
                SGA Pro
              </h1>
              <p className="text-xs text-gray-500 dark:text-gray-400">
                Sistema de Gestión de Almacenes
              </p>
            </div>
          </div>

          {/* Navigation */}
          <nav className="flex-1 px-4 py-6 space-y-6 overflow-y-auto">
            {navigationSections.map((section) => (
              <div key={section.title}>
                <h3 className="px-4 mb-2 text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  {section.title}
                </h3>
                <div className="space-y-1">
                  {section.items.map((item) => {
                    const isActive = pathname === item.href
                    return (
                      <Link
                        key={item.name}
                        href={item.href}
                        className={`flex items-center px-4 py-2.5 text-sm font-medium rounded-lg transition-colors ${
                          isActive
                            ? 'bg-primary-100 dark:bg-primary-900 text-primary-700 dark:text-primary-300'
                            : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
                        }`}
                      >
                        <item.icon className="w-5 h-5 mr-3" />
                        {item.name}
                      </Link>
                    )
                  })}
                </div>
              </div>
            ))}
          </nav>

          {/* User info and actions */}
          <div className="p-4 border-t border-gray-200 dark:border-gray-700">
            <div className="flex items-center justify-between mb-4">
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-900 dark:text-white truncate">
                  {user?.username}
                </p>
                <p className="text-xs text-gray-500 dark:text-gray-400 truncate">
                  {user?.email}
                </p>
              </div>
              <ThemeToggle />
            </div>
            <Link
              href="/profile"
              className="flex items-center w-full px-4 py-2 mb-2 text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
            >
              <UserCircleIcon className="w-5 h-5 mr-3" />
              Mi Perfil
            </Link>
            <button
              onClick={handleLogout}
              className="flex items-center w-full px-4 py-2 text-sm font-medium text-red-700 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-colors"
            >
              <ArrowRightOnRectangleIcon className="w-5 h-5 mr-3" />
              Cerrar Sesión
            </button>
          </div>
        </div>
      </div>

      {/* Main content */}
      <div className="pl-64">
        {/* Top bar */}
        <div className="sticky top-0 z-10 flex items-center justify-between h-16 px-8 bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
          <h2 className="text-2xl font-semibold text-gray-900 dark:text-white">
            {allNavigationItems.find((item) => item.href === pathname)?.name || 'Dashboard'}
          </h2>
          <ThemeToggle />
        </div>

        {/* Page content */}
        <main className="p-8">{children}</main>
      </div>
    </div>
  )
}
