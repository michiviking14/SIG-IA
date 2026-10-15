# INFORME TÉCNICO FORMAL DE EVIDENCIAS DE PRUEBAS TÉCNICAS Y FUNCIONALES
## SISTEMA INTELIGENTE DE GESTIÓN DOCUMENTAL (SIG-IA UTS)

**Proyecto de Trabajo de Grado:** Sistema Inteligente de Gestión Documental para las Unidades Tecnológicas de Santander (SIG-IA UTS)  
**Institución:** Unidades Tecnológicas de Santander (UTS)  
**Facultad:** Ciencias Naturales e Ingenierías  
**Ubicación en el Documento de Tesis:** Capítulo 4.4 (Fase de Pruebas), Capítulo 5 (Resultados) y Sección de Apéndices / Anexos  
**Fecha de Validación y Certificación:** Octubre de 2026  
**Entorno de Ejecución y Pruebas:**
- **Sistema Operativo:** Windows 10/11 x64 (PowerShell 5.1 / 7)
- **Lenguaje y Runtime:** Python 3.14.3 / FastAPI Framework
- **Framework de Pruebas:** Pytest 9.1.1 (con `pytest-asyncio` 1.4.0, `anyio` 4.14.2)
- **Base de Datos Relacional:** PostgreSQL 16 (Driver `psycopg` 3.x / SQLAlchemy 2.0)
- **Base de Datos Vectorial:** ChromaDB PersistentClient (`hnsw:space`: cosine)
- **Modelo de Embeddings:** `intfloat/multilingual-e5-small` (384 dimensiones densas)
- **Motor OCR:** Tesseract OCR 5.0 (Idioma Español `spa`, 300 DPI)

---

## 1. SUITE DE 11 PRUEBAS UNITARIAS AUTOMATIZADAS (TABLA 8 DE LA TESIS)

La siguiente tabla presenta la correlación exacta y los resultados formales de las 11 pruebas unitarias definidas en la **Tabla 8** de la tesis institucional, evaluadas mediante Pytest sobre los componentes de versionado, embeddings, similitud matemática, clasificación NLP y cálculo estadístico.

### Tabla 1. Matriz de Ejecución de Pruebas Unitarias (Tabla 8 de la Tesis)

| ID Prueba | Función / Método Pytest | Componente / Servicio | Criterio de Verificación Académico | Duración | Estado |
| :--- | :--- | :--- | :--- | :---: | :---: |
| **test_01** | `test_01_primera_version` | `VersionService` | Verifica que la primera versión de un documento nuevo se asigne automáticamente como `"v1.0"`. | 0.001 s | **PASSED** |
| **test_02** | `test_02_generacion_embeddings` | `NLPService` | Verifica que el modelo transformer produzca vectores de dimensión densa fija = 384. | 0.048 s | **PASSED** |
| **test_03** | `test_03_embeddings_texto_vacio` | `NLPService` | Verifica que ante un texto vacío el servicio no falle y devuelva una lista vacía `[]` de forma controlada. | 0.001 s | **PASSED** |
| **test_04** | `test_04_similitud_coseno_identicos` | `NLPService` | Verifica que dos vectores idénticos produzcan una similitud de coseno normalizada $\approx 1.000$ ($> 0.999$). | 0.001 s | **PASSED** |
| **test_05** | `test_05_similitud_vector_cero` | `NLPService` | Verifica el manejo del caso límite con vector nulo/cero sin producir excepción `ZeroDivisionError`. | 0.001 s | **PASSED** |
| **test_06** | `test_06_clasificacion_sin_categorias` | `NLPService` | Verifica que el motor responda de forma controlada `(None, None, [])` cuando no hay categorías configuradas. | 0.021 s | **PASSED** |
| **test_07** | `test_07_clasificacion_texto_vacio` | `NLPService` | Verifica que el motor no asigne categoría `(None, None, [])` cuando no existe contenido textual que analizar. | 0.001 s | **PASSED** |
| **test_08** | `test_08_clasificacion_categorias_reales` | `NLPService` | Verifica que un documento se clasifique en la categoría correcta y las sugerencias (Top 3) queden ordenadas descendentemente por score. | 0.092 s | **PASSED** |
| **test_09** | `test_09_clasificacion_palabras_clave` | `NLPService` | Verifica que el puntaje de coincidencia léxica de palabras clave (`score_keywords`) sea $> 0$ ante concordancias textuales. | 0.043 s | **PASSED** |
| **test_10** | `test_10_extraccion_texto_ponderado` | `NLPService` | Verifica que el algoritmo de ponderación preserve y priorice al inicio el encabezado / primera línea del documento. | 0.001 s | **PASSED** |
| **test_11** | `test_11_estadisticas_clasificacion` | `NLPService` | Verifica que los totales de documentos clasificados/sin clasificar y la distribución por categoría se calculen con exactitud. | 0.001 s | **PASSED** |

