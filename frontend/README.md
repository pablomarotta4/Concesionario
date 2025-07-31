# Concesionario Virtual - Frontend

Un frontend moderno y responsive para el sistema de gestión de concesionario de vehículos, construido con React, TypeScript y Tailwind CSS.

## 🚀 Características

### Funcionalidades Principales
- **Página de Inicio**: Hero section con vehículos destacados y características del concesionario
- **Catálogo de Vehículos**: Lista completa con filtros avanzados y búsqueda
- **Detalles de Vehículos**: Vista detallada con especificaciones técnicas e historial
- **Sistema de Autenticación**: Login seguro con JWT
- **Panel de Administración**: Gestión completa de vehículos y usuarios
- **Diseño Responsive**: Optimizado para móviles, tablets y desktop

### Tecnologías Utilizadas
- **React 18** con TypeScript
- **React Router** para navegación
- **Tailwind CSS** para estilos
- **Lucide React** para iconos
- **React Hook Form** para formularios
- **React Hot Toast** para notificaciones
- **Axios** para API calls

## 📦 Instalación

1. **Clonar el repositorio**
```bash
cd Concesionario/frontend
```

2. **Instalar dependencias**
```bash
npm install
```

3. **Configurar variables de entorno**
Crear un archivo `.env` en la raíz del proyecto:
```env
REACT_APP_API_URL=http://localhost:8000
```

4. **Ejecutar en modo desarrollo**
```bash
npm start
```

El frontend estará disponible en `http://localhost:3000`

## 🏗️ Estructura del Proyecto

```
src/
├── components/          # Componentes reutilizables
│   └── Layout/         # Componentes de layout (Header, Footer)
├── contexts/           # Contextos de React (AuthContext)
├── pages/              # Páginas principales
├── services/           # Servicios de API
├── types/              # Definiciones de TypeScript
├── App.tsx            # Componente principal
└── index.tsx          # Punto de entrada
```

## 🎨 Diseño y UX

### Paleta de Colores
- **Primario**: Azul (#3B82F6)
- **Secundario**: Gris (#64748B)
- **Éxito**: Verde (#10B981)
- **Error**: Rojo (#EF4444)
- **Advertencia**: Amarillo (#F59E0B)

### Componentes Principales

#### Header
- Logo y navegación principal
- Menú de usuario con dropdown
- Navegación responsive para móviles

#### Footer
- Información de contacto
- Enlaces rápidos
- Redes sociales

#### Cards de Vehículos
- Imagen del vehículo
- Información básica (marca, modelo, año)
- Precio destacado
- Estado de disponibilidad
- Botones de acción

## 🔐 Autenticación

El sistema utiliza JWT para la autenticación:

- **Login**: Formulario con validación
- **Protección de rutas**: Componente `ProtectedRoute`
- **Contexto de autenticación**: `AuthContext`
- **Interceptores de Axios**: Manejo automático de tokens

## 📱 Responsive Design

El frontend está completamente optimizado para:

- **Móviles** (< 768px)
- **Tablets** (768px - 1024px)
- **Desktop** (> 1024px)

### Breakpoints
- `sm`: 640px
- `md`: 768px
- `lg`: 1024px
- `xl`: 1280px
- `2xl`: 1536px

## 🚗 Funcionalidades de Vehículos

### Listado
- Vista en grid y lista
- Filtros por marca, año y precio
- Búsqueda por texto
- Paginación automática

### Detalles
- Galería de imágenes
- Especificaciones técnicas completas
- Historial del vehículo
- Información de contacto

### Administración
- CRUD completo de vehículos
- Gestión de estados
- Estadísticas en tiempo real

## 🔧 Configuración

### Variables de Entorno
```env
REACT_APP_API_URL=http://localhost:8000
```

### Tailwind CSS
El proyecto incluye configuración personalizada de Tailwind con:
- Paleta de colores personalizada
- Componentes reutilizables
- Animaciones personalizadas

### API Configuration
```typescript
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
```

## 📊 Estado de la Aplicación

### Contextos
- **AuthContext**: Manejo de autenticación y usuario
- **Toast notifications**: Feedback del usuario
- **Loading states**: Estados de carga

### Rutas Protegidas
- `/admin`: Solo usuarios administradores
- `/cars/:id`: Público
- `/`: Público

## 🎯 Optimizaciones

### Performance
- Lazy loading de imágenes
- Code splitting automático
- Optimización de bundle

### SEO
- Meta tags dinámicos
- URLs amigables
- Sitemap automático

### Accesibilidad
- ARIA labels
- Navegación por teclado
- Contraste adecuado

## 🚀 Deployment

### Build de Producción
```bash
npm run build
```

### Servir Build
```bash
npx serve -s build
```

## 🔍 Testing

### Ejecutar Tests
```bash
npm test
```

### Coverage
```bash
npm test -- --coverage
```

## 📝 Scripts Disponibles

- `npm start`: Ejecutar en modo desarrollo
- `npm build`: Build de producción
- `npm test`: Ejecutar tests
- `npm eject`: Eject de Create React App

## 🤝 Contribución

1. Fork el proyecto
2. Crear una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abrir un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

## 🆘 Soporte

Para soporte técnico o preguntas, contactar al equipo de desarrollo.

---

**Desarrollado con ❤️ para Concesionario Virtual** 