import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Car, ArrowRight, Star, MapPin, Calendar, Users } from 'lucide-react';
import { carsAPI } from '../services/api';
import { Car as CarType } from '../types';
import { getCarImageUrl } from '../services/imageService';
import { useAuth } from '../contexts/AuthContext';

const Home: React.FC = () => {
  const [featuredCars, setFeaturedCars] = useState<CarType[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const { user, isAuthenticated } = useAuth(); // Asegúrate de obtener isAuthenticated también

  useEffect(() => {
    const fetchFeaturedCars = async () => {
      try {
        const cars = await carsAPI.getAllCars();
        // Show first 6 available cars as featured
        const availableCars = cars.filter(car => car.is_available).slice(0, 6);
        setFeaturedCars(availableCars);
      } catch (error) {
        console.error('Error fetching cars:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchFeaturedCars();
  }, []);

  // Añade este useEffect para forzar re-render cuando cambie el estado de autenticación
  useEffect(() => {
    // Este useEffect se ejecutará cada vez que user o isAuthenticated cambien
    console.log('Auth state changed:', { user, isAuthenticated });
  }, [user, isAuthenticated]);

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('es-ES', {
      style: 'currency',
      currency: 'USD',
    }).format(price);
  };

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative bg-gradient-to-r from-primary-600 to-primary-800 text-white">
        <div className="absolute inset-0 bg-black opacity-20"></div>
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold mb-6">
              Encuentra tu auto ideal
            </h1>
            <p className="text-xl md:text-2xl mb-8 text-primary-100">
              La mejor selección de vehículos con las condiciones más favorables del mercado
            </p>
            {/* Mostrar contenido condicional basado en el estado de autenticación */}
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                to="/cars"
                className="bg-white text-primary-600 hover:bg-gray-100 px-8 py-3 rounded-lg font-semibold text-lg transition-colors inline-flex items-center justify-center"
              >
                Ver Vehículos
                <ArrowRight className="ml-2 h-5 w-5" />
              </Link>
              <Link
                to="/contact"
                className="border-2 border-white text-white hover:bg-white hover:text-primary-600 px-8 py-3 rounded-lg font-semibold text-lg transition-colors"
              >
                Contactar
              </Link>
            </div>
            {/* Mensaje de bienvenida si está autenticado */}
            {user && (
              <div className="mt-4">
                <p className="text-primary-100">
                  ¡Bienvenido, {user.name || user.email}!
                </p>
              </div>
            )}
          </div>
        </div>
      </section>

      {/* Rest of your component remains the same */}
      {/* Features Section */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              ¿Por qué elegirnos?
            </h2>
            <p className="text-lg text-gray-600">
              Ofrecemos la mejor experiencia en la compra de vehículos
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="bg-primary-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <Car className="h-8 w-8 text-primary-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Amplia Selección</h3>
              <p className="text-gray-600">
                Miles de vehículos verificados y en excelente estado
              </p>
            </div>
            
            <div className="text-center">
              <div className="bg-primary-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <Star className="h-8 w-8 text-primary-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Calidad Garantizada</h3>
              <p className="text-gray-600">
                Todos nuestros vehículos pasan por rigurosas inspecciones
              </p>
            </div>
            
            <div className="text-center">
              <div className="bg-primary-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <MapPin className="h-8 w-8 text-primary-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Ubicación Conveniente</h3>
              <p className="text-gray-600">
                Fácil acceso y estacionamiento gratuito
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Featured Cars Section */}
      <section className="py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Vehículos Destacados
            </h2>
            <p className="text-lg text-gray-600">
              Los mejores autos seleccionados especialmente para ti
            </p>
          </div>

          {isLoading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {[...Array(6)].map((_, index) => (
                <div key={index} className="card animate-pulse">
                  <div className="bg-gray-200 h-48 rounded-lg mb-4"></div>
                  <div className="space-y-2">
                    <div className="h-4 bg-gray-200 rounded"></div>
                    <div className="h-4 bg-gray-200 rounded w-3/4"></div>
                    <div className="h-4 bg-gray-200 rounded w-1/2"></div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {featuredCars.map((car) => (
                <div key={car.id} className="card hover:shadow-lg transition-shadow">
                  <div className="relative">
                    <img
                      src={getCarImageUrl(car)}
                      alt={`${car.brand} ${car.model}`}
                      className="w-full h-48 object-cover rounded-lg"
                      onError={(e) => {
                        const target = e.target as HTMLImageElement;
                        target.src = '/placeholder-car.jpg';
                      }}
                    />
                    <div className="absolute top-2 right-2 bg-primary-600 text-white px-2 py-1 rounded text-sm font-medium">
                      {car.is_available ? 'Disponible' : 'Vendido'}
                    </div>
                  </div>
                  
                  <div className="mt-4">
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
                    
                    <div className="grid grid-cols-2 gap-2 text-sm text-gray-600 mb-4">
                      <div className="flex items-center">
                        <Calendar className="h-4 w-4 mr-1" />
                        {car.year}
                      </div>
                      <div className="flex items-center">
                        <Users className="h-4 w-4 mr-1" />
                        {car.seats} asientos
                      </div>
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
          
          <div className="text-center mt-12">
            <Link
              to="/cars"
              className="btn-primary inline-flex items-center"
            >
              Ver Todos los Vehículos
              <ArrowRight className="ml-2 h-5 w-5" />
            </Link>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-primary-600 text-white py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold mb-4">
            ¿Listo para encontrar tu auto ideal?
          </h2>
          <p className="text-xl mb-8 text-primary-100">
            Nuestro equipo está listo para ayudarte a encontrar el vehículo perfecto
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/cars"
              className="bg-white text-primary-600 hover:bg-gray-100 px-8 py-3 rounded-lg font-semibold text-lg transition-colors"
            >
              Explorar Vehículos
            </Link>
            <Link
              to="/contact"
              className="border-2 border-white text-white hover:bg-white hover:text-primary-600 px-8 py-3 rounded-lg font-semibold text-lg transition-colors"
            >
              Contactar
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;