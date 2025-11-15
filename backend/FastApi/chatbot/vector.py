from sentence_transformers import SentenceTransformer, InputExample, losses, models
from sklearn.metrics.pairwise import cosine_similarity
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from sentence_transformers.losses import MSELoss    
import numpy as np
import pandas as pd
import warnings
import os
from datetime import datetime
warnings.filterwarnings("ignore")

# class PreferenceExtractor:
#     def __init__(self, model_name='all-MiniLM-L6-v2'):
#         # Usar Sentence Transformers para mejores embeddings
#         self.model = SentenceTransformer(model_name)

#         self.TEMPLATES = {
#                     "price_high": [
#                         "quiero un auto económico y barato",
#                         "busco algo con buen precio y asequible", 
#                         "necesito ahorrar dinero en la compra",
#                         "presupuesto limitado para auto económico",
#                         "auto barato que no cueste mucho",
#                         "precio bajo es mi prioridad",
#                         "economía de precio es importante"
#                     ],
#                     "price_low": [
#                         "no me importa el precio del auto",
#                         "quiero algo premium sin restricciones de precio",
#                         "busco lujo y exclusividad costosa",
#                         "precio no es problema",
#                         "puedo pagar lo que sea necesario",
#                         "dinero no es obstáculo"
#                     ],
#                     "price_medium": [
#                         "busco un auto con buen balance entre precio y calidad",
#                         "quiero algo ni muy caro ni muy barato",
#                         "precio razonable con buenas prestaciones",
#                         "algo en el rango medio de precios",
#                         "calidad y precio equilibrados",
#                         "busco valor por mi dinero"
#                     ],
#                     "power_high": [
#                         "quiero un auto potente y deportivo",
#                         "busco velocidad y aceleración rápida",
#                         "necesito mucha potencia y performance",
#                         "auto deportivo con motor turbo potente",
#                         "motor V8 con mucha fuerza",
#                         "velocidad y potencia son clave",
#                         "aceleración rápida es importante"
#                     ],
#                     "power_low": [
#                         "no necesito mucha potencia en el auto",
#                         "busco algo tranquilo para ciudad",
#                         "economía de combustible más importante que potencia",
#                         "motor básico está bien",
#                         "no busco velocidad ni deportividad",
#                         "uso urbano simple"
#                     ],
#                     "power_medium": [
#                         "busco un auto con buena potencia sin ser extremo",
#                         "quiero algo equilibrado en potencia y eficiencia",
#                         "no necesito un deportivo, pero sí algo ágil",
#                         "potencia moderada para uso diario",
#                         "algo que responda bien sin ser un V8",
#                         "busco un motor que no sea básico pero tampoco excesivo"
#                     ],
#                     "efficiency_high": [
#                         "quiero un auto eficiente y ecológico",
#                         "busco bajo consumo de combustible",
#                         "necesito híbrido o eléctrico sustentable",
#                         "ahorro en gasolina es importante",
#                         "consumo mínimo de combustible",
#                         "ecología y eficiencia prioritarias",
#                         "auto verde y sustentable"
#                     ],
#                     "efficiency_low": [
#                         "no me importa el consumo de combustible",
#                         "performance es más importante que eficiencia",
#                         "gasolina no es problema",
#                         "consumo alto no me molesta"
#                     ],
#                     "efficiency_medium": [
#                         "busco un auto con buen equilibrio entre potencia y eficiencia",
#                         "quiero algo que no consuma mucho pero tenga buena performance",
#                         "eficiencia moderada es aceptable",
#                         "algo que ahorre combustible sin sacrificar potencia",
#                         "equilibrio entre consumo y rendimiento",
#                         "busco un auto que no sea derrochador pero tampoco básico"
#                     ],
#                     "size_high": [
#                         "necesito un auto grande para familia",
#                         "busco espacioso con muchos asientos",
#                         "SUV grande para 7 personas",
#                         "auto familiar amplio y cómodo",
#                         "espacio para toda la familia",
#                         "necesito mucho lugar interior",
#                         "van o SUV grande"
#                     ],
#                     "size_low": [
#                         "quiero algo compacto y pequeño",
#                         "auto deportivo de 2 asientos",
#                         "fácil de estacionar en ciudad",
#                         "auto pequeño y ágil",
#                         "compacto para uso urbano",
#                         "no necesito mucho espacio"
#                     ],
#                     "size_medium": [
#                         "busco un auto mediano, ni muy grande ni muy pequeño",
#                         "quiero algo con buen equilibrio entre espacio y maniobrabilidad",
#                         "auto familiar compacto",
#                         "espacio suficiente sin ser un SUV grande",
#                         "algo que sea práctico pero no enorme",
#                         "tamaño intermedio para uso diario"
#                     ],
#                     "brand_high": [
#                         "quiero una marca premium y reconocida",
#                         "busco lujo y prestigio en la marca",
#                         "marca exclusiva y de alta gama",
#                         "BMW, Mercedes, Audi son importantes",
#                         "prestigio de marca es clave",
#                         "marca de lujo es prioritaria"
#                     ],
#                     "brand_low": [
#                         "no me importa la marca del auto",
#                         "funcionalidad más importante que prestigio",
#                         "cualquier marca está bien",
#                         "no busco status ni prestigio"
#                     ],
#                     "brand_medium": [
#                         "busco una marca confiable pero no necesariamente de lujo",
#                         "quiero algo con buena reputación sin ser premium",
#                         "marca reconocida pero accesible",
#                         "equilibrio entre calidad y precio en la marca",
#                         "algo popular y bien valorado",
#                         "marca con buena relación calidad-precio"
#                     ]
#                 }
        
