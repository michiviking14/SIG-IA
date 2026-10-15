import pytest
from app.services.nlp_service import nlp_service

class TestVersionDetection:
    """Pruebas para el sistema inteligente de detección y prevención de colisión de versiones."""

    def test_extraer_codigo_institucional(self):
        """Verifica que se extraigan correctamente los códigos UTS."""
        assert nlp_service.extraer_codigo_institucional("F-AM-04 Solicitud Grado V18.docx") == "F-AM-04"
        assert nlp_service.extraer_codigo_institucional("F-DC-125 AndersonDiz.docx") == "F-DC-125"
        assert nlp_service.extraer_codigo_institucional("SST-IG-05 Procedimiento.pdf") == "SST-IG-05"
        assert nlp_service.extraer_codigo_institucional("RESOLUCION-02-979.pdf") == "RES-02-979"
        assert nlp_service.extraer_codigo_institucional("informe_general_2026.docx") is None

    def test_normalizar_nombre_archivo(self):
        """Verifica que se remuevan sufijos de versión, copias y caracteres especiales."""
        norm1 = nlp_service.normalizar_nombre_archivo("F-AM-04 Solicitud Grado V18.docx")
        norm2 = nlp_service.normalizar_nombre_archivo("F-AM-04 Solicitud Grado v1.1.docx")
        assert norm1 == norm2
        assert "v18" not in norm1
        assert "v1.1" not in norm2

        norm_copia = nlp_service.normalizar_nombre_archivo("Plan de Trabajo (1) copia.docx")
        assert "copia" not in norm_copia
        assert "(1)" not in norm_copia

    def test_calcular_similitud_nombres_veto_codigos(self):
        """Si dos archivos tienen códigos institucionales distintos, la similitud DEBE ser 0.0 (veto)."""
        sim = nlp_service.calcular_similitud_nombres(
            "F-AM-04 Solicitud Grado V18.docx",
            "F-DC-125 AndersonDiz.docx"
        )
        assert sim == 0.0

    def test_calcular_similitud_nombres_mismo_archivo(self):
        """Archivos con el mismo nombre o variantes de versión deben tener similitud 1.0."""
        sim = nlp_service.calcular_similitud_nombres(
            "F-AM-04 Solicitud Grado V18.docx",
            "F-AM-04 Solicitud Grado v19.docx"
        )
        assert sim == 1.0

    def test_evaluar_candidato_veto_codigos_diferentes(self):
        """
        Caso crítico del reporte del usuario:
        F-AM-04 (Solicitud Grado) y F-DC-125 (Anderson Alviares)
        Incluso con 95% de similitud en el texto (por membretes institucionales de las UTS),
        DEBE ser rechazado como versión.
        """
        es_version, score, razon = nlp_service.evaluar_candidato_version(
            nombre_nuevo="F-DC-125 AndersonDiz.docx",
            nombre_existente="F-AM-04 Solicitud Grado V18.docx",
            similitud_contenido=0.95,
            categoria_id_nuevo=5,
            categoria_id_existente=2
        )
        assert es_version is False
        assert score == 0.0
        assert "Códigos institucionales diferentes" in razon

    def test_evaluar_candidato_misma_plantilla_con_cambios_menores(self):
        """
        Usuario modifica una frase o datos en la misma plantilla:
        Nombre similar (o mismo código), similitud de contenido alta -> DEBE ser versión.
        """
        es_version, score, razon = nlp_service.evaluar_candidato_version(
            nombre_nuevo="F-AM-04 Solicitud Grado V18_editado.docx",
            nombre_existente="F-AM-04 Solicitud Grado V18.docx",
            similitud_contenido=0.92,
            categoria_id_nuevo=2,
            categoria_id_existente=2
        )
        assert es_version is True
        assert score > 0.85

    def test_evaluar_candidato_nombres_totalmente_diferentes_sin_codigo(self):
        """
        Dos documentos sin código pero con nombres totalmente diferentes
        no deben unirse como versiones aunque compartan texto de plantilla.
        """
        es_version, score, razon = nlp_service.evaluar_candidato_version(
            nombre_nuevo="Manual de Convivencia Estudiantil.pdf",
            nombre_existente="Reglamento Disciplinario Docente.pdf",
            similitud_contenido=0.88,
            categoria_id_nuevo=1,
            categoria_id_existente=1
        )
        assert es_version is False
        assert "No cumple criterios de versionado" in razon
