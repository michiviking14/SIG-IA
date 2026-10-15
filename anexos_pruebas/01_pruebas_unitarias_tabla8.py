"""
================================================================================
ANEXO TÉCNICO: SUITE DE 11 PRUEBAS UNITARIAS FORMALES (PYTEST)
PROYECTO: SIG-IA UTS - GESTIÓN DOCUMENTAL INTELIGENTE
REFERENCIA DE TESIS: CAPÍTULO 4.4 (FASE DE PRUEBAS) - TABLA 8
================================================================================
Descripción:
Contiene la implementación exacta y ejecutable con Pytest de las 11 pruebas
unitarias descritas en la Tabla 8 del documento de grado:
- test_01_primera_version
- test_02_generacion_embeddings
- test_03_embeddings_texto_vacio
- test_04_similitud_coseno_identicos
- test_05_similitud_vector_cero
- test_06_clasificacion_sin_categorias
- test_07_clasificacion_texto_vacio
- test_08_clasificacion_categorias_reales
- test_09_clasificacion_palabras_clave
- test_10_extraccion_texto_ponderado
- test_11_estadisticas_clasificacion

Comando de ejecución:
pytest 01_pruebas_unitarias_tabla8.py -v --durations=0
================================================================================
"""

import sys
import os
import pytest

# Asegurar importación de módulos del backend
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
if not os.path.exists(backend_dir):
    backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

try:
    from dotenv import load_dotenv
    env_file = os.path.join(backend_dir, ".env")
    if os.path.exists(env_file):
        load_dotenv(env_file)
except ImportError:
    pass

from app.services.version_service import version_service
from app.services.nlp_service import nlp_service