#         # Pre-calcular embeddings de templates
#         self._precompute_template_embeddings()
#         self.threshold = 0.5  # Umbral de similitud para considerar una preferencia relevante
        
#     def _precompute_template_embeddings(self):
#         """Pre-calcula los embeddings de todos los templates para optimizar"""
#         self.template_embeddings = {}
        
#         for category, templates in self.TEMPLATES.items():
#             # Calcular embedding promedio para cada categoría
#             embeddings = self.model.encode(templates)
#             avg_embedding = np.mean(embeddings, axis=0)
#             self.template_embeddings[category] = avg_embedding
#             print(f"Template '{category}' embedding shape: {avg_embedding.shape}")  # Debugging line

#     def extract_preferences(self, user_input: str) -> dict:
#         """
#         Extrae las preferencias del usuario basado en su input
        
#         Args:
#             user_input: Texto del usuario describiendo lo que busca
            
#         Returns:
#             dict: Scores de preferencias (0-1) para cada categoría
#         """
#         # Codificar el input del usuario
#         user_embedding = self.model.encode([user_input])[0]
        
#         scores = {}
        
#         # Calcular scores para cada dimensión
#         for dimension in ['price', 'power', 'efficiency', 'size', 'brand']:
#             # Calcular similitud en cada nivel
#             high_key = f"{dimension}_high"
#             low_key = f"{dimension}_low"
#             medium_key = f"{dimension}_medium"

#             high_similarity = cosine_similarity(
#                 [user_embedding], 
#                 [self.template_embeddings[high_key]]
#             )[0][0]
#             low_similarity = cosine_similarity(
#                 [user_embedding], 
#                 [self.template_embeddings[low_key]]
#             )[0][0]
#             medium_similarity = cosine_similarity(
#                 [user_embedding], 
#                 [self.template_embeddings[medium_key]]
#             )[0][0]


#             # Normalizar score entre 0 y 1 con mejor discriminación
#             total_sim = high_similarity + low_similarity + medium_similarity
#             if total_sim > 0:
#                 score = (high_similarity + 0.5 * medium_similarity) / total_sim
#             else:
#                 score = 0.5  # Neutral si no hay similitud

#             scores[f"{dimension}_score"] = round(score, 3)

#         return scores

#     def get_preference_vector(self, user_input: str) -> np.ndarray:
#         """
#         Retorna un vector numpy con los 5 scores de preferencias
        
#         Args:
#             user_input: Texto del usuario
            
#         Returns:
#             np.ndarray: Vector de 5 dimensiones [price, power, efficiency, size, brand]
#         """
#         preferences = self.extract_preferences(user_input)
        
#         return np.array([
#             preferences['price_score'],
#             preferences['power_score'], 
#             preferences['efficiency_score'],
#             preferences['size_score'],
#             preferences['brand_score']
#         ])

