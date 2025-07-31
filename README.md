# Concesionario Virtual - Sistema Completo

Un sistema completo de gestión de concesionario de vehículos con backend en FastAPI y frontend en React.

## 🏗️ Arquitectura del Sistema

```
Concesionario/
├── backend/
│   └── FastApi/          # Backend en FastAPI
│       ├── main.py       # Aplicación principal
│       ├── routers/      # Endpoints de la API
│       ├── models/       # Modelos de datos
│       ├── services/     # Lógica de negocio
│       └── db/          # Configuración de base de datos
└── frontend/            # Frontend en React + TypeScript
    ├── src/
    │   ├── components/  # Componentes reutilizables
    │   ├── pages/       # Páginas principales
    │   ├── services/    # Servicios de API
    │   └── contexts/    # Contextos de React
    └── public/          # Archivos estáticos
```

## 🚀 Características Principales

### Backend (FastAPI)
- **Autenticación JWT**: Sistema seguro de login/logout
- **CRUD de Vehículos**: Gestión completa de inventario
- **Historial de Vehículos**: Seguimiento de accidentes y servicios
- **Gestión de Usuarios**: Administración de usuarios del sistema
- **API RESTful**: Endpoints bien documentados
- **CORS habilitado**: Para comunicación con frontend

### Frontend (React + TypeScript)
- **Diseño Moderno**: UI/UX profesional con Tailwind CSS
- **Responsive Design**: Optimizado para todos los dispositivos
- **Autenticación**: Sistema de login con protección de rutas
- **Catálogo de Vehículos**: Listado con filtros avanzados
- **Detalles Completos**: Vista detallada con especificaciones
- **Panel de Administración**: Gestión completa para admins
- **Notificaciones**: Feedback del usuario con toast

## 📋 Prerrequisitos

- **Python 3.8+**
- **Node.js 16+**
- **npm o yarn**

## 🛠️ Instalación y Configuración

### 1. Backend (FastAPI)

```bash
# Navegar al directorio del backend
cd Concesionario/backend/FastApi

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar el servidor
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

El backend estará disponible en: `http://localhost:8000`

### 2. Frontend (React)

```bash
# Navegar al directorio del frontend
cd Concesionario/frontend

# Instalar dependencias
npm install

# Crear archivo de variables de entorno
echo REACT_APP_API_URL=http://localhost:8000 > .env

# Ejecutar en modo desarrollo
npm start
```

El frontend estará disponible en: `http://localhost:3000`

### 3. Scripts Automatizados

#### Windows
```bash
# Backend
cd Concesionario/backend/FastApi
run-backend.bat

# Frontend (en otra terminal)
cd Concesionario/frontend
install-and-run.bat
```

#### Linux/Mac
```bash
# Backend
cd Concesionario/backend/FastApi
chmod +x run-backend.sh
./run-backend.sh

# Frontend (en otra terminal)
cd Concesionario/frontend
chmod +x install-and-run.sh
./install-and-run.sh
```

## 🔧 Configuración de Base de Datos

El sistema utiliza una base de datos en memoria por defecto. Para producción, configurar una base de datos persistente:

```python
# En db/client.py
DATABASE_URL = "sqlite:///./concesionario.db"  # SQLite
# o
DATABASE_URL = "postgresql://user:password@localhost/dbname"  # PostgreSQL
```

## 📊 Endpoints de la API

### Autenticación
- `POST /auth/login` - Iniciar sesión
- `GET /auth/me` - Obtener usuario actual
- `GET /auth/logout` - Cerrar sesión

### Vehículos
- `GET /cars/` - Listar todos los vehículos
- `POST /cars/newcar` - Crear nuevo vehículo
- `PUT /cars/updatecar/{id}` - Actualizar vehículo
- `DELETE /cars/deletecar/{id}` - Eliminar vehículo

### Historial de Vehículos
- `GET /carhistory/?car_id={id}` - Obtener historial
- `POST /carhistory/newcarhistory` - Crear historial
- `PUT /carhistory/updatecarhistory/{id}` - Actualizar historial
- `DELETE /carhistory/deletecarhistory/{id}` - Eliminar historial

## 🎨 Funcionalidades del Frontend

### Páginas Principales
1. **Inicio** (`/`): Hero section con vehículos destacados
2. **Catálogo** (`/cars`): Lista completa con filtros
3. **Detalles** (`/cars/:id`): Vista detallada del vehículo
4. **Login** (`/login`): Autenticación de usuarios
5. **Admin** (`/admin`): Panel de administración

### Características Especiales
- **Búsqueda Avanzada**: Por marca, modelo, color
- **Filtros Dinámicos**: Por año, precio, estado
- **Vista Responsive**: Grid y lista
- **Historial Completo**: Accidentes, servicios, propietarios
- **Gestión de Estados**: Disponible/Vendido

## 🔐 Autenticación y Seguridad

### Roles de Usuario
- **Usuario Regular**: Ver catálogo y detalles
- **Administrador**: Acceso completo al sistema

### Protección de Rutas
- Rutas públicas: `/`, `/cars`, `/cars/:id`
- Rutas protegidas: `/admin` (solo admins)

## 📱 Diseño Responsive

### Breakpoints
- **Móvil**: < 768px
- **Tablet**: 768px - 1024px
- **Desktop**: > 1024px

### Componentes Adaptativos
- Header con menú hamburguesa
- Grid de vehículos responsive
- Formularios optimizados para móvil

## 🚀 Deployment

### Backend (Producción)
```bash
# Instalar gunicorn
pip install gunicorn

# Ejecutar con gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Frontend (Producción)
```bash
# Build de producción
npm run build

# Servir con nginx o similar
npx serve -s build
```

## 🧪 Testing

### Backend
```bash
# Instalar pytest
pip install pytest

# Ejecutar tests
pytest
```

### Frontend
```bash
# Ejecutar tests
npm test

# Coverage
npm test -- --coverage
```

## 📈 Monitoreo y Logs

### Backend
- Logs automáticos de FastAPI
- Middleware de CORS configurado
- Manejo de errores centralizado

### Frontend
- React DevTools para debugging
- Console logs para desarrollo
- Error boundaries para producción

## 🔧 Configuración Avanzada

### Variables de Entorno

#### Backend (.env)
```env
DATABASE_URL=sqlite:///./concesionario.db
SECRET_KEY=tu_clave_secreta_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

#### Frontend (.env)
```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_ENVIRONMENT=development
```

### Personalización de Estilos

El frontend utiliza Tailwind CSS con configuración personalizada:

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          // ... más colores
        }
      }
    }
  }
}
```

## 🤝 Contribución

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🆘 Soporte

Para soporte técnico o preguntas:
- Crear un issue en el repositorio
- Contactar al equipo de desarrollo
- Revisar la documentación de la API

## 🎯 Roadmap

### Próximas Funcionalidades
- [ ] Sistema de reservas
- [ ] Notificaciones en tiempo real
- [ ] Integración con pasarelas de pago
- [ ] App móvil nativa
- [ ] Dashboard de analytics
- [ ] Sistema de reviews y ratings

### Mejoras Técnicas
- [ ] Cache con Redis
- [ ] Tests automatizados
- [ ] CI/CD pipeline
- [ ] Docker containers
- [ ] Microservicios

---

**Desarrollado con ❤️ para Concesionario Virtual**

*Un sistema moderno y completo para la gestión de concesionarios de vehículos.* 