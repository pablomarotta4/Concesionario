import React from 'react';
import { Car, Phone, Mail, MapPin } from 'lucide-react';

const Footer: React.FC = () => {
  return (
    <footer className="bg-gray-900 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Company Info */}
          <div className="col-span-1 md:col-span-2">
            <div className="flex items-center space-x-2 mb-4">
              <Car className="h-8 w-8 text-primary-400" />
              <span className="text-xl font-bold">Concesionario Virtual</span>
            </div>
            <p className="text-gray-300 mb-4">
              Tu destino confiable para encontrar el vehículo perfecto. 
              Ofrecemos una amplia selección de autos usados y nuevos 
              con las mejores condiciones del mercado.
            </p>
            <div className="flex space-x-4">
              <a href="#" className="text-gray-300 hover:text-white transition-colors">
                Facebook
              </a>
              <a href="#" className="text-gray-300 hover:text-white transition-colors">
                Instagram
              </a>
              <a href="#" className="text-gray-300 hover:text-white transition-colors">
                Twitter
              </a>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Enlaces Rápidos</h3>
            <ul className="space-y-2">
              <li>
                <a href="/" className="text-gray-300 hover:text-white transition-colors">
                  Inicio
                </a>
              </li>
              <li>
                <a href="/cars" className="text-gray-300 hover:text-white transition-colors">
                  Vehículos
                </a>
              </li>
              <li>
                <a href="/about" className="text-gray-300 hover:text-white transition-colors">
                  Nosotros
                </a>
              </li>
              <li>
                <a href="/contact" className="text-gray-300 hover:text-white transition-colors">
                  Contacto
                </a>
              </li>
            </ul>
          </div>

          {/* Contact Info */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Contacto</h3>
            <div className="space-y-3">
              <div className="flex items-center space-x-3">
                <Phone className="h-5 w-5 text-primary-400" />
                <span className="text-gray-300">+1 (555) 123-4567</span>
              </div>
              <div className="flex items-center space-x-3">
                <Mail className="h-5 w-5 text-primary-400" />
                <span className="text-gray-300">info@concesionario.com</span>
              </div>
              <div className="flex items-center space-x-3">
                <MapPin className="h-5 w-5 text-primary-400" />
                <span className="text-gray-300">
                  Av. Principal 123, Ciudad
                </span>
              </div>
            </div>
          </div>
        </div>

        <div className="border-t border-gray-800 mt-8 pt-8">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <p className="text-gray-300 text-sm">
              © 2024 Concesionario Virtual. Todos los derechos reservados.
            </p>
            <div className="flex space-x-6 mt-4 md:mt-0">
              <a href="/privacy" className="text-gray-300 hover:text-white text-sm transition-colors">
                Privacidad
              </a>
              <a href="/terms" className="text-gray-300 hover:text-white text-sm transition-colors">
                Términos
              </a>
              <a href="/cookies" className="text-gray-300 hover:text-white text-sm transition-colors">
                Cookies
              </a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer; 