class TestTabla8Unitarios:
    """Suite de 11 pruebas unitarias registradas en la Tabla 8 de la tesis."""

    def test_01_primera_version(self):
        """Verifica que la primera versión de un documento nuevo se asigne como 'v1.0'."""
        class MockVersion:
            def __init__(self):
                self.numero_version = "v1.0"
        
        class MockDocumento:
            id = 1
            versiones = []
        
        class MockQuery:
            def filter(self, *args):
                return self
            def order_by(self, *args):
                return self
            def first(self):
                return None
        
        class MockDB:
            def query(self, model):
                return MockQuery()
        
        mock_doc = MockDocumento()
        mock_db = MockDB()
        version = version_service.obtener_siguiente_version(mock_doc, mock_db)
        assert version == "v1.0"

    def test_02_generacion_embeddings(self):
        """Verifica que el modelo sentence-transformers produzca vectores de dimensión 384."""
        embedding = nlp_service.generar_embedding("Documento institucional de prueba UTS")
        assert isinstance(embedding, list)
        assert len(embedding) == 384
        assert all(isinstance(x, float) for x in embedding)

    def test_03_embeddings_texto_vacio(self):
        """Verifica que ante un texto vacío el servicio no falle y devuelva una lista vacía [] de forma controlada."""
        embedding_vacio = nlp_service.generar_embedding("")
        assert isinstance(embedding_vacio, list)
        assert embedding_vacio == []

        embedding_espacios = nlp_service.generar_embedding("   ")
        assert isinstance(embedding_espacios, list)
        assert embedding_espacios == []

        embedding_none = nlp_service.generar_embedding(None)
        assert isinstance(embedding_none, list)
        assert embedding_none == []

    def test_04_similitud_coseno_identicos(self):
        """Verifica que dos vectores idénticos produzcan una similitud de coseno cercana a 1.0."""
        embedding1 = [1.0] * 384
        embedding2 = [1.0] * 384
        similitud = nlp_service.calcular_similitud_coseno(embedding1, embedding2)
        assert similitud > 0.999
        assert pytest.approx(similitud, 0.001) == 1.0

    def test_05_similitud_vector_cero(self):
        """Verifica el manejo del caso límite con vector cero sin producir ZeroDivisionError."""
        embedding_normal = [1.0] * 384
        embedding_cero = [0.0] * 384
        # Caso 1: vector normal vs vector cero
        similitud = nlp_service.calcular_similitud_coseno(embedding_normal, embedding_cero)
        assert similitud == 0.0
        # Caso 2: ambos vectores en cero
        similitud_doble_cero = nlp_service.calcular_similitud_coseno(embedding_cero, embedding_cero)
        assert similitud_doble_cero == 0.0

    def test_06_clasificacion_sin_categorias(self):
        """Verifica que el sistema responda de forma controlada cuando no hay categorías configuradas."""
        cat_id, confianza, top_cats = nlp_service.clasificar_documento("Texto institucional de prueba", [])
        assert cat_id is None
        assert confianza is None
        assert top_cats == []

    def test_07_clasificacion_texto_vacio(self):
        """Verifica que el motor no asigne categoría cuando no hay contenido que analizar."""
        categorias_demo = [{"id": 1, "nombre": "Normativas", "embedding": None}]
        cat_id, confianza, top_cats = nlp_service.clasificar_documento("", categorias_demo)
        assert cat_id is None
        assert confianza is None
        assert top_cats == []

    def test_08_clasificacion_categorias_reales(self):
        """Verifica que un documento se asigne a la categoría correcta y las sugerencias (Top 3) queden ordenadas descendentemente por puntaje."""
        categorias = [
            {
                "id": 1,
                "nombre": "Normativas y políticas",
                "descripcion": "Reglas y lineamientos institucionales",
                "embedding": nlp_service.generar_embedding("Normativas y políticas. Reglas y lineamientos normativa política reglamento"),
                "palabras_clave": ["normativa", "política", "reglamento", "lineamiento"],
                "umbral_confianza": 0.50
            },
            {
                "id": 2,
                "nombre": "Informes y reportes",
                "descripcion": "Reportes estadísticos de gestión",
                "embedding": nlp_service.generar_embedding("Informes y reportes. Reportes estadísticos informe datos"),
                "palabras_clave": ["informe", "reporte", "estadística"],
                "umbral_confianza": 0.50
            },
            {
                "id": 3,
                "nombre": "Formatos y plantillas",
                "descripcion": "Documentos modelo y formularios",
                "embedding": nlp_service.generar_embedding("Formatos y plantillas. Documentos modelo formulario plantilla"),
                "palabras_clave": ["formato", "plantilla", "formulario"],
                "umbral_confianza": 0.50
            }
        ]
        
        texto_normativo = "Esta es una normativa institucional que establece los lineamientos del reglamento interno de políticas organizacionales de las UTS."
        cat_id, confianza, top_cats = nlp_service.clasificar_documento(texto_normativo, categorias, top_k=3)
        
        assert cat_id == 1
        assert len(top_cats) == 3
        assert top_cats[0]["categoria_id"] == 1
        assert top_cats[0]["score_final"] >= top_cats[1]["score_final"] >= top_cats[2]["score_final"]

    def test_09_clasificacion_palabras_clave(self):
        """Verifica que el puntaje de coincidencia de palabras clave sea > 0 cuando existen coincidencias léxicas."""
        categorias = [
            {
                "id": 1,
                "nombre": "Actas y resoluciones",
                "descripcion": "Actas de reuniones y resoluciones del consejo directivo",
                "embedding": nlp_service.generar_embedding("Actas y resoluciones. Actas de reuniones"),
                "palabras_clave": ["acta", "resolución", "sesión", "comité"],
                "umbral_confianza": 0.50
            }
        ]
        
        texto = "Acta de la sesión del comité directivo donde se aprobó la resolución institucional número 123."
        cat_id, confianza, top_cats = nlp_service.clasificar_documento(texto, categorias)
        
        assert len(top_cats) == 1
        assert top_cats[0]["score_keywords"] > 0
        assert top_cats[0]["categoria_id"] == 1

    def test_10_extraccion_texto_ponderado(self):
        """Verifica que el resultado conserve y priorice la primera línea/encabezado del documento."""
        texto = "\n".join([f"Línea {i} de encabezado institucional" for i in range(1, 101)])
        resultado = nlp_service.extraer_texto_ponderado(texto)
        assert len(resultado) > 0
        assert "Línea 1 de encabezado institucional" in resultado
        assert resultado.startswith("Línea 1")

    def test_11_estadisticas_clasificacion(self):
        """Verifica que los totales y la distribución por categoría se calculen correctamente."""
        categorias = [{"id": 1, "nombre": "Cat1"}, {"id": 2, "nombre": "Cat2"}]
        documentos = [
            {"categoria_id": 1},
            {"categoria_id": 1},
            {"categoria_id": 2},
            {"categoria_id": None}
        ]
        
        stats = nlp_service.obtener_estadisticas_clasificacion(categorias, documentos)
        
        assert stats["total_documentos"] == 4
        assert stats["clasificados"] == 3
        assert stats["sin_clasificar"] == 1
        assert len(stats["por_categoria"]) == 2
        assert stats["por_categoria"][0]["cantidad"] == 2
        assert stats["por_categoria"][1]["cantidad"] == 1
