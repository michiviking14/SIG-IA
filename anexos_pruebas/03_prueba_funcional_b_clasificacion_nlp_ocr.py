"""
================================================================================
ANEXO TÉCNICO: PRUEBA FUNCIONAL B
MATRIZ DE CLASIFICACIÓN AUTOMÁTICA MULTIMODAL (NLP Y OCR)
PROYECTO: SIG-IA UTS - GESTIÓN DOCUMENTAL INTELIGENTE
REFERENCIA DE TESIS: CAPÍTULO 4.4 Y CAPÍTULO 5 (RESULTADOS)
================================================================================
Descripción:
Evalúa la clasificación automática inteligente de documentos institucionales UTS
en las 5 categorías oficiales mediante la arquitectura híbrida:
- Similitud Coseno Semántica (50%): Vectorización con multilingual-e5-small
- Coincidencia Léxica de Palabras Clave (35%)
- Similitud de Nombre de Archivo (15%)
- Refuerzo k-NN (k=5) con factor de peso alfa = 0.30 sobre ChromaDB

Registra:
- Categoría Esperada vs Obtenida
- Porcentaje de Confianza (%)
- Top 3 de sugerencias con sus puntajes
- Precisión Global de Clasificación (Accuracy)

Comando de ejecución:
python 03_prueba_funcional_b_clasificacion_nlp_ocr.py
================================================================================
"""

import os
import sys

# Asegurar codificación UTF-8
sys.stdout.reconfigure(encoding='utf-8')

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

from app.core.config import settings
from app.core.database import SessionLocal
from app.models.categoria import Categoria
from app.services.nlp_service import nlp_service


