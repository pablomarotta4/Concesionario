import React, { useState } from 'react';
import { X, Upload } from 'lucide-react';
import { Car as CarType } from '../types';
import { carsAPI } from '../services/api';
import ImageUpload from './ImageUpload';
import toast from 'react-hot-toast';

interface CarAddModalProps {
  isOpen: boolean;
  onClose: () => void;
  onCarAdded: () => void;
}

const CarAddModal: React.FC<CarAddModalProps> = ({
  isOpen,
  onClose,
  onCarAdded
}) => {
  const [formData, setFormData] = useState<Partial<CarType>>({
    brand: '',
    model: '',
    year: new Date().getFullYear(),
    color: '',
    price: 0,
    is_available: true,
    mileage: 0,
    engine_type: '',
    transmission: '',
    fuel_type: '',
    doors: 4,
    seats: 5,
    max_speed: 0,
    acceleration: 0,
    horsepower: 0,
    torque: 0,
    weight: 0,
    length: 0,
    width: 0,
    description: '',
    image_url: '',
    paymenth_method: 'Financiamiento disponible'
  });
  const [isLoading, setIsLoading] = useState(false);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'number' ? parseFloat(value) : type === 'checkbox' ? (e.target as HTMLInputElement).checked : value
    }));
  };

  const handleImageUploaded = (filename: string) => {
    setFormData(prev => ({
      ...prev,
      image_url: filename
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    setIsLoading(true);
    try {
      await carsAPI.createCar(formData as CarType);
      toast.success('Vehículo agregado exitosamente');
      onCarAdded();
      onClose();
      // Reset form
      setFormData({
        brand: '',
        model: '',
        year: new Date().getFullYear(),
        color: '',
        price: 0,
        is_available: true,
        mileage: 0,
        engine_type: '',
        transmission: '',
        fuel_type: '',
        doors: 4,
        seats: 5,
        max_speed: 0,
        acceleration: 0,
        horsepower: 0,
        torque: 0,
        weight: 0,
        length: 0,
        width: 0,
        description: '',
        image_url: '',
        paymenth_method: 'Financiamiento disponible'
      });
    } catch (error) {
      console.error('Error creating car:', error);
      toast.error('Error al agregar el vehículo');
    } finally {
      setIsLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-4xl w-full mx-4 max-h-[90vh] overflow-y-auto">
        <div className="flex justify-between items-center p-6 border-b">
          <h2 className="text-xl font-semibold text-gray-900">
            Agregar Nuevo Vehículo
          </h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600"
          >
            <X className="h-6 w-6" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-6">
          {/* Basic Information */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div>
              <label className="form-label">Marca *</label>
              <input
                type="text"
                name="brand"
                value={formData.brand || ''}
                onChange={handleInputChange}
                className="input-field"
                required
              />
            </div>

            <div>
              <label className="form-label">Modelo *</label>
              <input
                type="text"
                name="model"
                value={formData.model || ''}
                onChange={handleInputChange}
                className="input-field"
                required
              />
            </div>

            <div>
              <label className="form-label">Año *</label>
              <input
                type="number"
                name="year"
                value={formData.year || ''}
                onChange={handleInputChange}
                className="input-field"
                min="1900"
                max="2030"
                required
              />
            </div>

            <div>
              <label className="form-label">Color *</label>
              <input
                type="text"
                name="color"
                value={formData.color || ''}
                onChange={handleInputChange}
                className="input-field"
                required
              />
            </div>

            <div>
              <label className="form-label">Precio (USD) *</label>
              <input
                type="number"
                name="price"
                value={formData.price || ''}
                onChange={handleInputChange}
                className="input-field"
                min="0"
                step="0.01"
                required
              />
            </div>

            <div>
              <label className="form-label">Kilometraje *</label>
              <input
                type="number"
                name="mileage"
                value={formData.mileage || ''}
                onChange={handleInputChange}
                className="input-field"
                min="0"
                required
              />
            </div>
          </div>

          {/* Technical Specifications */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div>
              <label className="form-label">Tipo de Motor *</label>
              <input
                type="text"
                name="engine_type"
                value={formData.engine_type || ''}
                onChange={handleInputChange}
                className="input-field"
                required
              />
            </div>

            <div>
              <label className="form-label">Transmisión *</label>
              <select
                name="transmission"
                value={formData.transmission || ''}
                onChange={handleInputChange}
                className="input-field"
                required
              >
                <option value="">Seleccionar...</option>
                <option value="Manual">Manual</option>
                <option value="Automática">Automática</option>
                <option value="CVT">CVT</option>
                <option value="Automática 6 velocidades">Automática 6 velocidades</option>
                <option value="Automática 8 velocidades">Automática 8 velocidades</option>
                <option value="Automática DSG 6 velocidades">Automática DSG 6 velocidades</option>
                <option value="Automática 7 velocidades S-tronic">Automática 7 velocidades S-tronic</option>
              </select>
            </div>

            <div>
              <label className="form-label">Tipo de Combustible *</label>
              <select
                name="fuel_type"
                value={formData.fuel_type || ''}
                onChange={handleInputChange}
                className="input-field"
                required
              >
                <option value="">Seleccionar...</option>
                <option value="Gasolina">Gasolina</option>
                <option value="Diésel">Diésel</option>
                <option value="Híbrido">Híbrido</option>
                <option value="Eléctrico">Eléctrico</option>
              </select>
            </div>

            <div>
              <label className="form-label">Puertas *</label>
              <input
                type="number"
                name="doors"
                value={formData.doors || ''}
                onChange={handleInputChange}
                className="input-field"
                min="2"
                max="5"
                required
              />
            </div>

            <div>
              <label className="form-label">Asientos *</label>
              <input
                type="number"
                name="seats"
                value={formData.seats || ''}
                onChange={handleInputChange}
                className="input-field"
                min="2"
                max="9"
                required
              />
            </div>

            <div>
              <label className="form-label">Velocidad Máxima (km/h)</label>
              <input
                type="number"
                name="max_speed"
                value={formData.max_speed || ''}
                onChange={handleInputChange}
                className="input-field"
                min="0"
              />
            </div>
          </div>

          {/* Performance Specifications */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div>
              <label className="form-label">Aceleración (0-100 km/h)</label>
              <input
                type="number"
                name="acceleration"
                value={formData.acceleration || ''}
                onChange={handleInputChange}
                className="input-field"
                min="0"
                step="0.1"
              />
            </div>

            <div>
              <label className="form-label">Caballos de Fuerza</label>
              <input
                type="number"
                name="horsepower"
                value={formData.horsepower || ''}
                onChange={handleInputChange}
                className="input-field"
                min="0"
              />
            </div>

            <div>
              <label className="form-label">Torque (Nm)</label>
              <input
                type="number"
                name="torque"
                value={formData.torque || ''}
                onChange={handleInputChange}
                className="input-field"
                min="0"
              />
            </div>

            <div>
              <label className="form-label">Peso (kg)</label>
              <input
                type="number"
                name="weight"
                value={formData.weight || ''}
                onChange={handleInputChange}
                className="input-field"
                min="0"
              />
            </div>
          </div>

          {/* Dimensions */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="form-label">Longitud (m)</label>
              <input
                type="number"
                name="length"
                value={formData.length || ''}
                onChange={handleInputChange}
                className="input-field"
                min="0"
                step="0.01"
              />
            </div>

            <div>
              <label className="form-label">Ancho (m)</label>
              <input
                type="number"
                name="width"
                value={formData.width || ''}
                onChange={handleInputChange}
                className="input-field"
                min="0"
                step="0.01"
              />
            </div>
          </div>

          {/* Description and Payment Method */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="form-label">Descripción *</label>
              <textarea
                name="description"
                value={formData.description || ''}
                onChange={handleInputChange}
                className="input-field"
                rows={4}
                required
              />
            </div>

            <div>
              <label className="form-label">Método de Pago *</label>
              <input
                type="text"
                name="paymenth_method"
                value={formData.paymenth_method || ''}
                onChange={handleInputChange}
                className="input-field"
                required
              />
            </div>
          </div>

          {/* Availability */}
          <div className="flex items-center">
            <input
              type="checkbox"
              name="is_available"
              checked={formData.is_available || false}
              onChange={handleInputChange}
              className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
            />
            <label className="ml-2 block text-sm text-gray-900">
              Vehículo disponible
            </label>
          </div>

          {/* Image Upload */}
          <div>
            <label className="form-label">Imagen del Vehículo</label>
            <div className="mt-2">
              <ImageUpload
                onImageUploaded={handleImageUploaded}
                className="mt-2"
              />
            </div>
          </div>

          {/* Submit Buttons */}
          <div className="flex justify-end space-x-4 pt-6 border-t">
            <button
              type="button"
              onClick={onClose}
              className="btn-secondary"
              disabled={isLoading}
            >
              Cancelar
            </button>
            <button
              type="submit"
              className="btn-primary"
              disabled={isLoading}
            >
              {isLoading ? (
                <div className="flex items-center">
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                  Agregando...
                </div>
              ) : (
                'Agregar Vehículo'
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default CarAddModal; 