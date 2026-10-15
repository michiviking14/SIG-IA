# ANEXOS DE PRUEBAS TÉCNICAS Y FUNCIONALES - PROYECTO SIG-IA UTS

Esta carpeta reúne la totalidad de los códigos fuente de pruebas técnicas y funcionales desarrolladas y certificadas para el **Informe Final de Trabajo de Grado (Capítulo 4.4 Fase de Pruebas, Capítulo 5 Resultados y Sección de Anexos/Apéndices)** del sistema **SIG-IA UTS**.

---

## 📁 Estructura de Archivos en esta Carpeta

| Archivo | Tipo de Prueba | Descripción Académica | Referencia en Tesis |
| :--- | :--- | :--- | :--- |
| **`01_pruebas_unitarias_tabla8.py`** | Pytest Unitario | Suite formal de las **11 pruebas unitarias** documentadas en la Tabla 8 del documento de grado (versionado, embeddings 384 dims, manejo de texto vacío, similitud coseno, vector cero, clasificación y estadísticas). | **Capítulo 4.4 (Tabla 8)** |
| **`02_prueba_funcional_a_versionado_sha256.py`** | Funcional (Objetivo 1 y 2) | Script ejecutable que simula el ciclo de vida secuencial del formato `F-AM-04 Solicitud Grado V18.docx` (`v1.0` $\rightarrow$ `v1.1` $\rightarrow$ `v1.2`), bloqueo de duplicados por hash exacto y verificación de `vigente=True` exclusivo. | **Capítulo 4.4 y 5.1** |
| **`03_prueba_funcional_b_clasificacion_nlp_ocr.py`** | Funcional (Objetivo 3) | Evaluación de la matriz de clasificación híbrida (50% coseno, 35% keywords, 15% nombre + $k\text{-NN}$ $k=5$) sobre 10 documentos reales en las 5 categorías institucionales (PDFs con OCR Tesseract, DOCX y DOC OLE). | **Capítulo 4.4 y 5.2** |
| **`04_prueba_funcional_c_busqueda_semantica_chroma.py`** | Funcional (Objetivo 4) | Búsqueda semántica vectorial en ChromaDB evaluando consultas conceptuales en lenguaje natural y variaciones de numeración institucional (`"No."`, `"N°"`, `"Nro."`), midiendo similitud (%) y latencia (ms). | **Capítulo 4.4 y 5.3** |
| **`05_ejecutor_todas_las_pruebas.py`** | Ejecutor Maestro | Script integrador que corre secuencialmente todos los bloques de pruebas y genera en consola el informe de aprobación consolidado. | **Resumen General de Anexos** |
| **`06_pruebas_unitarias_completas_sistema.py`** | Pytest Suite General | Suite extendida con las 23 pruebas de servicios del backend (incluyendo soporte de archivos legacy `.doc` OLE binario, RTF y filtros de fecha en ChromaDB). | **Apéndice de Software** |
| **`07_pruebas_deteccion_colision_versiones.py`** | Pytest Detección Versiones | Suite de pruebas especializadas en extracción de códigos institucionales UTS (`F-AM-04`, `F-DC-125`, `SST-IG-05`, `RES-02-979`) y veto de colisiones. | **Apéndice de Software** |

---

## 🚀 Instrucciones de Ejecución

Todos los scripts pueden ejecutarse de manera individual o consolidada utilizando el entorno virtual del proyecto (`.venv`):

### 1. Ejecutar la Suite de 11 Pruebas Unitarias (Tabla 8):
```bash
pytest anexos_pruebas/01_pruebas_unitarias_tabla8.py -v --durations=0
```

### 2. Ejecutar las Pruebas Funcionales Individualmente:
```bash
# Prueba Funcional A (Versionado y SHA-256):
python anexos_pruebas/02_prueba_funcional_a_versionado_sha256.py

# Prueba Funcional B (Clasificación NLP y OCR):
python anexos_pruebas/03_prueba_funcional_b_clasificacion_nlp_ocr.py

# Prueba Funcional C (Búsqueda Semántica ChromaDB):
python anexos_pruebas/04_prueba_funcional_c_busqueda_semantica_chroma.py
```

### 3. Ejecutar Todas las Pruebas en una Sola Corrida:
```bash
python anexos_pruebas/05_ejecutor_todas_las_pruebas.py
```

---

## 📊 Documento de Resultados y Tablas Formateadas
El reporte formal con tablas académicas, fórmulas matemáticas y salidas reales de consola listas para ser incorporadas al cuerpo del documento de tesis se encuentra en:
- `REPORTE_PRUEBAS_TESIS.md`