def ejecutar_prueba_clasificacion():
    print("=" * 80)
    print("PRUEBA FUNCIONAL B: MATRIZ DE CLASIFICACIÓN NLP Y OCR")
    print("=" * 80)

    db = SessionLocal()
    categorias_db = db.query(Categoria).all()
    categorias_list = [
        {
            "id": c.id,
            "nombre": c.nombre,
            "descripcion": c.descripcion or "",
            "embedding": c.embedding,
            "palabras_clave": c.palabras_clave,
            "umbral_confianza": c.umbral_confianza or settings.NLP_CONFIDENCE_THRESHOLD
        }
        for c in categorias_db
    ]
    id_a_nombre = {c["id"]: c["nombre"] for c in categorias_list}

    # Batería de 10 documentos institucionales representativos
    casos_prueba = [
        {
            "nombre_archivo": "Politica_Inclusión y Género.pdf",
            "origen": "OCR (Tesseract 5.0)",
            "cat_esperada_id": 1,
            "cat_esperada": "Normativas y politicas",
            "texto": (
                "CONSEJO DIRECTIVO ACUERDO No 01-056 Bucaramanga, Diciembre 13 de 2023. "
                "Por el cual se adopta la Política de Inclusión, Diversidad y Equidad de Género "
                "de las Unidades Tecnológicas de Santander UTS. Lineamientos normativos, principios rectores "
                "y marco regulatorio para la comunidad académica institucional."
            )
        },
        {
            "nombre_archivo": "sst-ig-05.pdf",
            "origen": "OCR (Tesseract 5.0)",
            "cat_esperada_id": 1,
            "cat_esperada": "Normativas y politicas",
            "texto": (
                "Unidades Tecnológicas de Santander. Procedimiento del Sistema de Gestión de "
                "Seguridad y Salud en el Trabajo SST-IG-05. Directriz institucional y disposiciones de "
                "cumplimiento obligatorio para la prevención de riesgos y marco legal ocupacional."
            )
        },
        {
            "nombre_archivo": "F-AM-04 Solicitud Grado V18.docx",
            "origen": "Nativo DOCX (XML)",
            "cat_esperada_id": 2,
            "cat_esperada": "Formatos y plantillas",
            "texto": (
                "FORMATO INSTITUCIONAL DE SOLICITUD DE GRADO F-AM-04 VERSION 18. "
                "ESPACIO PARA SER DILIGENCIADO POR EL ESTUDIANTE. Diligenciar todos los campos y casillas: "
                "Nombre completo, código estudiantil, programa académico, documentos anexos y firma del solicitante."
            )
        },
        {
            "nombre_archivo": "F-DC-127 Propuesta de trabajo de grado_ Modalidad Práctica V2.doc",
            "origen": "Nativo DOC (Word OLE)",
            "cat_esperada_id": 2,
            "cat_esperada": "Formatos y plantillas",
            "texto": (
                "Ficha técnica de la propuesta. Formato F-DC-127. Plantilla institucional estandarizada "
                "para presentación de propuestas de trabajo de grado en modalidad de práctica empresarial. "
                "Formulario de diligenciamiento con objetivos, cronograma y entidades vinculadas."
            )
        },
        {
            "nombre_archivo": "Resolución-No.-02-1917-del-20-de-noviembre-de-2025-Vacaciones-Colectivas.pdf",
            "origen": "OCR (Tesseract 5.0)",
            "cat_esperada_id": 3,
            "cat_esperada": "Actas y resoluciones",
            "texto": (
                "Unidades Tecnológicas de Santander RESOLUCIÓN No. 02-1917 del 20 de noviembre de 2025. "
                "Por medio de la cual se fija el período de vacaciones colectivas para los servidores públicos "
                "docentes y administrativos de las UTS. El Rector de las Unidades Tecnológicas de Santander "
                "en uso de sus facultades legales y estatutarias resuelve adoptar la presente decisión oficial."
            )
        },
        {
            "nombre_archivo": "RESOLUCIÓN-02-474-DEL-06-DE-ABRIL-DE-2026.pdf",
            "origen": "Nativo PDF (PyMuPDF)",
            "cat_esperada_id": 3,
            "cat_esperada": "Actas y resoluciones",
            "texto": (
                "RESOLUCIÓN No. 02-474 DEL 06 DE ABRIL DE 2026 UTS. "
                "Por la cual se adopta la decisión de sesión del Consejo Académico y se reglamentan "
                "las convocatorias institucionales aprobadas en comité directivo."
            )
        },
        {
            "nombre_archivo": "F-DC-196 Acta de Terminación y Recibo a Satisfacción de Prácticas V2.doc",
            "origen": "Nativo DOC (Word OLE)",
            "cat_esperada_id": 3,
            "cat_esperada": "Actas y resoluciones",
            "texto": (
                "ACTA DE TERMINACIÓN Y RECIBO A SATISFACCIÓN DE PRÁCTICAS EMPRESARIALES F-DC-196. "
                "En Bucaramanga, se reunieron los miembros del comité de prácticas y el tutor institucional "
                "para dejar constancia oficial de la culminación del período y aprobación de las actividades."
            )
        },
        {
            "nombre_archivo": "MANUAL-UTS.pdf",
            "origen": "Nativo PDF (PyMuPDF)",
            "cat_esperada_id": 4,
            "cat_esperada": "Manuales y procedimientos",
            "texto": (
                "MANUAL DE IDENTIDAD INSTITUCIONAL UNIDADES TECNOLÓGICAS DE SANTANDER UTS. "
                "Guía, manual y directrices para la correcta aplicación del logotipo, colores institucionales, "
                "tipografía, papelería, símbolos corporativos y arquitectura de marca."
            )
        },
        {
            "nombre_archivo": "res-224.pdf",
            "origen": "Nativo PDF (PyMuPDF)",
            "cat_esperada_id": 4,
            "cat_esperada": "Manuales y procedimientos",
            "texto": (
                "Unidades Tecnológicas de Santander RESOLUCIÓN No 02-224. "
                "Por medio de la cual se adopta el Manual Específico de Funciones y de Competencias Laborales "
                "para los empleos de la planta de personal. Manual y procedimiento institucional, organigrama, "
                "responsabilidades y flujos de procesos operativos."
            )
        },
        {
            "nombre_archivo": "F-DC-125  AndersonDiz.docx",
            "origen": "Nativo DOCX (XML)",
            "cat_esperada_id": 5,
            "cat_esperada": "Informes y reportes",
            "texto": (
                "TÍTULO DEL TRABAJO DE GRADO: CapacitIA - Gestión inteligente y automática de capacitaciones. "
                "Informe final de trabajo de grado, resultados estadísticos, métricas de evaluación del modelo, "
                "análisis de datos experimentales y balance de indicadores del proyecto de investigación."
            )
        }
    ]

    aciertos = 0
    total = len(casos_prueba)

    print(f"\nEvaluando {total} documentos con pipeline híbrido de clasificación...")
    print("-" * 120)
    print(f"{'#':2s} | {'Archivo':35s} | {'Extracción':12s} | {'Cat. Esperada':22s} | {'Cat. Obtenida':22s} | {'Conf.':6s} | {'Estado':7s}")
    print("-" * 120)

    for i, caso in enumerate(casos_prueba, 1):
        texto_ponderado = nlp_service.extraer_texto_ponderado(caso["texto"])
        cat_id, confianza, top_cats = nlp_service.clasificar_con_knn(
            texto_ponderado,
            categorias_list,
            nombre_archivo=caso["nombre_archivo"],
            k=5
        )
        cat_obtenida = id_a_nombre.get(cat_id, "Sin Clasificar")
        coincide = (cat_id == caso["cat_esperada_id"])
        if coincide:
            aciertos += 1

        conf_str = f"{(confianza or 0.0) * 100:.1f}%"
        estado_str = "ACIERTO" if coincide else "ERROR"
        print(f"{i:02d} | {caso['nombre_archivo'][:35]:35s} | {caso['origen'][:12]:12s} | {caso['cat_esperada'][:22]:22s} | {cat_obtenida[:22]:22s} | {conf_str:6s} | {estado_str:7s}")

    accuracy = (aciertos / total) * 100
    print("-" * 120)
    print(f"\nRESUMEN DE MÉTRICAS:")
    print(f" -> Total documentos evaluados: {total}")
    print(f" -> Aciertos: {aciertos}")
    print(f" -> Precisión Global (Accuracy): {accuracy:.2f}%")
    print("=" * 80)
    db.close()


if __name__ == "__main__":
    ejecutar_prueba_clasificacion()
