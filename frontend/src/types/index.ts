export interface Car {
  id?: string;
  brand: string;
  model: string;
  year: number;
  color: string;
  price: number;
  is_available: boolean;
  mileage: number;
  engine_type: string;
  transmission: string;
  fuel_type: string;
  doors: number;
  seats: number;
  max_speed?: number;
  acceleration: number;
  horsepower: number;
  torque: number;
  weight: number;
  length: number;
  width: number;
  description: string;
  image_url?: string;
  paymenth_method: string;
  history?: CarHistory;
}

export interface CarHistory {
  id?: string;
  car_id?: string;
  action?: string;
  accidents?: string[];
  service_records?: string[];
  ownership_history?: string[];
  last_updated?: string;
}

export interface User {
  id?: string;
  username: string;
  name: string;
  email: string;
  is_admin: boolean;
}

export interface UserDb extends User {
  password: string;
}

export interface AuthResponse {
  message: string;
  data: {
    access_token: string;
    token_type: string;
    user: User;
  };
}

export interface LoginForm {
  username: string;
  password: string;
}

export interface RegisterForm {
  username: string;
  name: string;
  email: string;
  password: string;
}

// Chatbot Types
export interface ChatbotMessage {
  id: string;
  text: string;
  sender: 'user' | 'bot';
  timestamp: Date;
  cars?: Car[];
  needsClarification?: boolean;
  clarificationQuestion?: string;
}

export interface ChatbotMessageRequest {
  message: string;
  session_id?: string;
}

export interface ChatbotMessageResponse {
  response: string;
  cars: Car[];
  filters_extracted: Record<string, any>;
  needs_clarification: boolean;
  clarification_question?: string;
  session_id: string;
} 