#     def analyze_user_input(self, user_input: str) -> dict:
#         """
#         Análisis completo del input del usuario
        
#         Args:
#             user_input: Texto del usuario
            
#         Returns:
#             dict: Análisis completo con scores y interpretación
#         """
#         preferences = self.extract_preferences(user_input)
#         vector = self.get_preference_vector(user_input)
        
#         # Interpretación de scores
#         interpretation = {}
#         for key, score in preferences.items():
#             dimension = key.replace('_score', '')
#             if score >= 0.65:
#                 interpretation[dimension] = "Alta preferencia"
#             elif score >= 0.35:
#                 interpretation[dimension] = "Preferencia moderada"
#             else:
#                 interpretation[dimension] = "Baja preferencia"
        
#         return {
#             'user_input': user_input,
#             'preference_scores': preferences,
#             'preference_vector': vector.tolist(),
#             'interpretation': interpretation
#         }

# # Función para testing
# def test_extractor():
#     """Función de prueba para el extractor"""
#     extractor = PreferenceExtractor()
    
#     test_inputs = [
#         "Busco un auto deportivo y potente, no me importa el precio",
#         "Necesito algo económico y eficiente para la familia",
#         "Quiero un BMW o Mercedes, algo lujoso y espacioso"
#     ]
    
#     print("🔍 Analizando preferencias de usuarios...\n")
    
#     for i, input_text in enumerate(test_inputs, 1):
#         print(f"--- Ejemplo {i} ---")
#         result = extractor.analyze_user_input(input_text)
        
#         print(f"Input: {result['user_input']}")
#         print("Scores:")
#         for key, value in result['preference_scores'].items():
#             print(f"  {key}: {value}")
#         print("Interpretación:")
#         for key, value in result['interpretation'].items():
#             print(f"  {key}: {value}")
#         print()


# # Clase para hacer matching con la base de datos de autos

# class CarMatcher:
#     def __init__(self, csv_path: str):
#         """
#         Inicializa el matcher con la base de datos de autos
        
#         Args:
#             csv_path: Ruta al archivo CSV con los datos de autos
#         """
#         self.extractor = PreferenceExtractor()
#         self.cars_df = pd.read_csv(csv_path)
        
#         # Las columnas de scores ya están en tu CSV
#         self.score_columns = ['Power Score', 'Price Score', 'Efficiency Score', 'Size Score', 'Brand Score']
#         self.car_vectors = self._prepare_car_vectors()
    
#     def _prepare_car_vectors(self) -> np.ndarray:
#         """Prepara los vectores de preferencias de los autos"""
#         return self.cars_df[self.score_columns].values
    
#     def find_best_matches(self, user_input: str, top_k: int = 5) -> pd.DataFrame:
#         """
#         Encuentra los mejores autos que coinciden con las preferencias del usuario
        
#         Args:
#             user_input: Texto del usuario describiendo lo que busca
#             top_k: Número de mejores coincidencias a retornar
            
#         Returns:
#             pd.DataFrame: Top K autos más similares con scores de similitud
#         """
#         # Extraer vector de preferencias del usuario
#         user_vector = self.extractor.get_preference_vector(user_input)
        
#         # Calcular similitud coseno con todos los autos
#         similarities = cosine_similarity([user_vector], self.car_vectors)[0]
        
#         # Agregar similitudes al DataFrame
#         result_df = self.cars_df.copy()
#         result_df['similarity_score'] = similarities
        
#         # Ordenar por similitud y retornar top K
#         return result_df.nlargest(top_k, 'similarity_score')[
#             ['Company Names', 'Cars Names', 'Cars Prices', 'Fuel Types', 'HorsePower', 'similarity_score'] + self.score_columns
#         ]

#     def analyze_match(self, user_input: str, top_k: int = 3):
#         """
#         Análisis completo de matching con interpretación
#         """
#         # Obtener preferencias del usuario
#         user_analysis = self.extractor.analyze_user_input(user_input)
        
#         # Obtener mejores matches
#         matches = self.find_best_matches(user_input, top_k)
        
#         print(f"🚗 Análisis de preferencias para: '{user_input}'")
#         print("\n📊 Preferencias detectadas:")
#         for key, value in user_analysis['preference_scores'].items():
#             print(f"  {key}: {value}")
        
