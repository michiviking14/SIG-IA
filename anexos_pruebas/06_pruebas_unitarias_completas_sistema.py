import pytest
from app.services.version_service import version_service
from app.services.nlp_service import nlp_service
from app.services.ocr_service import extraer_texto

class TestVersionService:
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

    test_obtener_primera_version = test_01_primera_version

class TestNLPService:
    def test_02_generacion_embeddings(self):
        """Verifica que el modelo sentence-transformers produzca vectores de dimensión 384."""
        embedding = nlp_service.generar_embedding("Documento de prueba")
        assert isinstance(embedding, list)
        assert len(embedding) == 384

    test_generar_embedding = test_02_generacion_embeddings

    def test_03_embeddings_texto_vacio(self):
        """Verifica que ante un texto vacío el servicio no falle y devuelva una lista vacía [] de forma controlada."""
        embedding = nlp_service.generar_embedding("")
        assert isinstance(embedding, list)
        assert embedding == []

    test_generar_embedding_vacio = test_03_embeddings_texto_vacio

    def test_04_similitud_coseno_identicos(self):
        """Verifica que dos vectores idénticos produzcan una similitud de coseno cercana a 1.0."""
        embedding1 = [1.0] * 384
        embedding2 = [1.0] * 384
        similitud = nlp_service.calcular_similitud_coseno(embedding1, embedding2)
        assert similitud > 0.99

    test_calcular_similitud_coseno = test_04_similitud_coseno_identicos

    def test_05_similitud_vector_cero(self):
        """Verifica el manejo del caso límite con vector cero sin producir ZeroDivisionError."""
        embedding1 = [1.0] * 384
        embedding2 = [0.0] * 384
        similitud = nlp_service.calcular_similitud_coseno(embedding1, embedding2)
        assert similitud == 0.0

    test_calcular_similitud_cero = test_05_similitud_vector_cero

    def test_06_clasificacion_sin_categorias(self):
        """Verifica que el sistema responda de forma controlada cuando no hay categorías configuradas."""
        cat_id, confianza, top_cats = nlp_service.clasificar_documento("texto de prueba", [])
        assert cat_id is None
        assert confianza is None
        assert top_cats == []

    test_clasificar_documento_sin_categorias = test_06_clasificacion_sin_categorias

    def test_07_clasificacion_texto_vacio(self):
        """Verifica que el motor no asigne categoría cuando no hay contenido que analizar."""
        cat_id, confianza, top_cats = nlp_service.clasificar_documento("", [{"id": 1, "nombre": "test", "embedding": None}])
        assert cat_id is None
        assert confianza is None

    test_clasificar_documento_texto_vacio = test_07_clasificacion_texto_vacio

    def test_08_clasificacion_categorias_reales(self):
        """Verifica que un documento se asigne a la categoría correcta y las sugerencias (Top 3) queden ordenadas descendentemente por puntaje."""
        categorias = [
            {
                "id": 1,
                "nombre": "Normativas y políticas",
                "descripcion": "Reglas y lineamientos",
                "embedding": nlp_service.generar_embedding("Normativas y políticas. Reglas y lineamientos normativa política reglamento"),
                "palabras_clave": ["normativa", "política", "reglamento"],
                "umbral_confianza": 0.50
            },
            {
                "id": 2,
                "nombre": "Informes y reportes",
                "descripcion": "Reportes estadísticos",
                "embedding": nlp_service.generar_embedding("Informes y reportes. Reportes estadísticos informe datos"),
                "palabras_clave": ["informe", "reporte", "estadística"],
                "umbral_confianza": 0.50
            },
            {
                "id": 3,
                "nombre": "Formatos y plantillas",
                "descripcion": "Modelos y formatos institucionales",
                "embedding": nlp_service.generar_embedding("Formatos y plantillas. Modelos y formatos formulario"),
                "palabras_clave": ["formato", "plantilla", "formulario"],
                "umbral_confianza": 0.50
            }
        ]
        
        texto_normativo = "Esta es una normativa institucional que establece los lineamientos del reglamento interno de políticas organizacionales."
        cat_id, confianza, top_cats = nlp_service.clasificar_documento(texto_normativo, categorias, top_k=3)
        
        assert len(top_cats) == 3
        assert cat_id == 1
        assert top_cats[0]["categoria_id"] == 1
        assert top_cats[0]["score_final"] >= top_cats[1]["score_final"] >= top_cats[2]["score_final"]

    test_clasificar_documento_con_categorias = test_08_clasificacion_categorias_reales

    def test_09_clasificacion_palabras_clave(self):
        """Verifica que el puntaje de coincidencia de palabras clave sea > 0 cuando existen coincidencias léxicas."""
        categorias = [
            {
                "id": 1,
                "nombre": "Actas y resoluciones",
                "descripcion": "Actas de reuniones",
                "embedding": nlp_service.generar_embedding("Actas y resoluciones. Actas de reuniones"),
                "palabras_clave": ["acta", "resolución", "sesión", "comité"],
                "umbral_confianza": 0.70
            }
        ]
        
        texto = "Acta de la sesión del comité directivo donde se aprobó la resolución número 123."
        cat_id, confianza, top_cats = nlp_service.clasificar_documento(texto, categorias)
        
        assert top_cats[0]["score_keywords"] > 0
        assert len(top_cats) == 1

    test_clasificar_con_palabras_clave = test_09_clasificacion_palabras_clave

    def test_10_extraccion_texto_ponderado(self):
        """Verifica que el resultado conserve y priorice la primera línea/encabezado del documento."""
        texto = "\n".join([f"Línea {i}" for i in range(1, 101)])
        resultado = nlp_service.extraer_texto_ponderado(texto)
        assert len(resultado) > 0
        assert "Línea 1" in resultado
        assert resultado.startswith("Línea 1")

    def test_extraer_texto_ponderado_vacio(self):
        resultado = nlp_service.extraer_texto_ponderado("")
        assert resultado == ""

    def test_generar_embedding_categoria(self):
        embedding = nlp_service.generar_embedding_categoria(
            nombre="Test",
            descripcion="Descripción de prueba",
            palabras_clave=["palabra1", "palabra2"]
        )
        assert isinstance(embedding, list)
        assert len(embedding) == 384

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

    test_obtener_estadisticas_clasificacion = test_11_estadisticas_clasificacion