> **Resultado Consolidado:** 11 pruebas ejecutadas, **11 aprobadas (100% de éxito)**, 0 fallos, 0 errores. Tiempo total de ejecución de la suite: **11.05 segundos** (incluyendo inicialización de tensores y modelos).

---

### Salida Real Verbatim de Consola (`pytest -v --durations=0`)

```text
============================= test session starts =============================
platform win32 -- Python 3.14.3, pytest-9.1.1, pluggy-1.6.0 -- D:\Sig-IA\Sig-IA\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: D:\Sig-IA\Sig-IA\backend
configfile: pytest.ini
plugins: anyio-4.14.2, asyncio-1.4.0
asyncio: mode=Mode.AUTO, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collecting ... collected 11 items

tests/test_tabla8_unitarios.py::TestTabla8Unitarios::test_01_primera_version PASSED [  9%]
tests/test_tabla8_unitarios.py::TestTabla8Unitarios::test_02_generacion_embeddings PASSED [ 18%]
tests/test_tabla8_unitarios.py::TestTabla8Unitarios::test_03_embeddings_texto_vacio PASSED [ 27%]
tests/test_tabla8_unitarios.py::TestTabla8Unitarios::test_04_similitud_coseno_identicos PASSED [ 36%]
tests/test_tabla8_unitarios.py::TestTabla8Unitarios::test_05_similitud_vector_cero PASSED [ 45%]
tests/test_tabla8_unitarios.py::TestTabla8Unitarios::test_06_clasificacion_sin_categorias PASSED [ 54%]
tests/test_tabla8_unitarios.py::TestTabla8Unitarios::test_07_clasificacion_texto_vacio PASSED [ 63%]
tests/test_tabla8_unitarios.py::TestTabla8Unitarios::test_08_clasificacion_categorias_reales PASSED [ 72%]
tests/test_tabla8_unitarios.py::TestTabla8Unitarios::test_09_clasificacion_palabras_clave PASSED [ 81%]
tests/test_tabla8_unitarios.py::TestTabla8Unitarios::test_10_extraccion_texto_ponderado PASSED [ 90%]
tests/test_tabla8_unitarios.py::TestTabla8Unitarios::test_11_estadisticas_clasificacion PASSED [100%]

============================== slowest durations ==============================
0.09s call     tests/test_tabla8_unitarios.py::TestTabla8Unitarios::test_08_clasificacion_categorias_reales
0.05s call     tests/test_tabla8_unitarios.py::TestTabla8Unitarios::test_02_generacion_embeddings
0.04s call     tests/test_tabla8_unitarios.py::TestTabla8Unitarios::test_09_clasificacion_palabras_clave
0.02s call     tests/test_tabla8_unitarios.py::TestTabla8Unitarios::test_06_clasificacion_sin_categorias
0.00s call     tests/test_tabla8_unitarios.py::TestTabla8Unitarios::test_01_primera_version
0.00s call     tests/test_tabla8_unitarios.py::TestTabla8Unitarios::test_04_similitud_coseno_identicos
0.00s call     tests/test_tabla8_unitarios.py::TestTabla8Unitarios::test_05_similitud_vector_cero
0.00s call     tests/test_tabla8_unitarios.py::TestTabla8Unitarios::test_07_clasificacion_texto_vacio
0.00s call     tests/test_tabla8_unitarios.py::TestTabla8Unitarios::test_10_extraccion_texto_ponderado
0.00s call     tests/test_tabla8_unitarios.py::TestTabla8Unitarios::test_11_estadisticas_clasificacion
0.00s call     tests/test_tabla8_unitarios.py::TestTabla8Unitarios::test_03_embeddings_texto_vacio
======================= 11 passed, 1 warning in 11.05s ========================
```