#         print(f"\n🎯 Top {top_k} recomendaciones:")
#         for idx, (_, car) in enumerate(matches.iterrows(), 1):
#             print(f"\n{idx}. {car['Company Names']} {car['Cars Names']}")
#             print(f"   Precio: {car['Cars Prices']}")
#             print(f"   Similitud: {car['similarity_score']:.3f}")
#             print(f"   Scores: Power={car['Power Score']:.2f}, Price={car['Price Score']:.2f}, "
#                   f"Efficiency={car['Efficiency Score']:.2f}, Size={car['Size Score']:.2f}, Brand={car['Brand Score']:.2f}")


# # Función para testing
# def test_extractor():
#     """Función de prueba para el extractor"""
#     extractor = PreferenceExtractor()
    
#     test_inputs = [
#         "Busco un auto deportivo y potente, no me importa el precio",
#         "Necesito algo económico y eficiente para la familia",
#         "Quiero un BMW o Mercedes, algo lujoso y espacioso"
#     ]
    
#     print("🔍 Analizando preferencias de usuarios...\n")
    
#     for i, input_text in enumerate(test_inputs, 1):
#         print(f"--- Ejemplo {i} ---")
#         result = extractor.analyze_user_input(input_text)
        
#         print(f"Input: {result['user_input']}")
#         print("Scores:")
#         for key, value in result['preference_scores'].items():
#             print(f"  {key}: {value}")
#         print("Interpretación:")
#         for key, value in result['interpretation'].items():
#             print(f"  {key}: {value}")
#         print()

# def test_car_matcher():
#     """Función de prueba para el matcher de autos"""
#     csv_path = '/Users/pablomarotta/Desktop/ML/Concesionario/Concesionario/backend/FastApi/chatbot/cars_with_custom_scores.csv'
#     matcher = CarMatcher(csv_path)
    
#     test_inputs = [
#         "Busco un auto deportivo y potente, no me importa el precio",
#         "Necesito algo económico y eficiente para la familia",
#         "Quiero un BMW o Mercedes, algo lujoso y espacioso"
#     ]
    
#     print("🎯 Probando sistema de recomendaciones de autos...\n")
    
#     for input_text in test_inputs:
#         matcher.analyze_match(input_text)
#         print("\n" + "="*80 + "\n")

