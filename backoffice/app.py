import streamlit as st
import requests
import json
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Configuración de la API
API_URL = "http://localhost:8000"  # URL de tu API FastAPI

# Función para manejar el login
def login(username: str, password: str):
    try:
        response = requests.post(
            f"{API_URL}/auth/login",
            data={"username": username, "password": password}
        )
        if response.status_code == 200:
            result = response.json()
            if result.get("data", {}).get("access_token"):
                return result["data"]
        return None
    except Exception as e:
        st.error(f"Error al conectar con la API: {str(e)}")
        return None

# Función para obtener la lista de autos
def get_cars(token: str):
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{API_URL}/cars/", headers=headers)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        st.error(f"Error al obtener los autos: {str(e)}")
        return []

# Función para crear un auto
def create_car(token: str, car_data: dict):
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(
            f"{API_URL}/cars/newcar",
            json=car_data,
            headers=headers
        )
        return response.status_code == 200
    except Exception as e:
        st.error(f"Error al crear el auto: {str(e)}")
        return False

# Función para actualizar un auto
def update_car(token: str, car_id: str, car_data: dict):
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.put(
            f"{API_URL}/cars/updatecar/{car_id}",
            json=car_data,
            headers=headers
        )
        return response.status_code == 200
    except Exception as e:
        st.error(f"Error al actualizar el auto: {str(e)}")
        return False

# Página de login
def login_page():
    st.title("Backoffice - Login")
    
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    
    if st.button("Iniciar sesión"):
        if username and password:
            result = login(username, password)
            if result:
                st.session_state.token = result["access_token"]
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Credenciales inválidas")
        else:
            st.warning("Por favor ingrese usuario y contraseña")