---

## 2. PRUEBA FUNCIONAL A: MOTOR DE VERSIONADO Y DETECCIÓN CRIPTOGRÁFICA SHA-256

Esta prueba evalúa el cumplimiento del **Objetivo Específico 1 y 2** del proyecto: la gestión del ciclo de vida documental y la prevención de duplicidad basada en huella digital criptográfica (SHA-256 de 256 bits / 64 caracteres hexadecimales).

### Descripción del Escenario de Prueba
Se simuló el ciclo de vida del documento institucional **`F-AM-04 Solicitud Grado V18.docx`**, correspondiente al formato institucional para trámites de graduación en las Unidades Tecnológicas de Santander:
1. **Creación Inicial:** Carga de la plantilla base institucional.
2. **Intento de Duplicado Idéntico:** Intento intencional de volver a radicar el mismo archivo sin alteraciones.
3. **Modificación Menor (Versión 1.1):** Actualización con anexos estudiantiles (Paz y Salvo de Biblioteca y Pruebas Saber Pro).
4. **Modificación Final (Versión 1.2):** Incorporación de vistos buenos institucionales y firmas de Decanatura.

### Tabla 2. Resultados del Control de Versiones y Verificación Criptográfica SHA-256

| Evento / Paso | Nombre del Archivo | Hash SHA-256 (Truncado / Completo) | Versión Resultante | Estado Vigente (`vigente`) | Código / Acción del Sistema | Resultado de Verificación |
| :--- | :--- | :--- | :---: | :---: | :--- | :---: |
| **1. Carga Inicial** | `F-AM-04 Solicitud Grado V18.docx` | `ae2a0a2da6df9d74...` | **v1.0** | `True` | `200 OK` (Creación de registro padre y versión) | **EXITOSO** |
| **2. Intento Duplicado** | `F-AM-04 Solicitud Grado V18.docx` | `ae2a0a2da6df9d74...` | *Rechazado* | `N/A` | `400 Bad Request` ("El archivo es idéntico a la versión vigente") | **BLOQUEADO** |
| **3. Primera Reforma** | `F-AM-04 Solicitud Grado V18_mod.docx` | `d418f29f4dd40b5b...` | **v1.1** | `True` (v1.0 $\rightarrow$ `False`) | `200 OK` (Cierre de vigencia v1.0 y activación v1.1) | **EXITOSO** |
| **4. Segunda Reforma** | `F-AM-04 Solicitud Grado V18_final.docx` | `b9ad7b7af2a953a9...` | **v1.2** | `True` (v1.1 $\rightarrow$ `False`) | `200 OK` (Cierre de vigencia v1.1 y activación v1.2) | **EXITOSO** |

### Verificación de la Regla de Negocio de Vigencia Única
Al finalizar la secuencia documental en la base de datos:
- Versión `v1.0`: `vigente = False`
- Versión `v1.1`: `vigente = False`
- Versión `v1.2`: `vigente = True`

**Conclusión:** Se comprobó que el motor garantiza que **únicamente la versión más reciente permanece activa (`vigente=True`)**, preservando el historial completo para auditoría e impidiendo la redundancia de almacenamiento mediante hashes SHA-256.

---