training_Data = [
    # Alta potencia, baja sensibilidad a precio
    ("Quiero un auto muy potente y deportivo", [0.95, 0.2, 0.3, 0.5, 0.3]),
    ("Necesito mucha aceleración y velocidad", [0.9, 0.3, 0.4, 0.4, 0.2]),
    ("Busco un motor fuerte con muchos caballos de fuerza", [0.95, 0.25, 0.35, 0.45, 0.25]),
    ("Me gusta la potencia y el desempeño deportivo", [0.9, 0.3, 0.35, 0.5, 0.3]),
    
    # Sensibilidad alta a precio
    ("Busco algo económico y barato", [0.4, 0.95, 0.5, 0.5, 0.6]),
    ("Necesito un auto de bajo costo", [0.3, 0.95, 0.45, 0.4, 0.7]),
    ("Presupuesto muy ajustado, lo más barato posible", [0.3, 1.0, 0.4, 0.3, 0.65]),
    ("Quiero la mejor relación calidad-precio", [0.5, 0.9, 0.5, 0.6, 0.6]),
    
    # Tamaño grande (familiar)
    ("Necesito un auto grande para mi familia", [0.4, 0.6, 0.95, 0.5, 0.5]),
    ("Busco algo espacioso con muchos asientos", [0.35, 0.55, 0.95, 0.45, 0.5]),
    ("Tengo 5 hijos, necesito espacio", [0.3, 0.5, 1.0, 0.5, 0.5]),
    ("Quiero una minivan o SUV grande", [0.4, 0.5, 0.95, 0.5, 0.45]),
    
    # Marca premium
    ("Quiero una marca de prestigio y reconocida", [0.5, 0.4, 0.5, 0.95, 0.5]),
    ("Busco marcas alemanas o japonesas confiables", [0.5, 0.5, 0.5, 0.9, 0.6]),
    ("La reputación de la marca es muy importante", [0.45, 0.5, 0.5, 0.95, 0.55]),
    ("Mercedes, BMW o Audi preferiblemente", [0.6, 0.3, 0.5, 0.95, 0.4]),
    
    # Alta eficiencia
    ("Necesito bajo consumo de combustible", [0.3, 0.7, 0.5, 0.5, 0.95]),
    ("Busco un híbrido o eléctrico", [0.4, 0.6, 0.5, 0.5, 0.95]),
    ("Quiero ahorrar en gasolina", [0.3, 0.8, 0.5, 0.5, 0.9]),
    ("Eficiencia energética es mi prioridad", [0.35, 0.65, 0.5, 0.5, 0.95]),
    
    # Combinaciones múltiples
    ("Auto potente pero eficiente", [0.85, 0.5, 0.5, 0.6, 0.8]),
    ("Grande, espacioso pero económico", [0.4, 0.85, 0.9, 0.5, 0.65]),
    ("Marca premium con buen rendimiento", [0.7, 0.4, 0.5, 0.9, 0.6]),
    ("Deportivo de marca reconocida, precio no importa", [0.9, 0.2, 0.4, 0.9, 0.3]),
    
    # Neutral/balanceado
    ("Un auto normal para uso diario", [0.5, 0.6, 0.5, 0.5, 0.6]),
    ("Algo estándar sin preferencias específicas", [0.5, 0.5, 0.5, 0.5, 0.5]),
    
    # Más variaciones para cada categoría
    ("El precio realmente no me importa", [0.5, 0.1, 0.5, 0.5, 0.5]),
    ("No necesito mucha potencia", [0.2, 0.6, 0.5, 0.5, 0.6]),
    ("Puede ser compacto", [0.5, 0.6, 0.2, 0.5, 0.7]),
    ("Cualquier marca está bien", [0.5, 0.6, 0.5, 0.3, 0.6]),
    ("El consumo no es problema", [0.6, 0.5, 0.5, 0.5, 0.2]),
    
    # Más ejemplos contextuales
    ("Para ir al trabajo en ciudad", [0.3, 0.75, 0.3, 0.5, 0.85]),
    ("Para viajes largos en carretera", [0.5, 0.6, 0.6, 0.6, 0.8]),
    ("Para uso off-road y aventura", [0.7, 0.5, 0.7, 0.6, 0.4]),
    ("Auto de lujo para ejecutivo", [0.6, 0.3, 0.6, 0.95, 0.5]),
    ("Primer auto para estudiante", [0.3, 0.95, 0.3, 0.4, 0.8]),
]

def create_training_examples(data):
    examples = []
    for text, vector in data:
        examples.append(InputExample(texts=[text], label=vector))
    return examples

training_examples = create_training_examples(training_Data)

def create_regression_model(base_model='sentence-transformers/all-MiniLM-L6-v2'):
    # Cargar modelo base
    try:
        word_embedding_model = models.Transformer(base_model)
    except Exception as e:
        print(f"⚠️ Error cargando {base_model}: {e}")
        print("🔄 Intentando con modelo alternativo...")
        # Usar un modelo más simple disponible localmente
        base_model = 'distilbert-base-uncased'
        word_embedding_model = models.Transformer(base_model)
    
    pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension())

    dense_model = models.Dense(in_features=pooling_model.get_sentence_embedding_dimension(),
                               out_features=5,  # 5 dimensiones para las preferencias
                               activation_function=torch.nn.Identity())

    model = SentenceTransformer(modules=[word_embedding_model, pooling_model, dense_model])

    train_dataloader = DataLoader(training_examples, shuffle=True, batch_size=16)
    train_loss = MSELoss(model)

    train_size = int(0.8 * len(training_examples))
    val_size = len(training_examples) - train_size

    training_examples_split = training_examples[:train_size]
    validation_examples_split = training_examples[train_size:]
    
    train_dataloader = DataLoader(training_examples_split, shuffle=True, batch_size=16)

    return model, train_dataloader, validation_examples_split

def evaluate_model(model, validation_examples):
    """
    Evalúa el modelo en el set de validación
    """
    total_mse = 0
    num_examples = len(validation_examples)
    
    for example in validation_examples:
        text = example.texts[0]
        true_label = np.array(example.label)
        
        # Predecir
        prediction = model.encode([text])[0]
        
        # Calcular MSE
        mse = np.mean((prediction - true_label) ** 2)
        total_mse += mse
    
    return total_mse / num_examples if num_examples > 0 else float('inf')

