import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { 
  Search, 
  Filter, 
  Grid, 
  List, 
  ChevronDown,
  Calendar,
  Users,
  MapPin,
  Star,
  Car
} from 'lucide-react';
import { carsAPI } from '../services/api';
import { Car as CarType } from '../types';
import { getCarImageUrl } from '../services/imageService';

const Cars: React.FC = () => {
  const [cars, setCars] = useState<CarType[]>([]);
  const [filteredCars, setFilteredCars] = useState<CarType[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedBrand, setSelectedBrand] = useState('');
  const [selectedYear, setSelectedYear] = useState('');
  const [selectedPriceRange, setSelectedPriceRange] = useState('');
  const [showFilters, setShowFilters] = useState(false);

  useEffect(() => {
    const fetchCars = async () => {
      try {
        const carsData = await carsAPI.getAllCars();
        setCars(carsData);
        setFilteredCars(carsData);
      } catch (error) {
        console.error('Error fetching cars:', error);
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

    // Brand filter
    if (selectedBrand) {
      filtered = filtered.filter(car => car.brand === selectedBrand);
    }

    // Year filter
    if (selectedYear) {
      filtered = filtered.filter(car => car.year.toString() === selectedYear);
    }

    // Price range filter
    if (selectedPriceRange) {
      const [min, max] = selectedPriceRange.split('-').map(Number);
      filtered = filtered.filter(car => {
        if (max) {
          return car.price >= min && car.price <= max;
        } else {
          return car.price >= min;
        }
      });
    }

    setFilteredCars(filtered);
  }, [cars, searchTerm, selectedBrand, selectedYear, selectedPriceRange]);

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('es-ES', {
      style: 'currency',
      currency: 'USD',
    }).format(price);
  };

  const getUniqueBrands = () => {
    return [...new Set(cars.map(car => car.brand))];
  };

  const getUniqueYears = () => {
    return [...new Set(cars.map(car => car.year))].sort((a, b) => b - a);
  };

  const clearFilters = () => {
    setSearchTerm('');
    setSelectedBrand('');
    setSelectedYear('');
    setSelectedPriceRange('');
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="animate-pulse">
            <div className="h-8 bg-gray-200 rounded w-1/4 mb-8"></div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {[...Array(6)].map((_, index) => (
                <div key={index} className="card">
                  <div className="bg-gray-200 h-48 rounded-lg mb-4"></div>
                  <div className="space-y-2">
                    <div className="h-4 bg-gray-200 rounded"></div>
                    <div className="h-4 bg-gray-200 rounded w-3/4"></div>
                    <div className="h-4 bg-gray-200 rounded w-1/2"></div>
                  </div>
                </div>
              ))}
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
            Nuestros Vehículos
          </h1>
          <p className="text-gray-600">
            Encuentra el auto perfecto para ti
          </p>
        </div>

        {/* Search and Filters */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-8">
          <div className="flex flex-col lg:flex-row gap-4">
            {/* Search */}
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                <input
                  type="text"
                  placeholder="Buscar por marca, modelo o color..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="input-field pl-10"
                />
              </div>
            </div>

            {/* View Mode Toggle */}
            <div className="flex items-center space-x-2">
              <button
                onClick={() => setViewMode('grid')}
                className={`p-2 rounded ${
                  viewMode === 'grid'
                    ? 'bg-primary-100 text-primary-600'
                    : 'text-gray-400 hover:text-gray-600'
                }`}
              >
                <Grid className="h-5 w-5" />
              </button>
              <button
                onClick={() => setViewMode('list')}
                className={`p-2 rounded ${
                  viewMode === 'list'
                    ? 'bg-primary-100 text-primary-600'
                    : 'text-gray-400 hover:text-gray-600'
                }`}
              >
                <List className="h-5 w-5" />
              </button>
            </div>

            {/* Filters Toggle */}
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

          {/* Filters Panel */}
          {showFilters && (
            <div className="mt-6 pt-6 border-t border-gray-200">
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                {/* Brand Filter */}
                <div>
                  <label className="form-label">Marca</label>
                  <select
                    value={selectedBrand}
                    onChange={(e) => setSelectedBrand(e.target.value)}
                    className="input-field"
                  >
                    <option value="">Todas las marcas</option>
                    {getUniqueBrands().map(brand => (
                      <option key={brand} value={brand}>{brand}</option>
                    ))}
                  </select>
                </div>

                {/* Year Filter */}
                <div>
                  <label className="form-label">Año</label>
                  <select
                    value={selectedYear}
                    onChange={(e) => setSelectedYear(e.target.value)}
                    className="input-field"
                  >
                    <option value="">Todos los años</option>
                    {getUniqueYears().map(year => (
                      <option key={year} value={year}>{year}</option>
                    ))}
                  </select>
                </div>

                {/* Price Range Filter */}
                <div>
                  <label className="form-label">Rango de Precio</label>
                  <select
                    value={selectedPriceRange}
                    onChange={(e) => setSelectedPriceRange(e.target.value)}
                    className="input-field"
                  >
                    <option value="">Todos los precios</option>
                    <option value="0-10000">$0 - $10,000</option>
                    <option value="10000-25000">$10,000 - $25,000</option>
                    <option value="25000-50000">$25,000 - $50,000</option>
                    <option value="50000-100000">$50,000 - $100,000</option>
                    <option value="100000-999999">Más de $100,000</option>
                  </select>
                </div>

                {/* Clear Filters */}
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

        {/* Results Count */}
        <div className="mb-6">
          <p className="text-gray-600">
            Mostrando {filteredCars.length} de {cars.length} vehículos
          </p>
        </div>

        {/* Cars Grid/List */}
        {filteredCars.length === 0 ? (
          <div className="text-center py-12">
            <Car className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              No se encontraron vehículos
            </h3>
            <p className="text-gray-600">
              Intenta ajustar tus filtros de búsqueda
            </p>
          </div>
        ) : (
          <div className={
            viewMode === 'grid'
              ? 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8'
              : 'space-y-6'
          }>
            {filteredCars.map((car) => (
              <div
                key={car.id}
                className={`card hover:shadow-lg transition-shadow ${
                  viewMode === 'list' ? 'flex' : ''
                }`}
              >
                <div className={viewMode === 'list' ? 'flex-shrink-0 mr-6' : ''}>
                  <div className="relative">
                    <img
                      src={getCarImageUrl(car)}
                      alt={`${car.brand} ${car.model}`}
                      className={`object-cover rounded-lg ${
                        viewMode === 'list' ? 'w-64 h-48' : 'w-full h-48'
                      }`}
                      onError={(e) => {
                        const target = e.target as HTMLImageElement;
                        target.src = '/placeholder-car.jpg';
                      }}
                    />
                    <div className="absolute top-2 right-2 bg-primary-600 text-white px-2 py-1 rounded text-sm font-medium">
                      {car.is_available ? 'Disponible' : 'Vendido'}
                    </div>
                  </div>
                </div>
                
                <div className={`mt-4 ${viewMode === 'list' ? 'flex-1' : ''}`}>
                  <h3 className="text-xl font-semibold text-gray-900 mb-2">
                    {car.brand} {car.model}
                  </h3>
                  
                  <div className="flex items-center justify-between mb-3">
                    <span className="text-2xl font-bold text-primary-600">
                      {formatPrice(car.price)}
                    </span>
                    <span className="text-sm text-gray-500">
                      {car.year}
                    </span>
                  </div>
                  
                  <div className={`grid gap-2 text-sm text-gray-600 mb-4 ${
                    viewMode === 'list' ? 'grid-cols-3' : 'grid-cols-2'
                  }`}>
                    <div className="flex items-center">
                      <Calendar className="h-4 w-4 mr-1" />
                      {car.year}
                    </div>
                    <div className="flex items-center">
                      <Users className="h-4 w-4 mr-1" />
                      {car.seats} asientos
                    </div>
                    <div className="flex items-center">
                      <MapPin className="h-4 w-4 mr-1" />
                      {car.mileage.toLocaleString()} km
                    </div>
                    {viewMode === 'list' && (
                      <div className="flex items-center">
                        <Star className="h-4 w-4 mr-1" />
                        {car.fuel_type}
                      </div>
                    )}
                  </div>
                  
                  <Link
                    to={`/cars/${car.id}`}
                    className="btn-primary w-full text-center"
                  >
                    Ver Detalles
                  </Link>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Cars; 