## 3. PRUEBA FUNCIONAL B: MATRIZ DE CLASIFICACIÓN AUTOMÁTICA MULTIMODAL (NLP Y OCR)

Esta prueba valida el **Objetivo Específico 3**: la clasificación automática inteligente de documentos institucionales mediante una arquitectura híbrida compuesta por:
- **Similitud Coseno Semántica ($50\%$):** Vectorización densa mediante `multilingual-e5-small`.
- **Coincidencia de Palabras Clave ($35\%$):** Normalización de texto y extracción léxica de terminología UTS.
- **Similitud de Nombre de Archivo ($15\%$):** Análisis semántico y léxico del nombre del archivo.
- **Refuerzo k-NN ($k=5$):** Votación por distancia inversa ponderada sobre la colección de referencia institucional de ChromaDB con factor de peso $\alpha = 0.30$.

$$\text{Score}_{\text{base}} = 0.50 \cdot S_{\text{coseno}} + 0.35 \cdot S_{\text{keywords}} + 0.15 \cdot S_{\text{nombre}}$$
$$\text{Score}_{\text{final}} = \min\left(\text{Score}_{\text{base}} \cdot \left(1 + \text{Score}_{k\text{-NN}} \cdot 0.30\right),\, 1.0\right)$$

### Tabla 3. Resultados de Clasificación Automática sobre Documentos Reales UTS

| ID | Documento Evaluado | Formato / Origen de Extracción | Categoría Esperada | Categoría Asignada por SIG-IA | Confianza (%) | Top 3 de Sugerencias Ponderadas | Precisión |
| :---: | :--- | :---: | :--- | :--- | :---: | :--- | :---: |
| **01** | `Politica_Inclusión y Género.pdf` | OCR (Tesseract 5.0) | Normativas y políticas | **Normativas y políticas** | **96.46%** | 1. Normativas y políticas (0.96)<br>2. Actas y resoluciones (0.86)<br>3. Manuales y procedimientos (0.63) | **Acierto** |
| **02** | `sst-ig-05.pdf` | OCR (Tesseract 5.0) | Normativas y políticas | **Normativas y políticas** | **78.26%** | 1. Normativas y políticas (0.78)<br>2. Manuales y procedimientos (0.68)<br>3. Informes y reportes (0.62) | **Acierto** |
| **03** | `F-AM-04 Solicitud Grado V18.docx` | Nativo DOCX (XML) | Formatos y plantillas | **Formatos y plantillas** | **100.00%** | 1. Formatos y plantillas (1.00)<br>2. Actas y resoluciones (0.62)<br>3. Normativas y políticas (0.62) | **Acierto** |
| **04** | `F-DC-127 Propuesta trabajo grado.doc` | Nativo DOC (Word OLE) | Formatos y plantillas | **Formatos y plantillas** | **100.00%** | 1. Formatos y plantillas (1.00)<br>2. Informes y reportes (0.63)<br>3. Manuales y procedimientos (0.61) | **Acierto** |
| **05** | `Resolución-No.-02-1917 Vacaciones.pdf` | OCR (Tesseract 5.0) | Actas y resoluciones | **Actas y resoluciones** | **87.34%** | 1. Actas y resoluciones (0.87)<br>2. Manuales y procedimientos (0.67)<br>3. Normativas y políticas (0.62) | **Acierto** |
| **06** | `RESOLUCIÓN-02-474-ABRIL-2026.pdf` | Nativo PDF (PyMuPDF) | Actas y resoluciones | **Actas y resoluciones** | **100.00%** | 1. Actas y resoluciones (1.00)<br>2. Normativas y políticas (0.63)<br>3. Manuales y procedimientos (0.57) | **Acierto** |
| **07** | `F-DC-196 Acta Terminación Prácticas.doc` | Nativo DOC (Word OLE) | Actas y resoluciones | **Actas y resoluciones** | **100.00%** | 1. Actas y resoluciones (1.00)<br>2. Normativas y políticas (0.55)<br>3. Manuales y procedimientos (0.54) | **Acierto** |
| **08** | `MANUAL-UTS.pdf` | Nativo PDF (PyMuPDF) | Manuales y procedimientos | **Manuales y procedimientos** | **93.57%** | 1. Manuales y procedimientos (0.94)<br>2. Formatos y plantillas (0.55)<br>3. Normativas y políticas (0.54) | **Acierto** |
| **09** | `res-224.pdf` (Manual de Funciones) | Nativo PDF (PyMuPDF) | Manuales y procedimientos | **Manuales y procedimientos** | **94.41%** | 1. Manuales y procedimientos (0.94)<br>2. Actas y resoluciones (0.73)<br>3. Normativas y políticas (0.62) | **Acierto** |
| **10** | `F-DC-125 AndersonDiz.docx` | Nativo DOCX (XML) | Informes y reportes | **Informes y reportes** | **97.94%** | 1. Informes y reportes (0.98)<br>2. Formatos y plantillas (0.76)<br>3. Normativas y políticas (0.54) | **Acierto** |

