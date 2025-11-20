import React, { useState, useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';
import { Send, Bot, User, RotateCcw, Car, Loader2, AlertCircle } from 'lucide-react';
import { chatbotAPI } from '../services/api';
import { ChatbotMessage, Car as CarType } from '../types';
import { getCarImageUrl } from '../services/imageService';
import toast from 'react-hot-toast';

const Chatbot: React.FC = () => {
  const [messages, setMessages] = useState<ChatbotMessage[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId] = useState<string>(() => `session-${Date.now()}`);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    // Mensaje de bienvenida inicial
    const welcomeMessage: ChatbotMessage = {
      id: 'welcome',
      text: '¡Hola! Soy tu asistente virtual para ayudarte a encontrar el auto perfecto. ¿Qué tipo de vehículo estás buscando?',
      sender: 'bot',
      timestamp: new Date(),
    };
    setMessages([welcomeMessage]);
  }, []);

  useEffect(() => {
    // Auto-scroll solo cuando lleguen mensajes del bot (no al enviar mensaje de usuario)
    if (messages.length > 0 && messages[messages.length - 1].sender === 'bot') {
      // Usar setTimeout para asegurar que los cards de autos se han renderizado
      setTimeout(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
      }, 100);
    }
  }, [messages]);

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('es-ES', {
      style: 'currency',
      currency: 'USD',
    }).format(price);
  };

  const handleSendMessage = async (e?: React.FormEvent) => {
    e?.preventDefault();
    
    if (!inputMessage.trim() || isLoading) return;

    const userMessage: ChatbotMessage = {
      id: `user-${Date.now()}`,
      text: inputMessage.trim(),
      sender: 'user',
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    const currentInput = inputMessage.trim();
    setInputMessage('');
    setIsLoading(true);

    try {
      const response = await chatbotAPI.sendMessage({
        message: currentInput,
        session_id: sessionId,
      });

      const botMessage: ChatbotMessage = {
        id: `bot-${Date.now()}`,
        text: response.response,
        sender: 'bot',
        timestamp: new Date(),
        cars: response.cars.length > 0 ? response.cars : undefined,
        needsClarification: response.needs_clarification,
        clarificationQuestion: response.clarification_question,
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error: any) {
      console.error('Error sending message:', error);
      const errorMessage: ChatbotMessage = {
        id: `error-${Date.now()}`,
        text: 'Lo siento, hubo un error al procesar tu mensaje. Por favor, intenta nuevamente.',
        sender: 'bot',
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
      toast.error('Error al enviar mensaje');
    } finally {
      setIsLoading(false);
      inputRef.current?.focus();
    }
  };

  const handleReset = async () => {
    try {
      await chatbotAPI.resetSession(sessionId);
      const welcomeMessage: ChatbotMessage = {
        id: 'welcome-reset',
        text: '¡Hola! Soy tu asistente virtual para ayudarte a encontrar el auto perfecto. ¿Qué tipo de vehículo estás buscando?',
        sender: 'bot',
        timestamp: new Date(),
      };
      setMessages([welcomeMessage]);
      toast.success('Conversación reiniciada');
    } catch (error) {
      console.error('Error resetting session:', error);
      toast.error('Error al reiniciar la conversación');
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-6 flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              Asistente Virtual
            </h1>
            <p className="text-gray-600">
              Encuentra el auto perfecto con ayuda de nuestro chatbot
            </p>
          </div>
          <button
            onClick={handleReset}
            className="btn-secondary flex items-center space-x-2"
            title="Reiniciar conversación"
          >
            <RotateCcw className="h-4 w-4" />
            <span className="hidden sm:inline">Reiniciar</span>
          </button>
        </div>

        {/* Chat Container */}
        <div className="bg-white rounded-xl shadow-lg border border-gray-200 flex flex-col" style={{ height: 'calc(100vh - 250px)', minHeight: '600px' }}>
          {/* Messages Area */}
          <div className="flex-1 overflow-y-auto p-6 space-y-4">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex items-start space-x-3 ${
                  message.sender === 'user' ? 'flex-row-reverse space-x-reverse' : ''
                }`}
              >
                {/* Avatar */}
                <div
                  className={`flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center ${
                    message.sender === 'user'
                      ? 'bg-primary-600 text-white'
                      : 'bg-gray-200 text-gray-700'
                  }`}
                >
                  {message.sender === 'user' ? (
                    <User className="h-5 w-5" />
                  ) : (
                    <Bot className="h-5 w-5" />
                  )}
                </div>

                {/* Message Content */}
                <div
                  className={`flex-1 ${
                    message.sender === 'user' ? 'text-right' : ''
                  }`}
                >
                  <div
                    className={`inline-block max-w-[80%] rounded-lg px-4 py-2 ${
                      message.sender === 'user'
                        ? 'bg-primary-600 text-white'
                        : 'bg-gray-100 text-gray-900'
                    }`}
                  >
                    <p className="whitespace-pre-wrap">{message.text}</p>
                    {message.needsClarification && message.clarificationQuestion && (
                      <div className="mt-2 pt-2 border-t border-gray-300">
                        <p className="text-sm font-medium">{message.clarificationQuestion}</p>
                      </div>
                    )}
                  </div>
                  <p className="text-xs text-gray-500 mt-1">
                    {message.timestamp.toLocaleTimeString('es-ES', {
                      hour: '2-digit',
                      minute: '2-digit',
                    })}
                  </p>
                </div>
              </div>
            ))}

            {/* Loading Indicator */}
            {isLoading && (
              <div className="flex items-start space-x-3">
                <div className="flex-shrink-0 w-10 h-10 rounded-full bg-gray-200 flex items-center justify-center">
                  <Bot className="h-5 w-5 text-gray-700" />
                </div>
                <div className="flex-1">
                  <div className="inline-block bg-gray-100 rounded-lg px-4 py-2">
                    <Loader2 className="h-5 w-5 animate-spin text-primary-600" />
                  </div>
                </div>
              </div>
            )}

            {/* Recommended Cars */}
            {messages.map((message) => {
              if (message.cars && message.cars.length > 0) {
                return (
                  <div key={`cars-${message.id}`} className="mt-4">
                    <div className="bg-primary-50 border border-primary-200 rounded-lg p-4 mb-4">
                      <h3 className="text-lg font-semibold text-primary-900 mb-2 flex items-center">
                        <Car className="h-5 w-5 mr-2" />
                        Autos Recomendados ({message.cars.length})
                      </h3>
                      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                        {message.cars.map((car: CarType) => (
                          <Link
                            key={car.id}
                            to={`/cars/${car.id}`}
                            className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 hover:shadow-md transition-shadow"
                          >
                            <div className="relative mb-3">
                              <img
                                src={getCarImageUrl(car)}
                                alt={`${car.brand} ${car.model}`}
                                className="w-full h-32 object-cover rounded-lg"
                                onError={(e) => {
                                  const target = e.target as HTMLImageElement;
                                  target.src = '/placeholder-car.jpg';
                                }}
                              />
                              {car.is_available && (
                                <div className="absolute top-2 right-2 bg-green-500 text-white px-2 py-1 rounded text-xs font-medium">
                                  Disponible
                                </div>
                              )}
                            </div>
                            <h4 className="font-semibold text-gray-900 mb-1">
                              {car.brand} {car.model}
                            </h4>
                            <p className="text-sm text-gray-600 mb-2">
                              {car.year} • {car.mileage.toLocaleString()} km
                            </p>
                            <p className="text-lg font-bold text-primary-600">
                              {formatPrice(car.price)}
                            </p>
                          </Link>
                        ))}
                      </div>
                    </div>
                  </div>
                );
              }
              return null;
            })}

            <div ref={messagesEndRef} />
          </div>

          {/* Input Area */}
          <div className="border-t border-gray-200 p-4">
            <form onSubmit={handleSendMessage} className="flex space-x-2">
              <input
                ref={inputRef}
                type="text"
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Escribe tu mensaje..."
                className="flex-1 input-field"
                disabled={isLoading}
              />
              <button
                type="submit"
                disabled={!inputMessage.trim() || isLoading}
                className="btn-primary flex items-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isLoading ? (
                  <Loader2 className="h-5 w-5 animate-spin" />
                ) : (
                  <>
                    <Send className="h-5 w-5" />
                    <span className="hidden sm:inline">Enviar</span>
                  </>
                )}
              </button>
            </form>
            <p className="text-xs text-gray-500 mt-2 text-center">
              Presiona Enter para enviar
            </p>
          </div>
        </div>

        {/* Help Section */}
        <div className="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
          <div className="flex items-start space-x-3">
            <AlertCircle className="h-5 w-5 text-blue-600 flex-shrink-0 mt-0.5" />
            <div>
              <h3 className="font-semibold text-blue-900 mb-1">Consejos para usar el chatbot</h3>
              <ul className="text-sm text-blue-800 space-y-1 list-disc list-inside">
                <li>Puedes describir el tipo de auto que buscas (marca, modelo, año, color, etc.)</li>
                <li>Menciona tu presupuesto o rango de precios</li>
                <li>Especifica características importantes (combustible, transmisión, asientos, etc.)</li>
                <li>El chatbot te ayudará a refinar tu búsqueda con preguntas de seguimiento</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Chatbot;



