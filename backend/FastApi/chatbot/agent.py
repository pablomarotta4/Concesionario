
class ConversationalAgent:
    """
    Agente conversacional que gestiona el perfil del usuario, hace preguntas y recomienda autos.
    """
    def __init__(self):
        # Perfil del usuario que se irá completando (basado en los campos de tu modelo Car)
        self.user_profile = {
            "brand": None,           # Toyota, BMW, Honda, etc.
            "model": None,           # Corolla, Civic, etc.
            "year": None,            # 2020, 2021, etc.
            "color": None,           # Plateado, Rojo, Azul, etc.
            "price": None,           # Presupuesto máximo del usuario
            "mileage": None,         # Kilometraje preferido
            "engine_type": None,     # "2.0L 4-Cylinder", "V6", etc.
            "transmission": None,    # Manual, Automatic
            "fuel_type": None,       # Gasolina, Diesel, Híbrido
            "doors": None,           # 2, 4, 5
            "seats": None,           # 2, 4, 5, 7
            "horsepower": None,      # Potencia deseada (rango)
            "paymenth_method": None  # Contado, Financiamiento
        }
        # Orden de preguntas (empezamos con lo más básico)
        self.fields_order = [
            "brand", "model", "year", "color", "price", 
            "transmission", "fuel_type", "doors", "seats"
        ]

    def get_missing_field(self):
        """Devuelve el primer campo faltante en el perfil del usuario."""
        for field in self.fields_order:
            if not self.user_profile.get(field):
                return field
        return None

    def generate_question(self, field):
        preguntas = {
            "brand": "¿Tienes alguna marca preferida? (Toyota, BMW, Honda, etc.)",
            "model": "¿Qué modelo buscas? (Corolla, Civic, etc.)",
            "year": "¿De qué año te gustaría el auto? (2020, 2021, etc.)",
            "color": "¿Qué color prefieres? (Plateado, Rojo, Azul, etc.)",
            "price": "¿Cuál es tu presupuesto máximo?",
            "transmission": "¿Prefieres transmisión manual o automática?",
            "fuel_type": "¿Qué tipo de combustible prefieres? (Gasolina, Diesel, Híbrido)",
            "doors": "¿Cuántas puertas necesitas? (2, 4, 5)",
            "seats": "¿Para cuántas personas? (2, 4, 5, 7 asientos)",
            "mileage": "¿Te importa el kilometraje? ¿Prefieres bajo kilometraje?",
            "engine_type": "¿Qué tipo de motor prefieres? (4-cilindros, V6, etc.)",
            "horsepower": "¿Te interesa un auto potente o más económico?",
            "paymenth_method": "¿Cómo planeas pagar? (Contado o Financiamiento)"
        }
        return preguntas.get(field, f"¿Podrías especificar {field}?")

    def update_profile(self, field, value):
        self.user_profile[field] = value

    def handle_message(self, message):
        """
        Procesa el mensaje del usuario, actualiza el perfil y decide la siguiente acción.
        (Por ahora, la extracción de entidades es manual/simulada)
        """
        # Simulación: el usuario responde directamente al campo que falta
        missing = self.get_missing_field()
        if missing:
            self.update_profile(missing, message)
            next_missing = self.get_missing_field()
            if next_missing:
                return self.generate_question(next_missing)
            else:
                # Cuando el perfil está completo, llamamos a la función de recomendación
                return self.get_recommendations()
        else:
            return "¡Ya tengo toda la información necesaria!"
    
    def get_recommendations(self):
        """
        Cuando el perfil del usuario está completo, busca y recomienda autos afines.
        """
        # Aquí integraremos el vectorizador para comparar el user_profile con los autos de la DB
        # Por ahora, devolvemos un mensaje de ejemplo
        profile_summary = ", ".join([f"{k}: {v}" for k, v in self.user_profile.items() if v is not None])
        return f"¡Perfecto! Basándome en tus preferencias ({profile_summary}), te mostraré los autos más recomendados. [Aquí se integraría el vectorizador]"
    
    def reset_profile(self):
        """Reinicia el perfil del usuario para una nueva búsqueda."""
        for key in self.user_profile:
            self.user_profile[key] = None