class TestDocSupport:
    def test_doc_config_allowed_extensions(self):
        from app.core.config import settings
        assert ".doc" in settings.ALLOWED_EXTENSIONS
        assert "application/msword" in settings.ALLOWED_MIME_TYPES

    def test_doc_magic_bytes_validation(self):
        from app.core.security import validate_file_magic_bytes
        ole_header = b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1" + b"\x00" * 20
        assert validate_file_magic_bytes(ole_header, ".doc") is True

        rtf_header = b"{\\rtf1\\ansi\\deff0" + b"\x00" * 20
        assert validate_file_magic_bytes(rtf_header, ".doc") is True

        fake_header = b"NOT_A_VALID_HEADER"
        assert validate_file_magic_bytes(fake_header, ".doc") is False

    def test_extraer_texto_doc_ole(self):
        import struct
        from app.services.ocr_service import extraer_texto_doc_ole
        text = "Documento DOC UTS de prueba."
        ansi_bytes = text.encode('cp1252')
        text_offset = 0x0200
        wd = bytearray(text_offset + len(ansi_bytes) + 16)
        struct.pack_into("<H", wd, 0, 0xA5EC)
        struct.pack_into("<H", wd, 2, 0x00C1)
        struct.pack_into("<H", wd, 0x000A, 0x0200)
        fc_val = 0x40000000 | (text_offset * 2)
        plcfpcd = struct.pack("<II", 0, len(ansi_bytes)) + struct.pack("<HIH", 0, fc_val, 0)
        clx = bytes([2]) + struct.pack("<I", len(plcfpcd)) + plcfpcd
        struct.pack_into("<II", wd, 0x01A2, 0, len(clx))
        wd[text_offset : text_offset + len(ansi_bytes)] = ansi_bytes
        extracted = extraer_texto_doc_ole(bytes(wd), bytes(clx))
        assert "Documento DOC UTS" in extracted

    def test_extraer_texto_rtf(self):
        from app.services.ocr_service import extraer_texto_rtf
        rtf_content = rb"{\rtf1\ansi\deff0 {\fonttbl {\f0 Times New Roman;}} \f0\fs24 Hola UTS \b Negrita \b0 texto plano.}"
        extracted = extraer_texto_rtf(rtf_content)
        assert "Hola UTS" in extracted
        assert "Negrita" in extracted


class TestBugFixes:
    def test_version_increment_edge_cases(self):
        class MockVersion:
            def __init__(self, ver):
                self.numero_version = ver
        
        class MockDocumento:
            id = 1
        
        class MockQuery:
            def __init__(self, v):
                self.v = v
            def filter(self, *args):
                return self
            def order_by(self, *args):
                return self
            def first(self):
                return self.v
        
        class MockDB:
            def __init__(self, v):
                self.v = v
            def query(self, model):
                return MockQuery(self.v)

        doc = MockDocumento()
        # Case 1: v1.0 -> v1.1
        assert version_service.obtener_siguiente_version(doc, MockDB(MockVersion("v1.0"))) == "v1.1"
        # Case 2: v1.1 -> v1.2
        assert version_service.obtener_siguiente_version(doc, MockDB(MockVersion("v1.1"))) == "v1.2"
        # Case 3: 2.3 (without v) -> v2.4
        assert version_service.obtener_siguiente_version(doc, MockDB(MockVersion("2.3"))) == "v2.4"
        # Case 4: corrupted non-numeric string -> fallback v1.1
        assert version_service.obtener_siguiente_version(doc, MockDB(MockVersion("invalid_ver"))) == "v1.1"

    def test_filtros_chromadb_fechas(self):
        # Empty filters
        assert nlp_service._aplicar_filtros_chromadb({}) is None
        assert nlp_service._aplicar_filtros_chromadb(None) is None

        # Only category
        res = nlp_service._aplicar_filtros_chromadb({"categoria_id": 3})
        assert res == {"categoria_id": 3}

        # Date range
        res = nlp_service._aplicar_filtros_chromadb({"fecha_desde": "2026-01-01", "fecha_hasta": "2026-03-31"})
        assert "$and" in res
        assert {"fecha": {"$gte": "2026-01-01"}} in res["$and"]
        assert {"fecha": {"$lte": "2026-03-31 23:59:59"}} in res["$and"]

        # Combined category + dates
        res = nlp_service._aplicar_filtros_chromadb({"categoria_id": 7, "fecha_desde": "2026-02-01"})
        assert "$and" in res
        assert {"categoria_id": 7} in res["$and"]
        assert {"fecha": {"$gte": "2026-02-01"}} in res["$and"]
