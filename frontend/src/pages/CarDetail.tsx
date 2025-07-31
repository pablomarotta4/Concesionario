import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { 
  ArrowLeft, 
  Calendar, 
  Users, 
  MapPin, 
  Star, 
  Zap, 
  Gauge, 
  Scale,
  Ruler,
  CreditCard,
  Phone,
  Mail,
  Clock,
  CheckCircle,
  AlertCircle
} from 'lucide-react';
import { carsAPI, carHistoryAPI } from '../services/api';
import { Car as CarType, CarHistory } from '../types';
import { getCarImageUrl } from '../services/imageService';
import toast from 'react-hot-toast';

const CarDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [car, setCar] = useState<CarType | null>(null);
  const [carHistory, setCarHistory] = useState<CarHistory | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'details' | 'history' | 'contact'>('details');

  useEffect(() => {
    const fetchCarDetails = async () => {
      if (!id) return;
      
      try {
        const [carData, historyData] = await Promise.all([
          carsAPI.getAllCars().then(cars => cars.find(c => c.id === id)),
          carHistoryAPI.getCarHistory(id).catch(() => null)
        ]);
        
        if (carData) {
          setCar(carData);
        }
        setCarHistory(historyData);
      } catch (error) {
        console.error('Error fetching car details:', error);
        toast.error('Error al cargar los detalles del vehículo');
      } finally {
        setIsLoading(false);
      }
    };

    fetchCarDetails();
  }, [id]);

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('es-ES', {
      style: 'currency',
      currency: 'USD',
    }).format(price);
  };

  const formatMileage = (mileage: number) => {
    return mileage.toLocaleString('es-ES');
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="animate-pulse">
            <div className="h-8 bg-gray-200 rounded w-1/4 mb-8"></div>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              <div className="bg-gray-200 h-96 rounded-lg"></div>
              <div className="space-y-4">
                <div className="h-6 bg-gray-200 rounded"></div>
                <div className="h-4 bg-gray-200 rounded w-3/4"></div>
                <div className="h-4 bg-gray-200 rounded w-1/2"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (!car) {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center py-12">
            <AlertCircle className="h-12 w-12 text-red-500 mx-auto mb-4" />
            <h2 className="text-2xl font-bold text-gray-900 mb-2">
              Vehículo no encontrado
            </h2>
            <p className="text-gray-600 mb-6">
              El vehículo que buscas no existe o ha sido removido.
            </p>
            <Link to="/cars" className="btn-primary">
              Volver a Vehículos
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Breadcrumb */}
        <div className="mb-8">
          <Link
            to="/cars"
            className="inline-flex items-center text-primary-600 hover:text-primary-500"
          >
            <ArrowLeft className="h-4 w-4 mr-2" />
            Volver a Vehículos
          </Link>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Car Images */}
          <div>
            <div className="relative">
                             <img
                 src={getCarImageUrl(car)}
                 alt={`${car.brand} ${car.model}`}
                 className="w-full h-96 object-cover rounded-lg"
                 onError={(e) => {
                   const target = e.target as HTMLImageElement;
                   target.src = '/placeholder-car.jpg';
                 }}
               />
              <div className="absolute top-4 right-4">
                <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                  car.is_available 
                    ? 'bg-green-100 text-green-800' 
                    : 'bg-red-100 text-red-800'
                }`}>
                  {car.is_available ? 'Disponible' : 'Vendido'}
                </span>
              </div>
            </div>
          </div>

          {/* Car Info */}
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              {car.brand} {car.model}
            </h1>
            <p className="text-lg text-gray-600 mb-6">
              {car.year} • {car.color} • {formatMileage(car.mileage)} km
            </p>

            <div className="text-3xl font-bold text-primary-600 mb-6">
              {formatPrice(car.price)}
            </div>

            {/* Quick Specs */}
            <div className="grid grid-cols-2 gap-4 mb-8">
              <div className="flex items-center">
                <Calendar className="h-5 w-5 text-gray-400 mr-2" />
                <span className="text-sm text-gray-600">{car.year}</span>
              </div>
              <div className="flex items-center">
                <Users className="h-5 w-5 text-gray-400 mr-2" />
                <span className="text-sm text-gray-600">{car.seats} asientos</span>
              </div>
              <div className="flex items-center">
                <MapPin className="h-5 w-5 text-gray-400 mr-2" />
                <span className="text-sm text-gray-600">{formatMileage(car.mileage)} km</span>
              </div>
              <div className="flex items-center">
                <Star className="h-5 w-5 text-gray-400 mr-2" />
                <span className="text-sm text-gray-600">{car.fuel_type}</span>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="space-y-3">
              <button className="btn-primary w-full">
                <Phone className="h-4 w-4 mr-2" />
                Contactar Vendedor
              </button>
              <button className="btn-secondary w-full">
                <Mail className="h-4 w-4 mr-2" />
                Enviar Mensaje
              </button>
            </div>
          </div>
        </div>

        {/* Tabs */}
        <div className="mt-12">
          <div className="border-b border-gray-200">
            <nav className="-mb-px flex space-x-8">
              <button
                onClick={() => setActiveTab('details')}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'details'
                    ? 'border-primary-500 text-primary-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Detalles
              </button>
              <button
                onClick={() => setActiveTab('history')}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'history'
                    ? 'border-primary-500 text-primary-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Historial
              </button>
              <button
                onClick={() => setActiveTab('contact')}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'contact'
                    ? 'border-primary-500 text-primary-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Contacto
              </button>
            </nav>
          </div>

          {/* Tab Content */}
          <div className="mt-8">
            {activeTab === 'details' && (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                {/* Technical Specifications */}
                <div className="card">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">
                    Especificaciones Técnicas
                  </h3>
                  <div className="space-y-3">
                    <div className="flex justify-between">
                      <span className="text-gray-600">Motor</span>
                      <span className="font-medium">{car.engine_type}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Transmisión</span>
                      <span className="font-medium">{car.transmission}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Combustible</span>
                      <span className="font-medium">{car.fuel_type}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Puertas</span>
                      <span className="font-medium">{car.doors}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Asientos</span>
                      <span className="font-medium">{car.seats}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Velocidad Máxima</span>
                      <span className="font-medium">{car.max_speed || 'N/A'} km/h</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Aceleración</span>
                      <span className="font-medium">{car.acceleration}s (0-100 km/h)</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Caballos de Fuerza</span>
                      <span className="font-medium">{car.horsepower} hp</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Torque</span>
                      <span className="font-medium">{car.torque} Nm</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Peso</span>
                      <span className="font-medium">{car.weight} kg</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Longitud</span>
                      <span className="font-medium">{car.length} m</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Ancho</span>
                      <span className="font-medium">{car.width} m</span>
                    </div>
                  </div>
                </div>

                {/* Description */}
                <div className="card">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">
                    Descripción
                  </h3>
                  <p className="text-gray-600 leading-relaxed">
                    {car.description}
                  </p>
                  
                  <div className="mt-6">
                    <h4 className="font-medium text-gray-900 mb-2">
                      Método de Pago
                    </h4>
                    <div className="flex items-center">
                      <CreditCard className="h-4 w-4 text-gray-400 mr-2" />
                      <span className="text-gray-600">{car.paymenth_method}</span>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'history' && (
              <div className="card">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">
                  Historial del Vehículo
                </h3>
                {carHistory ? (
                  <div className="space-y-4">
                    {carHistory.action && (
                      <div className="flex items-start">
                        <CheckCircle className="h-5 w-5 text-green-500 mr-3 mt-0.5" />
                        <div>
                          <p className="font-medium text-gray-900">Última Acción</p>
                          <p className="text-gray-600">{carHistory.action}</p>
                        </div>
                      </div>
                    )}
                    
                    {carHistory.accidents && carHistory.accidents.length > 0 && (
                      <div className="flex items-start">
                        <AlertCircle className="h-5 w-5 text-red-500 mr-3 mt-0.5" />
                        <div>
                          <p className="font-medium text-gray-900">Accidentes Reportados</p>
                          <ul className="text-gray-600 list-disc list-inside">
                            {carHistory.accidents.map((accident, index) => (
                              <li key={index}>{accident}</li>
                            ))}
                          </ul>
                        </div>
                      </div>
                    )}
                    
                    {carHistory.service_records && carHistory.service_records.length > 0 && (
                      <div className="flex items-start">
                        <CheckCircle className="h-5 w-5 text-blue-500 mr-3 mt-0.5" />
                        <div>
                          <p className="font-medium text-gray-900">Registros de Servicio</p>
                          <ul className="text-gray-600 list-disc list-inside">
                            {carHistory.service_records.map((record, index) => (
                              <li key={index}>{record}</li>
                            ))}
                          </ul>
                        </div>
                      </div>
                    )}
                    
                    {carHistory.ownership_history && carHistory.ownership_history.length > 0 && (
                      <div className="flex items-start">
                        <Users className="h-5 w-5 text-purple-500 mr-3 mt-0.5" />
                        <div>
                          <p className="font-medium text-gray-900">Historial de Propietarios</p>
                          <ul className="text-gray-600 list-disc list-inside">
                            {carHistory.ownership_history.map((owner, index) => (
                              <li key={index}>{owner}</li>
                            ))}
                          </ul>
                        </div>
                      </div>
                    )}
                    
                    {carHistory.last_updated && (
                      <div className="flex items-center text-sm text-gray-500">
                        <Clock className="h-4 w-4 mr-2" />
                        Última actualización: {carHistory.last_updated}
                      </div>
                    )}
                  </div>
                ) : (
                  <p className="text-gray-600">
                    No hay información de historial disponible para este vehículo.
                  </p>
                )}
              </div>
            )}

            {activeTab === 'contact' && (
              <div className="card">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">
                  Información de Contacto
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <h4 className="font-medium text-gray-900 mb-3">Concesionario Virtual</h4>
                    <div className="space-y-3">
                      <div className="flex items-center">
                        <Phone className="h-5 w-5 text-gray-400 mr-3" />
                        <span className="text-gray-600">+1 (555) 123-4567</span>
                      </div>
                      <div className="flex items-center">
                        <Mail className="h-5 w-5 text-gray-400 mr-3" />
                        <span className="text-gray-600">info@concesionario.com</span>
                      </div>
                      <div className="flex items-center">
                        <MapPin className="h-5 w-5 text-gray-400 mr-3" />
                        <span className="text-gray-600">Av. Principal 123, Ciudad</span>
                      </div>
                    </div>
                  </div>
                  
                  <div>
                    <h4 className="font-medium text-gray-900 mb-3">Horarios de Atención</h4>
                    <div className="space-y-2 text-gray-600">
                      <div>Lunes - Viernes: 9:00 AM - 6:00 PM</div>
                      <div>Sábado: 9:00 AM - 4:00 PM</div>
                      <div>Domingo: Cerrado</div>
                    </div>
                  </div>
                </div>
                
                <div className="mt-6 pt-6 border-t border-gray-200">
                  <button className="btn-primary mr-4">
                    <Phone className="h-4 w-4 mr-2" />
                    Llamar Ahora
                  </button>
                  <button className="btn-secondary">
                    <Mail className="h-4 w-4 mr-2" />
                    Enviar Email
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default CarDetail; 