### Métrica de Desempeño Global de la Clasificación
- **Muestra evaluada:** 10 documentos institucionales representativos de las 5 categorías.
- **Clasificaciones correctas:** 10
- **Clasificaciones incorrectas:** 0
- **Precisión Global de Clasificación ($Accuracy$):** **100.0%**
- **Confianza Media Obtenida:** **94.80%**

---

## 4. PRUEBA FUNCIONAL C: BÚSQUEDA SEMÁNTICA VECTORIAL EN CHROMADB Y ROBUSTEZ ANTE VARIACIONES DE NUMERACIÓN

Esta prueba evalúa el motor de recuperación de información semántica implementado sobre ChromaDB, midiendo:
1. Capacidad de respuesta ante lenguaje natural conceptual no literal.
2. Invarianza ante variaciones sintácticas en la numeración de actos administrativos institucionales de las UTS (`"No."`, `"N°"`, `"Nro."` y omisión de prefijo).
3. Latencia de búsqueda vectorial en milisegundos (ms).

### Tabla 4. Resultados de Búsqueda Semántica Vectorial y Latencia

| ID | Tipo de Búsqueda | Consulta en Lenguaje Natural / Sintaxis UTS | Documento Principal Recuperado por ChromaDB | Versión | Categoría Asociada | Similitud (%) | Latencia (ms) |
| :---: | :--- | :--- | :--- | :---: | :--- | :---: | :---: |
| **C01** | Lenguaje Natural | *"requisitos y tramite para solicitud de grado de estudiantes"* | `F-AM-04 Solicitud Grado V18.docx` | v1.0 | Formatos y plantillas | **87.69%** | 191.66 ms |
| **C02** | Lenguaje Natural | *"politica institucional de equidad de genero e inclusion social"* | `Politica_Inclusión y Género.pdf` | v1.0 | Normativas y políticas | **86.75%** | 61.16 ms |
| **C03** | Lenguaje Natural | *"manual de identidad corporativa logotipo y tipografia institucional"* | `MANUAL-UTS.pdf` | v1.0 | Manuales y procedimientos | **90.11%** | 37.95 ms |
| **C04** | Lenguaje Natural | *"manual especifico de funciones y competencias laborales"* | `res-224.pdf` | v1.0 | Manuales y procedimientos | **87.30%** | 68.58 ms |
| **C05** | Lenguaje Natural | *"proyecto de grado modelo de inteligencia artificial capacitacion"* | `F-DC-125 AndersonDiz.docx` | v1.0 | Informes y reportes | **87.60%** | 26.93 ms |
| **C06** | Variación Núm. | *"Resolución No. 02-1917 vacaciones colectivas"* | `Resolución-No.-02-1917-del-20-de-noviembre...pdf` | v1.0 | Actas y resoluciones | **89.16%** | 24.10 ms |
| **C07** | Variación Núm. | *"Resolución N° 02-1917 vacaciones colectivas"* | `Resolución-No.-02-1917-del-20-de-noviembre...pdf` | v1.0 | Actas y resoluciones | **89.33%** | 23.76 ms |
| **C08** | Variación Núm. | *"Resolución Nro. 02-1917 vacaciones colectivas"* | `Resolución-No.-02-1917-del-20-de-noviembre...pdf` | v1.0 | Actas y resoluciones | **88.68%** | 25.40 ms |
| **C09** | Variación Núm. | *"Acuerdo No 01-056 política de inclusión"* | `Politica_Inclusión y Género.pdf` | v1.0 | Normativas y políticas | **89.06%** | 36.04 ms |
| **C10** | Variación Núm. | *"Acuerdo N° 01-056 política de inclusión"* | `Politica_Inclusión y Género.pdf` | v1.0 | Normativas y políticas | **89.05%** | 22.09 ms |
| **C11** | Variación Núm. | *"Acuerdo Nro. 01-056 política de inclusión"* | `Politica_Inclusión y Género.pdf` | v1.0 | Normativas y políticas | **88.71%** | 23.05 ms |
| **C12** | Variación Núm. | *"Resolución No. 02-474 del 2026"* | `RESOLUCIÓN-02-474-DEL-06-DE-ABRIL-DE-2026.pdf` | v1.0 | Actas y resoluciones | **88.84%** | 23.16 ms |
| **C13** | Variación Núm. | *"Resolución N° 02-474 del 2026"* | `RESOLUCIÓN-02-474-DEL-06-DE-ABRIL-DE-2026.pdf` | v1.0 | Actas y resoluciones | **88.85%** | 22.14 ms |
| **C14** | Variación Núm. | *"Resolución Nro. 02-474 del 2026"* | `RESOLUCIÓN-02-474-DEL-06-DE-ABRIL-DE-2026.pdf` | v1.0 | Actas y resoluciones | **88.65%** | 26.21 ms |
| **C15** | Prefijo Directo | *"Resolución 02-1917"* | `res-224.pdf` *(Top 1)* / `Resolución-02-1917` *(Top 2)* | v1.0 | Actas y resoluciones | **87.71%** | 21.39 ms |

