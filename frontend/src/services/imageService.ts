const API_BASE_URL = 'http://localhost:8000';

export const getImageUrl = (imagePath: string | null | undefined): string => {
  if (!imagePath) {
    return '/placeholder-car.jpg';
  }
  
  // Si la imagen ya es una URL completa, la devolvemos tal como está
  if (imagePath.startsWith('http://') || imagePath.startsWith('https://')) {
    return imagePath;
  }
  
  // Si es una ruta relativa, la construimos con el backend
  return `${API_BASE_URL}/static/img/${imagePath}`;
};

export const getCarImageUrl = (car: any): string => {
  if (car.image_url) {
    return getImageUrl(car.image_url);
  }
  
  // Si no hay imagen específica, usar placeholder
  return '/placeholder-car.jpg';
}; 