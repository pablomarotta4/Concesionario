import React, { useState, useEffect } from 'react';
import { 
  Plus, 
  Edit, 
  Trash2, 
  Eye, 
  Car, 
  Users, 
  Settings,
  Search,
  Filter,
  ChevronDown
} from 'lucide-react';
import { carsAPI } from '../services/api';
import { Car as CarType } from '../types';
import CarEditModal from '../components/CarEditModal';
import CarAddModal from '../components/CarAddModal';
import toast from 'react-hot-toast';

const Admin: React.FC = () => {
  const [cars, setCars] = useState<CarType[]>([]);
  const [filteredCars, setFilteredCars] = useState<CarType[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedStatus, setSelectedStatus] = useState('');
  const [showFilters, setShowFilters] = useState(false);
  const [editingCar, setEditingCar] = useState<CarType | null>(null);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [isAddModalOpen, setIsAddModalOpen] = useState(false);

  useEffect(() => {
    const fetchCars = async () => {
      try {
        const carsData = await carsAPI.getAllCars();
        setCars(carsData);
        setFilteredCars(carsData);
      } catch (error) {
        console.error('Error fetching cars:', error);
        toast.error('Error al cargar los vehículos');
      } finally {
        setIsLoading(false);
      }
    };

    fetchCars();
  }, []);

  useEffect(() => {
    let filtered = cars;

    // Search filter
    if (searchTerm) {
      filtered = filtered.filter(car =>
        car.brand.toLowerCase().includes(searchTerm.toLowerCase()) ||
        car.model.toLowerCase().includes(searchTerm.toLowerCase()) ||
        car.color.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    // Status filter
    if (selectedStatus) {
      filtered = filtered.filter(car => 
        selectedStatus === 'available' ? car.is_available : !car.is_available
      );
    }

    setFilteredCars(filtered);
  }, [cars, searchTerm, selectedStatus]);

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('es-ES', {
      style: 'currency',
      currency: 'USD',
    }).format(price);
  };

  const handleDeleteCar = async (carId: string) => {
    if (window.confirm('¿Estás seguro de que quieres eliminar este vehículo?')) {
      try {
        await carsAPI.deleteCar(carId);
        setCars(cars.filter(car => car.id !== carId));
        toast.success('Vehículo eliminado exitosamente');
      } catch (error) {
        console.error('Error deleting car:', error);
        toast.error('Error al eliminar el vehículo');
      }
    }
  };

  const clearFilters = () => {
    setSearchTerm('');
    setSelectedStatus('');
  };

  const handleEditCar = (car: CarType) => {
    setEditingCar(car);
    setIsEditModalOpen(true);
  };

  const handleCarUpdated = () => {
    // Refresh cars list
    const fetchCars = async () => {
      try {
        const carsData = await carsAPI.getAllCars();
        setCars(carsData);
        setFilteredCars(carsData);
      } catch (error) {
        console.error('Error fetching cars:', error);
        toast.error('Error al cargar los vehículos');
      }
    };
    fetchCars();
  };

  const closeEditModal = () => {
    setEditingCar(null);
    setIsEditModalOpen(false);
  };

  const openAddModal = () => {
    setIsAddModalOpen(true);
  };

  const closeAddModal = () => {
    setIsAddModalOpen(false);
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="animate-pulse">
            <div className="h-8 bg-gray-200 rounded w-1/4 mb-8"></div>
            <div className="bg-white rounded-lg shadow-sm p-6">
              <div className="space-y-4">
                {[...Array(5)].map((_, index) => (
                  <div key={index} className="h-16 bg-gray-200 rounded"></div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Panel de Administración
          </h1>
          <p className="text-gray-600">
            Gestiona vehículos, usuarios y configuraciones del sistema
          </p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="card">
            <div className="flex items-center">
              <div className="bg-primary-100 p-3 rounded-lg">
                <Car className="h-6 w-6 text-primary-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Total Vehículos</p>
                <p className="text-2xl font-bold text-gray-900">{cars.length}</p>
              </div>
            </div>
          </div>

          <div className="card">
            <div className="flex items-center">
              <div className="bg-green-100 p-3 rounded-lg">
                <Car className="h-6 w-6 text-green-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Disponibles</p>
                <p className="text-2xl font-bold text-gray-900">
                  {cars.filter(car => car.is_available).length}
                </p>
              </div>
            </div>
          </div>

          <div className="card">
            <div className="flex items-center">
              <div className="bg-red-100 p-3 rounded-lg">
                <Car className="h-6 w-6 text-red-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Vendidos</p>
                <p className="text-2xl font-bold text-gray-900">
                  {cars.filter(car => !car.is_available).length}
                </p>
              </div>
            </div>
          </div>

          <div className="card">
            <div className="flex items-center">
              <div className="bg-purple-100 p-3 rounded-lg">
                <Users className="h-6 w-6 text-purple-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Usuarios</p>
                <p className="text-2xl font-bold text-gray-900">25</p>
              </div>
            </div>
          </div>
        </div>

        {/* Cars Management */}
        <div className="card">
          <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6">
            <div>
              <h2 className="text-xl font-semibold text-gray-900 mb-1">
                Gestión de Vehículos
              </h2>
              <p className="text-gray-600">
                Administra el inventario de vehículos
              </p>
            </div>
            <button 
              onClick={openAddModal}
              className="btn-primary mt-4 sm:mt-0"
            >
              <Plus className="h-4 w-4 mr-2" />
              Agregar Vehículo
            </button>
          </div>

          {/* Search and Filters */}
          <div className="mb-6">
            <div className="flex flex-col lg:flex-row gap-4">
              <div className="flex-1">
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                  <input
                    type="text"
                    placeholder="Buscar vehículos..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="input-field pl-10"
                  />
                </div>
              </div>

              <button
                onClick={() => setShowFilters(!showFilters)}
                className="btn-secondary flex items-center"
              >
                <Filter className="h-4 w-4 mr-2" />
                Filtros
                <ChevronDown className={`h-4 w-4 ml-2 transition-transform ${
                  showFilters ? 'rotate-180' : ''
                }`} />
              </button>
            </div>

            {showFilters && (
              <div className="mt-4 pt-4 border-t border-gray-200">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div>
                    <label className="form-label">Estado</label>
                    <select
                      value={selectedStatus}
                      onChange={(e) => setSelectedStatus(e.target.value)}
                      className="input-field"
                    >
                      <option value="">Todos los estados</option>
                      <option value="available">Disponible</option>
                      <option value="sold">Vendido</option>
                    </select>
                  </div>

                  <div className="flex items-end">
                    <button
                      onClick={clearFilters}
                      className="btn-secondary w-full"
                    >
                      Limpiar Filtros
                    </button>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Cars Table */}
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Vehículo
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Precio
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Estado
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Kilometraje
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Acciones
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {filteredCars.map((car) => (
                  <tr key={car.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <div className="flex-shrink-0 h-10 w-10">
                          <img
                            className="h-10 w-10 rounded-lg object-cover"
                            src={car.image_url || '/placeholder-car.jpg'}
                            alt={`${car.brand} ${car.model}`}
                          />
                        </div>
                        <div className="ml-4">
                          <div className="text-sm font-medium text-gray-900">
                            {car.brand} {car.model}
                          </div>
                          <div className="text-sm text-gray-500">
                            {car.year} • {car.color}
                          </div>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-medium text-gray-900">
                        {formatPrice(car.price)}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                        car.is_available
                          ? 'bg-green-100 text-green-800'
                          : 'bg-red-100 text-red-800'
                      }`}>
                        {car.is_available ? 'Disponible' : 'Vendido'}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {car.mileage.toLocaleString()} km
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <div className="flex space-x-2">
                        <button className="text-primary-600 hover:text-primary-900">
                          <Eye className="h-4 w-4" />
                        </button>
                        <button 
                          onClick={() => handleEditCar(car)}
                          className="text-blue-600 hover:text-blue-900"
                        >
                          <Edit className="h-4 w-4" />
                        </button>
                        <button 
                          onClick={() => handleDeleteCar(car.id!)}
                          className="text-red-600 hover:text-red-900"
                        >
                          <Trash2 className="h-4 w-4" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {filteredCars.length === 0 && (
            <div className="text-center py-8">
              <Car className="h-12 w-12 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">
                No se encontraron vehículos
              </h3>
              <p className="text-gray-600">
                Intenta ajustar tus filtros de búsqueda
              </p>
            </div>
          )}
        </div>

        {/* Quick Actions */}
        <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="card">
            <div className="flex items-center">
              <div className="bg-blue-100 p-3 rounded-lg">
                <Settings className="h-6 w-6 text-blue-600" />
              </div>
              <div className="ml-4">
                <h3 className="text-lg font-medium text-gray-900">Configuración</h3>
                <p className="text-sm text-gray-600">Ajusta la configuración del sistema</p>
              </div>
            </div>
          </div>

          <div className="card">
            <div className="flex items-center">
              <div className="bg-green-100 p-3 rounded-lg">
                <Users className="h-6 w-6 text-green-600" />
              </div>
              <div className="ml-4">
                <h3 className="text-lg font-medium text-gray-900">Usuarios</h3>
                <p className="text-sm text-gray-600">Gestiona usuarios del sistema</p>
              </div>
            </div>
          </div>

          <div className="card">
            <div className="flex items-center">
              <div className="bg-purple-100 p-3 rounded-lg">
                <Car className="h-6 w-6 text-purple-600" />
              </div>
              <div className="ml-4">
                <h3 className="text-lg font-medium text-gray-900">Reportes</h3>
                <p className="text-sm text-gray-600">Genera reportes de ventas</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Car Edit Modal */}
      <CarEditModal
        car={editingCar}
        isOpen={isEditModalOpen}
        onClose={closeEditModal}
        onCarUpdated={handleCarUpdated}
      />

      {/* Car Add Modal */}
      <CarAddModal
        isOpen={isAddModalOpen}
        onClose={closeAddModal}
        onCarAdded={handleCarUpdated}
      />
    </div>
  );
};

export default Admin; 