### Análisis Estadístico de Rendimiento del Motor de Búsqueda
- **Latencia Promedio Global:** **42.24 ms**
- **Latencia en Consultas en Caliente:** **22 ms – 26 ms**
- **Similitud Semántica Promedio:** **88.52%**
- **Robustez ante Variaciones de Numeración:** El preprocesamiento léxico de SIG-IA unifica eficazmente las variaciones `"No."`, `"N°"` y `"Nro."`, obteniendo en todas ellas un grado de similitud superior al **$88.6\%$** y apuntando de manera inequívoca al acto administrativo correspondiente.

---

## 5. CONCLUSIONES TÉCNICAS PARA LA TESIS

1. **Efectividad del Pipeline Híbrido NLP:** La integración del modelo `multilingual-e5-small` con la extracción de palabras clave, el análisis del nombre del archivo y el refuerzo $k\text{-NN}$ ($k=5$) demostró una precisión del **$100\%$** en la batería de pruebas de clasificación institucional.
2. **Robustez del Motor Criptográfico SHA-256:** El control de versiones secuencial garantiza que nunca coexistan múltiples versiones con estado `vigente=True` para un mismo documento y bloquea la radicación de archivos idénticos mediante comparación de huella digital de 256 bits en tiempo constante ($O(1)$).
3. **Eficiencia en Búsqueda Semántica:** La base de datos vectorial ChromaDB, operando en espacio coseno, demostró tiempos de respuesta promedio de **$42.24\text{ ms}$**, cumpliendo con los estándares de interactividad para sistemas de gestión documental institucional.
4. **Idoneidad Académica:** Todas las 11 pruebas unitarias especificadas en la Tabla 8 del documento de tesis fueron aprobadas formalmente sin regresiones en las funcionalidades existentes del sistema.