# Página principal del backoffice
def main_page():
    # Configuración de la sidebar
    with st.sidebar:
        st.title("Menú")
        selected_option = st.radio(
            "Seleccione una opción",
            ["Lista de Autos", "Gestión de Usuarios", "Configuración"]
        )
        
        # Botón de cerrar sesión en la parte inferior de la sidebar
        st.sidebar.markdown("---")
        if st.sidebar.button("Cerrar Sesión"):
            st.session_state.logged_in = False
            st.rerun()
    
    st.title("Backoffice - Gestión de Autos")
    
    # Mostrar contenido según la opción seleccionada
    if selected_option == "Lista de Autos":
        # Botón para mostrar/ocultar el formulario de crear auto
        show_create_form = st.expander("Crear Nuevo Auto", expanded=False)
        
        with show_create_form:
            with st.form(key="create_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Información Básica**")
                    new_brand = st.text_input("Marca")
                    new_model = st.text_input("Modelo")
                    new_year = st.number_input("Año")
                    new_color = st.text_input("Color")
                    new_price = st.number_input("Precio")
                    new_is_available = st.checkbox("Disponible", value=True)
                    new_mileage = st.number_input("Kilometraje")
                    
                with col2:
                    st.write("**Especificaciones Técnicas**")
                    new_engine_type = st.text_input("Tipo de Motor")
                    new_transmission = st.text_input("Transmisión")
                    new_fuel_type = st.text_input("Tipo de Combustible")
                    new_doors = st.number_input("Puertas")
                    new_seats = st.number_input("Asientos")
                    new_max_speed = st.number_input("Velocidad Máxima")
                    new_acceleration = st.number_input("Aceleración (0-100 km/h)")
                    new_horsepower = st.number_input("Potencia (HP)")
                    new_torque = st.number_input("Torque (Nm)")
                
                st.write("**Dimensiones**")
                col3, col4 = st.columns(2)
                with col3:
                    new_weight = st.number_input("Peso (kg)")
                    new_length = st.number_input("Largo (m)")
                    new_width = st.number_input("Ancho (m)")
                
                with col4:
                    st.write("**Información Adicional**")
                    new_description = st.text_area("Descripción")
                    new_payment_method = st.text_input("Método de Pago")
                    new_image_url = st.text_input("URL de la Imagen")
                
                if st.form_submit_button("Crear Auto"):
                    car_data = {
                        "brand": new_brand,
                        "model": new_model,
                        "year": new_year,
                        "color": new_color,
                        "price": new_price,
                        "is_available": new_is_available,
                        "mileage": new_mileage,
                        "engine_type": new_engine_type,
                        "transmission": new_transmission,
                        "fuel_type": new_fuel_type,
                        "doors": new_doors,
                        "seats": new_seats,
                        "max_speed": new_max_speed,
                        "acceleration": new_acceleration,
                        "horsepower": new_horsepower,
                        "torque": new_torque,
                        "weight": new_weight,
                        "length": new_length,
                        "width": new_width,
                        "description": new_description,
                        "paymenth_method": new_payment_method,
                        "image_url": new_image_url
                    }
                    if create_car(st.session_state.token, car_data):
                        st.success("Auto creado correctamente")
                        st.rerun()
                    else:
                        st.error("Error al crear el auto")
        
        # Mostrar lista de autos
        cars = get_cars(st.session_state.token)
        
        if cars:
            st.subheader("Lista de Autos")
            # Agregar búsqueda
            search = st.text_input("Buscar auto", "")
            
            for car in cars:
                # Filtrar por búsqueda
                if search.lower() in f"{car.get('brand', '')} {car.get('model', '')}".lower():
                    with st.expander(f"{car.get('brand', '')} {car.get('model', '')}"):
                        # Mostrar detalles del auto
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write("**Información Básica**")
                            st.write(f"ID: {car.get('id', '')}")
                            st.write(f"Marca: {car.get('brand', '')}")
                            st.write(f"Modelo: {car.get('model', '')}")
                            st.write(f"Año: {car.get('year', '')}")
                            st.write(f"Color: {car.get('color', '')}")
                            st.write(f"Precio: ${car.get('price', 0):,.2f}")
                            st.write(f"Disponible: {'Sí' if car.get('is_available', False) else 'No'}")
                            st.write(f"Kilometraje: {car.get('mileage', 0)} km")
                            
                        with col2:
                            st.write("**Especificaciones Técnicas**")
                            st.write(f"Motor: {car.get('engine_type', '')}")
                            st.write(f"Transmisión: {car.get('transmission', '')}")
                            st.write(f"Combustible: {car.get('fuel_type', '')}")
                            st.write(f"Puertas: {car.get('doors', 0)}")
                            st.write(f"Asientos: {car.get('seats', 0)}")
                            st.write(f"Velocidad Máxima: {car.get('max_speed', 'N/A')} km/h")
                            st.write(f"Aceleración: {car.get('acceleration', 0)} s (0-100 km/h)")
                            st.write(f"Potencia: {car.get('horsepower', 0)} HP")
                            st.write(f"Torque: {car.get('torque', 0)} Nm")
                        
                        st.write("**Dimensiones**")
                        col3, col4 = st.columns(2)
                        with col3:
                            st.write(f"Peso: {car.get('weight', 0)} kg")
                            st.write(f"Largo: {car.get('length', 0)} m")
                            st.write(f"Ancho: {car.get('width', 0)} m")
                        
                        with col4:
                            st.write("**Información Adicional**")
                            st.write(f"Descripción: {car.get('description', '')}")
                            st.write(f"Método de Pago: {car.get('paymenth_method', '')}")
                            if car.get('image_url'):
                                st.image(car.get('image_url'), width=200)
                        
                        # Formulario para editar auto
                        with st.form(key=f"edit_form_{car.get('id', '')}"):
                            st.subheader("Editar Auto")
                            
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.write("**Información Básica**")
                                new_brand = st.text_input("Marca", value=car.get('brand', ''))
                                new_model = st.text_input("Modelo", value=car.get('model', ''))
                                new_year = st.number_input("Año", value=car.get('year', 0))
                                new_color = st.text_input("Color", value=car.get('color', ''))
                                new_price = st.number_input("Precio", value=car.get('price', 0))
                                new_is_available = st.checkbox("Disponible", value=car.get('is_available', False))
                                new_mileage = st.number_input("Kilometraje", value=car.get('mileage', 0))
                                
                            with col2:
                                st.write("**Especificaciones Técnicas**")
                                new_engine_type = st.text_input("Tipo de Motor", value=car.get('engine_type', ''))
                                new_transmission = st.text_input("Transmisión", value=car.get('transmission', ''))
                                new_fuel_type = st.text_input("Tipo de Combustible", value=car.get('fuel_type', ''))
                                new_doors = st.number_input("Puertas", value=car.get('doors', 0))
                                new_seats = st.number_input("Asientos", value=car.get('seats', 0))
                                new_max_speed = st.number_input("Velocidad Máxima", value=car.get('max_speed', 0))
                                new_acceleration = st.number_input("Aceleración (0-100 km/h)", value=car.get('acceleration', 0))
                                new_horsepower = st.number_input("Potencia (HP)", value=car.get('horsepower', 0))
                                new_torque = st.number_input("Torque (Nm)", value=car.get('torque', 0))
                            
                            st.write("**Dimensiones**")
                            col3, col4 = st.columns(2)
                            with col3:
                                new_weight = st.number_input("Peso (kg)", value=car.get('weight', 0))
                                new_length = st.number_input("Largo (m)", value=car.get('length', 0))
                                new_width = st.number_input("Ancho (m)", value=car.get('width', 0))
                            
                            with col4:
                                st.write("**Información Adicional**")
                                new_description = st.text_area("Descripción", value=car.get('description', ''))
                                new_payment_method = st.text_input("Método de Pago", value=car.get('paymenth_method', ''))
                                new_image_url = st.text_input("URL de la Imagen", value=car.get('image_url', ''))
                            
                            if st.form_submit_button("Actualizar"):
                                car_data = {
                                    "brand": new_brand,
                                    "model": new_model,
                                    "year": new_year,
                                    "color": new_color,
                                    "price": new_price,
                                    "is_available": new_is_available,
                                    "mileage": new_mileage,
                                    "engine_type": new_engine_type,
                                    "transmission": new_transmission,
                                    "fuel_type": new_fuel_type,
                                    "doors": new_doors,
                                    "seats": new_seats,
                                    "max_speed": new_max_speed,
                                    "acceleration": new_acceleration,
                                    "horsepower": new_horsepower,
                                    "torque": new_torque,
                                    "weight": new_weight,
                                    "length": new_length,
                                    "width": new_width,
                                    "description": new_description,
                                    "paymenth_method": new_payment_method,
                                    "image_url": new_image_url
                                }
                                if update_car(st.session_state.token, car.get('id', ''), car_data):
                                    st.success("Auto actualizado correctamente")
                                    st.rerun()
                                else:
                                    st.error("Error al actualizar el auto")
    
    elif selected_option == "Gestión de Usuarios":
        st.write("Sección de Gestión de Usuarios - En desarrollo")
    
    elif selected_option == "Configuración":
        st.write("Sección de Configuración - En desarrollo")

# Configuración inicial de la sesión
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Renderizar la página correspondiente
if not st.session_state.logged_in:
    login_page()
else:
    main_page() 