def train_preference_model(epochs=10, save_path='./preference_model'):
    """
    Entrena el modelo de preferencias con validación
    
    Args:
        epochs: Número de épocas de entrenamiento
        save_path: Ruta donde guardar el modelo entrenado
    """
    
    # Crear modelo
    model, train_dataloader, validation_examples = create_regression_model()
    train_loss = MSELoss(model)
    
    print(f"📊 Datos de entrenamiento: {len(train_dataloader.dataset)} ejemplos")
    print(f"📊 Datos de validación: {len(validation_examples)} ejemplos")
    
    # Métricas para seguimiento
    train_losses = []
    val_losses = []
    best_val_loss = float('inf')
    
    print("\n🎯 Comenzando entrenamiento...")
    print("-" * 60)
    
    for epoch in range(epochs):
        # Entrenamiento
        model.fit(
            train_objectives=[(train_dataloader, train_loss)],
            epochs=1,
            warmup_steps=0,
            evaluation_steps=0,
            show_progress_bar=False,
            save_best_model=False
        )
        
        # Evaluación
        val_loss = evaluate_model(model, validation_examples)
        train_loss_value = evaluate_model(model, train_dataloader.dataset)
        
        train_losses.append(train_loss_value)
        val_losses.append(val_loss)
        
        # Guardar mejor modelo
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            model.save(f"{save_path}_best")
            
        print(f"Época {epoch+1:2d}/{epochs} | "
              f"Train Loss: {train_loss_value:.4f} | "
              f"Val Loss: {val_loss:.4f} | "
              f"{'✨ Nuevo mejor!' if val_loss == best_val_loss else ''}")
    
    # Guardar modelo final
    model.save(save_path)
    
    print(f"\n✅ Entrenamiento completado!")
    print(f"📁 Mejor modelo guardado en: {save_path}_best")
    print(f"📁 Modelo final guardado en: {save_path}")
    print(f"🎯 Mejor pérdida de validación: {best_val_loss:.4f}")
    
    return model, train_losses, val_losses

def test_trained_model(model_path='./preference_model_best'):
    """
    Prueba el modelo entrenado con ejemplos de test
    """
    print(f"🔍 Cargando modelo entrenado desde: {model_path}")
    
    try:
        model = SentenceTransformer(model_path)
        print("✅ Modelo cargado exitosamente!")
    except Exception as e:
        print(f"❌ Error cargando modelo: {e}")
        return None
    
    # Casos de prueba
    test_cases = [
        ("Quiero un auto muy potente y deportivo", [0.95, 0.2, 0.3, 0.5, 0.3]),
        ("Busco algo económico y barato", [0.4, 0.95, 0.5, 0.5, 0.6]),
        ("Necesito un auto grande para mi familia", [0.4, 0.6, 0.95, 0.5, 0.5]),
        ("Quiero una marca de prestigio", [0.5, 0.4, 0.5, 0.95, 0.5]),
        ("Necesito bajo consumo de combustible", [0.3, 0.7, 0.5, 0.5, 0.95]),
    ]
    
    print("\n🎯 Probando predicciones del modelo:")
    print("-" * 80)
    
    total_error = 0
    for i, (text, expected) in enumerate(test_cases, 1):
        # Predecir
        predicted = model.encode([text])[0]
        
        # Calcular error
        mse = np.mean((predicted - np.array(expected)) ** 2)
        total_error += mse
        
        print(f"\n{i}. Texto: '{text}'")
        print(f"   Esperado:  {[f'{x:.2f}' for x in expected]}")
        print(f"   Predicho:  {[f'{x:.2f}' for x in predicted]}")
        print(f"   MSE:       {mse:.4f}")
    
    avg_error = total_error / len(test_cases)
    print(f"\n📊 Error promedio (MSE): {avg_error:.4f}")
    
    return model

