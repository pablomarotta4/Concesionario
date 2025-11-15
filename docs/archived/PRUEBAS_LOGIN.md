# 🧪 Pruebas de Login - Verificación Final

## Estado de los Servicios

✅ **Backend**: http://localhost:8000 (Running)
✅ **Frontend**: http://localhost:3000 (Running)  
✅ **MongoDB**: Port 27017 (Running)

---

## 1️⃣ Prueba de API (Backend - Terminal)

```bash
curl -X POST http://localhost:8000/auth/login \
  -d "username=admin&password=admin123" \
  -H "Content-Type: application/x-www-form-urlencoded"
```

**Respuesta esperada**:
```json
{
  "message": "Login successful",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
  }
}
```

**Status**: ✅ Funcionando correctamente

---

## 2️⃣ Prueba de Frontend (Navegador)

### Pasos:
1. Abre http://localhost:3000 en tu navegador
2. Deberías ver la página de Login
3. Intenta loguearte con:
   - **Usuario**: `admin`
   - **Contraseña**: `admin123`

### Si funciona:
- ✅ Serás redirigido al dashboard
- ✅ El token se guardará en localStorage
- ✅ Podrás ver los autos disponibles

### Si no funciona:
- Abre DevTools (F12)
- Ve a la pestaña "Network"
- Haz click en "Login"
- Busca la solicitud POST a `/auth/login`
- Verifica:
  - **Status code**: 200 ✅
  - **Response**: Contiene `access_token` ✅

---

## 3️⃣ Otros usuarios para probar

```
1. Usuario: pmarotta
   Contraseña: password123
   Rol: Usuario regular

2. Usuario: jperez
   Contraseña: password123
   Rol: Usuario regular

3. Usuario: mgarcia
   Contraseña: password123
   Rol: Usuario regular

4. Usuario: lrodriguez
   Contraseña: password123
   Rol: Administrador
```

---

## 4️⃣ Pruebas de Endpoints Protegidos

Una vez logueado, prueba estos endpoints en Postman o curl:

### Obtener información del usuario actual:
```bash
curl -X GET http://localhost:8000/auth/me \
  -H "Authorization: Bearer <YOUR_TOKEN>"
```

### Obtener lista de autos:
```bash
curl -X GET http://localhost:8000/cars
```

### Obtener histórico de usuario:
```bash
curl -X GET http://localhost:8000/carhistory \
  -H "Authorization: Bearer <YOUR_TOKEN>"
```

---

## 🔍 Verificación de Base de Datos

Para verificar que los usuarios están en la base de datos:

```bash
# Conectarse a MongoDB con autenticación
docker-compose exec mongodb mongosh -u admin -p changeme123 \
  --authenticationDatabase admin concesionario \
  --eval "db.users.find().pretty()"
```

**Deberías ver**:
- 5 documentos de usuarios
- Campo `password` con hash que empieza con `$2b$`
- Campos: `username`, `name`, `email`, `is_admin`

---

## ✅ Checklist de Verificación

- [ ] Backend reiniciado y corriendo
- [ ] Seed ejecutado (datos en BD)
- [ ] Login funciona por API (curl)
- [ ] Frontend carga sin errores
- [ ] Login funciona desde frontend
- [ ] Token se guarda en localStorage
- [ ] Puedo acceder a endpoints protegidos
- [ ] Puedo ver lista de autos
- [ ] Puedo ver histórico personal

---

## 🆘 Troubleshooting Rápido

### "Usuario no encontrado" o "Contraseña incorrecta"
```bash
# 1. Reiniciar backend
docker-compose restart backend

# 2. Limpiar base de datos y reejecutar seed
docker-compose down -v
docker-compose up -d
make seed
```

### CORS Error en Frontend
- Verifica que main.py tenga CORS configurado correctamente
- El backend debería aceptar requests desde http://localhost:3000

### Token no se guarda
- Abre DevTools → Application → LocalStorage
- Verifica que haya una entrada `token` con el JWT

### 404 en /auth/login
- Verifica que el router JWT está incluido en main.py
- Reinicia el backend: `docker-compose restart backend`

---

## 📊 Resumen de Cambios

| Archivo | Cambio | Estado |
|---------|--------|--------|
| db/client.py | Base de datos correcta + autenticación | ✅ |
| services/user_service.py | get_database() + bcrypt config | ✅ |
| services/auth_service.py | bcrypt deprecated="auto" | ✅ |
| seed_database.py | Hash con rounds=12 | ✅ |
| routers/jwt_auth_router.py | Respuesta formateada | ✅ |
| frontend/src/services/api.ts | Expecta respuesta JSON | ✅ |

---

## 🎯 Próximas Acciones

1. **Inmediato**: Prueba el login desde el navegador
2. **Si hay error**: Verifica DevTools → Network
3. **Si persiste**: Revisa los logs del backend
4. **Final**: Actualiza este documento con resultados

