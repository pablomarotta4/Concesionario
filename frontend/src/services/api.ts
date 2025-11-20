import axios from 'axios';
import { Car, CarHistory, User, AuthResponse, LoginForm, RegisterForm, ChatbotMessageRequest, ChatbotMessageResponse } from '../types';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  login: async (credentials: LoginForm): Promise<AuthResponse> => {
    const formData = new FormData();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);
    
    const response = await api.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  logout: async (): Promise<void> => {
    await api.get('/auth/logout');
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  },

  getCurrentUser: async (): Promise<User> => {
    const response = await api.get('/auth/me');
    return response.data;
  },
};

// Cars API
export const carsAPI = {
  getAllCars: async (): Promise<Car[]> => {
    const response = await api.get('/cars/');
    return response.data;
  },

  createCar: async (car: Car): Promise<Car> => {
    const response = await api.post('/cars/newcar', car);
    return response.data;
  },

  updateCar: async (carId: string, car: Car): Promise<Car> => {
    const response = await api.put(`/cars/updatecar/${carId}`, car);
    return response.data;
  },

  deleteCar: async (carId: string): Promise<void> => {
    await api.delete(`/cars/deletecar/${carId}`);
  },
};

// Car History API
export const carHistoryAPI = {
  getCarHistory: async (carId: string): Promise<CarHistory> => {
    const response = await api.get(`/carhistory/?car_id=${carId}`);
    return response.data;
  },

  createCarHistory: async (carHistory: CarHistory): Promise<CarHistory> => {
    const response = await api.post('/carhistory/newcarhistory', carHistory);
    return response.data;
  },

  updateCarHistory: async (carId: string, carHistory: CarHistory): Promise<CarHistory> => {
    const response = await api.put(`/carhistory/updatecarhistory/${carId}`, carHistory);
    return response.data;
  },

  deleteCarHistory: async (carId: string): Promise<void> => {
    await api.delete(`/carhistory/deletecarhistory/${carId}`);
  },
};

// Chatbot API
export const chatbotAPI = {
  sendMessage: async (request: ChatbotMessageRequest): Promise<ChatbotMessageResponse> => {
    const response = await api.post('/api/chatbot/message', request);
    return response.data;
  },

  resetSession: async (sessionId: string = 'default'): Promise<{ message: string; session_id: string }> => {
    const response = await api.post('/api/chatbot/reset', null, {
      params: { session_id: sessionId },
    });
    return response.data;
  },

  getSessionInfo: async (sessionId: string): Promise<any> => {
    const response = await api.get(`/api/chatbot/session/${sessionId}`);
    return response.data;
  },

  healthCheck: async (): Promise<{ status: string; service?: string; sessions_active?: number; reason?: string }> => {
    const response = await api.get('/api/chatbot/health');
    return response.data;
  },
};

export default api; 