class TrainedPreferenceExtractor:
    """
    Extractor de preferencias usando modelo entrenado
    """
    def __init__(self, model_path='./preference_model_best'):
        try:
            self.model = SentenceTransformer(model_path)
            print(f"✅ Modelo entrenado cargado desde: {model_path}")
        except Exception as e:
            print(f"⚠️ No se pudo cargar modelo entrenado: {e}")
            print("🔄 Usando modelo base sin entrenar...")
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def extract_preferences(self, user_input: str) -> dict:
        """Extrae preferencias usando el modelo entrenado"""
        # Predecir directamente con el modelo entrenado
        scores = self.model.encode([user_input])[0]
        
        # Asegurar que estén en rango [0,1]
        scores = np.clip(scores, 0, 1)
        
        return {
            'power_score': round(float(scores[0]), 3),
            'price_score': round(float(scores[1]), 3),
            'size_score': round(float(scores[2]), 3),
            'brand_score': round(float(scores[3]), 3),
            'efficiency_score': round(float(scores[4]), 3)
        }
    
    def get_preference_vector(self, user_input: str) -> np.ndarray:
        """Retorna vector de preferencias"""
        scores = self.model.encode([user_input])[0]
        return np.clip(scores, 0, 1)
    
    def analyze_user_input(self, user_input: str) -> dict:
        """Análisis completo del input del usuario"""
        preferences = self.extract_preferences(user_input)
        vector = self.get_preference_vector(user_input)
        
        # Interpretación de scores
        interpretation = {}
        for key, score in preferences.items():
            dimension = key.replace('_score', '')
            if score >= 0.7:
                interpretation[dimension] = "Alta preferencia"
            elif score >= 0.3:
                interpretation[dimension] = "Preferencia moderada"
            else:
                interpretation[dimension] = "Baja preferencia"
        
        return {
            'user_input': user_input,
            'preference_scores': preferences,
            'preference_vector': vector.tolist(),
            'interpretation': interpretation
        }

class ImprovedCarMatcher:
    """
    Matcher de autos usando modelo entrenado
    """
    def __init__(self, csv_path: str, model_path='./preference_model_best'):
        self.extractor = TrainedPreferenceExtractor(model_path)
        self.cars_df = pd.read_csv(csv_path)
        
        # Mapear columnas del CSV a nuestro orden [power, price, size, brand, efficiency]
        self.score_columns = ['Power Score', 'Price Score', 'Size Score', 'Brand Score', 'Efficiency Score']
        self.car_vectors = self._prepare_car_vectors()
    
    def _prepare_car_vectors(self) -> np.ndarray:
        """Prepara los vectores ordenados según el modelo entrenado"""
        return self.cars_df[self.score_columns].values
    
    def find_best_matches(self, user_input: str, top_k: int = 5) -> pd.DataFrame:
        """Encuentra los mejores autos usando el modelo entrenado"""
        # Extraer vector de preferencias del usuario
        user_vector = self.extractor.get_preference_vector(user_input)
        
        # Calcular similitud coseno con todos los autos
        similarities = cosine_similarity([user_vector], self.car_vectors)[0]
        
        # Agregar similitudes al DataFrame
        result_df = self.cars_df.copy()
        result_df['similarity_score'] = similarities
        
        # Ordenar por similitud y retornar top K
        return result_df.nlargest(top_k, 'similarity_score')[
            ['Company Names', 'Cars Names', 'Cars Prices', 'Fuel Types', 'HorsePower', 'similarity_score'] + self.score_columns
        ]
    
    def analyze_match(self, user_input: str, top_k: int = 3):
        """Análisis completo usando modelo entrenado"""
        # Obtener preferencias del usuario
        user_analysis = self.extractor.analyze_user_input(user_input)
        
        # Obtener mejores matches
        matches = self.find_best_matches(user_input, top_k)
        
        print(f"🚗 Análisis con modelo entrenado: '{user_input}'")
        print("\n📊 Preferencias detectadas:")
        for key, value in user_analysis['preference_scores'].items():
            print(f"  {key}: {value}")
        
        print(f"\n🎯 Top {top_k} recomendaciones:")
        for idx, (_, car) in enumerate(matches.iterrows(), 1):
            print(f"\n{idx}. {car['Company Names']} {car['Cars Names']}")
            print(f"   Precio: {car['Cars Prices']}")
            print(f"   Similitud: {car['similarity_score']:.3f}")
            print(f"   Scores: Power={car['Power Score']:.2f}, Price={car['Price Score']:.2f}, "
                  f"Size={car['Size Score']:.2f}, Brand={car['Brand Score']:.2f}, Efficiency={car['Efficiency Score']:.2f}")

