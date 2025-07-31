@echo off
echo Instalando dependencias del frontend...
npm install

echo.
echo Configurando variables de entorno...
echo REACT_APP_API_URL=http://localhost:8000 > .env

echo.
echo Iniciando el servidor de desarrollo...
echo El frontend estara disponible en: http://localhost:3000
echo.
npm start 