def run_complete_training_pipeline():
    """
    Ejecuta el pipeline completo de entrenamiento y pruebas
    """
    print("🎓 INICIANDO PIPELINE COMPLETO DE ENTRENAMIENTO")
    print("=" * 60)
    
    # 1. Entrenar el modelo
    print("\n1️⃣ FASE DE ENTRENAMIENTO")
    model, train_losses, val_losses = train_preference_model(epochs=15)
    
    # 2. Probar el modelo entrenado
    print("\n2️⃣ FASE DE PRUEBAS")
    test_trained_model()
    
    # 3. Comparar con matcher mejorado
    print("\n3️⃣ FASE DE RECOMENDACIONES")
    csv_path = '/Users/pablomarotta/Desktop/ML/Concesionario/Concesionario/backend/FastApi/chatbot/cars_with_custom_scores.csv'
    matcher = ImprovedCarMatcher(csv_path)
    
    test_inputs = [
        "Busco un auto deportivo y potente, no me importa el precio",
        "Necesito algo económico y eficiente para la familia",
        "Quiero un BMW o Mercedes, algo lujoso y espacioso"
    ]
    
    for input_text in test_inputs:
        matcher.analyze_match(input_text)
        print("\n" + "="*80 + "\n")
    
    print("✅ PIPELINE COMPLETADO!")
    
    return model, train_losses, val_losses

def quick_preference_analysis(user_input: str, model_path='./preference_model_best'):
    """
    Función rápida para analizar preferencias y obtener recomendaciones
    
    Args:
        user_input: Texto del usuario
        model_path: Ruta del modelo entrenado
        
    Returns:
        dict: Resultados del análisis
    """
    try:
        # Cargar extractor entrenado
        extractor = TrainedPreferenceExtractor(model_path)
        
        # Analizar preferencias
        analysis = extractor.analyze_user_input(user_input)
        
        # Obtener recomendaciones
        csv_path = '/Users/pablomarotta/Desktop/ML/Concesionario/Concesionario/backend/FastApi/chatbot/cars_with_custom_scores.csv'
        matcher = ImprovedCarMatcher(csv_path, model_path)
        recommendations = matcher.find_best_matches(user_input, top_k=5)
        
        return {
            'preferences': analysis['preference_scores'],
            'interpretation': analysis['interpretation'],
            'recommendations': recommendations.to_dict('records')
        }
        
    except Exception as e:
        print(f"❌ Error en análisis rápido: {e}")
        return None

# Ejecutar cuando se corra el archivo
if __name__ == "__main__":
    print("🚀 Sistema de Entrenamiento de Preferencias")
    print("Selecciona una opción:")
    print("1. Entrenar modelo completo")
    print("2. Solo probar modelo existente")
    print("3. Ejecutar pipeline completo")
    print("4. Análisis rápido interactivo")
    
    try:
        choice = input("\nIngresa tu opción (1-4): ").strip()
        
        if choice == "1":
            train_preference_model(epochs=15)
        elif choice == "2":
            test_trained_model()
        elif choice == "3":
            run_complete_training_pipeline()
        elif choice == "4":
            print("\n🔍 ANÁLISIS RÁPIDO INTERACTIVO")
            print("Escribe tu consulta sobre el auto que buscas:")
            user_query = input(">>> ")
            
            result = quick_preference_analysis(user_query)
            if result:
                print(f"\n📊 Preferencias detectadas:")
                for key, value in result['preferences'].items():
                    print(f"  {key}: {value}")
                
                print(f"\n🎯 Top 3 recomendaciones:")
                for i, car in enumerate(result['recommendations'][:3], 1):
                    print(f"{i}. {car['Company Names']} {car['Cars Names']} - {car['Cars Prices']}")
                    print(f"   Similitud: {car['similarity_score']:.3f}")
        else:
            print("Ejecutando pipeline completo por defecto...")
            run_complete_training_pipeline()
            
    except KeyboardInterrupt:
        print("\n⛔ Proceso cancelado por el usuario")
    except Exception as e:
        print(f"❌ Error durante la ejecución: {e}")
        import traceback
        traceback.print_exc()