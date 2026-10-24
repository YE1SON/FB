# Estudio Editorial y Experimentación de FaithSpark Daily

Este documento describe la arquitectura editorial, los motores de generación de descripciones, las estrategias de hashtags, el sistema de experimentación A/B (grupos A1–B3) y las herramientas de validación de seguridad implementadas en JesusReels Studio para la página de Facebook **FaithSpark Daily**.

---

## 1. Flujo de Trabajo Editorial Integrado

La aplicación organiza la producción audiovisual y la publicación en un flujo continuo:

1. **Definición de Guion y Tema (Etapa 1)**: Selección del pilar temático y tema específico (catálogo de 26 temáticas), generación del guion (apertura, cuerpo, llamado a la acción opcional) y selección de la apertura más efectiva.
2. **Locución y Música (Etapa 2)**: Selección de voces recomendadas (Guy, Christopher, Brian) y pista de adoración en piano/acústico.
3. **Escenas Visuales (Etapa 3)**: Asignación de escenas basadas en el contenido real del guion para inicio, desarrollo y cierre.
4. **Subtítulos (Etapa 4)**: Estilo tipográfico limpio (*clean*), con márgenes de seguridad para la interfaz de Facebook Reels.
5. **Configuración Técnica (Etapa 5)**: Opciones de cámara, movimiento y mezcla de audio con normalización LUFS (-14 LUFS).
6. **Exportación, Optimización Editorial y Registro (Etapa 6)**:
   - Renderizado del archivo MP4 final en proporción vertical 9:16.
   - Generación de la descripción optimizada para Facebook basada en el **guion narrativo definitivo**.
   - Asignación de formato de copy (A o B) y estrategia de hashtags (0, 3 o 5).
   - Verificación de seguridad editorial previa a la publicación en tiempo real (*Preflight Check*).
   - Registro de observaciones y métricas de desempeño a las 48 horas y 7 días.

---

## 2. Generación de Descripciones para Facebook Reels

A diferencia de las versiones iniciales que generaban el texto de publicación al inicio y quedaban desactualizadas, el motor editorial actual (`engine/editorial_captions.py`) trabaja sobre el **guion final aprobado**:

### Formato A — Breve Emocional (~20–40 palabras)
- **Objetivo**: Conectar de forma inmediata con el estado emocional del espectador en su feed móvil, invitando a la pausa y la paz.
- **Estructura**:
  - Título breve con emojis sobrios (ej. `✝️ Rest in His Peace Tonight ✝️`).
  - Reflexión condensada de 20 a 40 palabras (sin contar hashtags ni versículo).
  - Cita bíblica canónica de apoyo.
  - Llamado a la acción suave y voluntario (ej. *"Save this prayer for whenever you need comfort"*).
  - Tono cálido, pastoral y en inglés estadounidense natural. Sin promesas milagrosas ni condicionamientos.

### Formato B — Reflexivo Contextual (~50–85 palabras)
- **Objetivo**: Fomentar la retención y la lectura reflexiva mediante una contextualización cotidiana de la prueba o desafío.
- **Estructura**:
  - Título temático.
  - Párrafo reflexivo de 50 a 85 palabras que aborda situaciones reales (hijos adultos distanciados, noches de insomnio, cargas financieras).
  - Cita bíblica canónica completa y verificada.
  - Pregunta o invitación final a la meditación personal.

### Detección de Guion Desactualizado (*Stale Caption Detection*)
Si el operador edita manualmente el gancho, cuerpo o llamado a la acción en la Etapa 1 después de haber generado la descripción, la interfaz de la Etapa 6 muestra una alerta no intrusiva:
> ⚠️ **El guion narrativo fue modificado.** La descripción actual puede no coincidir con tu locución. Haz clic abajo para regenerar.

El operador puede pulsar **"✨ Regenerar Descripción con Guion Actual"** para sincronizar el texto con la nueva locución o mantener sus ediciones manuales si así lo prefiere.

---

## 3. Catálogo y Estrategia de Hashtags Temáticos

Para evitar el uso de etiquetas genéricas o irrelevantes, el sistema cuenta con un catálogo curado que cubre las 26 temáticas del proyecto:

- **Estrategias disponibles**:
  1. `0 Tags`: Sin hashtags (evalúa el alcance algorítmico basado puramente en contenido y transcripción de audio).
  2. `3 Tags`: 3 hashtags específicos del tema (enfoque nicho de alta relevancia).
  3. `5 Tags`: 5 hashtags que combinan la temática específica con etiquetas de fe consolidadas.
- **Reglas de normalización**:
  - Preservación estricta de mayúsculas internas (*CamelCase*), por ejemplo: `#PrayingParents`, `#NightPrayer`, `#TrustingGod`.
  - Deduplicación insensible a mayúsculas y minúsculas (*case-insensitive*).
  - Eliminación de caracteres inválidos y signos de puntuación.
  - Sin afirmaciones falsas de "hashtags en tendencia".

---

## 4. Diseño Experimental A/B (Grupos A1 a B3)

Para evaluar qué combinaciones generan mayor tiempo medio de reproducción, retención y compartidos en la audiencia adulta de Estados Unidos, se estructuran 6 grupos experimentales:

| Grupo | Formato de Descripción | Cantidad de Hashtags | Enfoque Principal |
| :---: | :--- | :---: | :--- |
| **A1** | Formato A (Breve emocional) | 0 hashtags | Brevedad máxima, distribución limpia sin metadatos visibles |
| **A2** | Formato A (Breve emocional) | 3 hashtags | Mensaje rápido + etiquetas de nicho |
| **A3** | Formato A (Breve emocional) | 5 hashtags | Mensaje rápido + combinación balanceada de fe y nicho |
| **B1** | Formato B (Reflexivo contextual) | 0 hashtags | Lectura profunda guiada sin distracciones de etiquetas |
| **B2** | Formato B (Reflexivo contextual) | 3 hashtags | Contexto bíblico profundo + etiquetas temáticas |
| **B3** | Formato B (Reflexivo contextual) | 5 hashtags | Reflexión extendida + espectro temático completo |

### Matriz de Distribución de 18 Reels Iniciales
Para garantizar rigor estadístico y evitar sesgos temáticos o de horario, se define una matriz de 18 publicaciones equilibrada (3 repeticiones por grupo experimental) distribuida equitativamente entre las 3 temáticas iniciales prioritarias:
1. **Oración nocturna / paz para dormir** (*Night Prayer & Rest*).
2. **Padres preocupados por hijos adultos** (*Praying for Adult Children*).
3. **Dificultades económicas cotidianas** (*Trusting God in Financial Hardship*).

La interfaz incluye un botón **"🎯 Siguiente sugerido por matriz"** que consulta la API (`GET /api/editorial-experiment-matrix`) y preselecciona automáticamente el siguiente grupo experimental según el historial de publicaciones.

---

## 5. Validación Editorial de Seguridad (*Preflight Checklist*)

El módulo `engine/editorial_validator.py` ejecuta cinco análisis automáticos no bloqueantes antes de publicar:

1. **Detección de Español Accidental**: Escanea el texto público en busca de caracteres propios del español (`á, é, í, ó, ú, ñ, ¿, ¡`) o palabras en español para asegurar que todo el contenido dirigido a EE. UU. esté en inglés estadounidense impecable.
2. **Prevención de Manipulación o Superstición**: Bloquea o alerta sobre fórmulas manipulativas como *"Type Amen to claim your blessing"*, promesas de riqueza milagrosa (*"God will make you rich tomorrow"*), o condicionamientos de fe.
3. **Verificación Canónica de Escrituras**: Comprueba que la referencia citada corresponda a una estructura bíblica válida (*Libro Capítulo:Versículo*) y coincida con el catálogo de 26 escrituras autorizadas.
4. **Coherencia Narrativa (Alineación Guion–Copy)**: Verifica que las palabras clave de la descripción coincidan sustancialmente con el tema y la narración del video para evitar discrepancias que confundan al espectador.
5. **Detección de Contenido Duplicado**: Alerta si una descripción tiene más del 85% de similitud léxica con publicaciones recientes almacenadas en el registro histórico.

> **Principio de Diseño**: Las alertas son visibles y educativas, pero no bloquean la acción del operador si este decide publicar conscientemente.

---

## 6. Registro de Métricas y Bitácora de Desempeño

El archivo `data/editorial_results.json` almacena los datos de cada publicación y sus observaciones de métricas:

- **Identificación**: ID único del Reel, grupo experimental (`A1`–`B3`), temática, tipo de copy, lista de hashtags, URL de Facebook (opcional), fecha y duración en segundos.
- **Puntos de Control**:
  - **48 Horas**: Impulso inicial del algoritmo de Meta.
  - **7 Días**: Desempeño acumulado y estabilización de la audiencia.
- **Métricas Registradas**:
  - Visualizaciones (*views*)
  - Tiempo medio de reproducción en segundos (*avg_watch_time_sec*)
  - Porcentaje medio visualizado (*avg_watched_pct*)
  - Reacciones (*reactions*)
  - Comentarios (*comments*)
  - Compartidos (*shares*)
  - Seguidores ganados (*followers_gained*)
  - Porcentaje de audiencia en Estados Unidos (*us_viewer_pct*)

### Preservación de Datos: Vacío vs Cero Real
> [!IMPORTANT]
> Se mantiene una distinción estricta entre una métrica aún no observada (`null` en JSON, celda vacía `""` en CSV) y un valor medido real de cero (`0`). Nunca se reemplazan datos faltantes con ceros artificiales.

### Exportación de Datos
El operador puede descargar en cualquier momento la base de datos completa de experimentos mediante dos accesos directos en la interfaz o a través de los endpoints:
- `GET /api/editorial-results/export/csv`: Archivo CSV listo para análisis en hojas de cálculo (Excel, Google Sheets).
- `GET /api/editorial-results/export/json`: Objeto JSON estructurado para modelado o scripts automatizados.

---

## 7. Eliminación de Llamados a la Acción Forzados

En versiones anteriores, `generate_script` en `engine/scripts.py` forzaba la inserción de un llamado a la acción solicitando nombres (*"Leave your first name below..."*) cuando no se especificaba uno. Esta lógica fue corregida:
- Si el usuario desmarca la opción de incluir CTA (`include_cta: False`), el guion se genera sin ningún llamado forzado.
- Los llamados a la acción generados respetan el formato pastoral de FaithSpark Daily, priorizando la salvación del video, la oración reflexiva o la meditación personal sobre el compromiso forzado.

---

## 8. Verificación Técnica y Pruebas Automatizadas

La suite completa de pruebas unitarias y de integración se ejecuta con:

```bash
# Pruebas específicas del sistema de experimentación y validación editorial (17 pruebas)
python -m unittest tests/test_editorial_experimentation.py -v

# Suite completa de regresión y calidad (35 pruebas totales)
python -m unittest discover -s tests -v

# Comprobación de sintaxis en frontend
node --check static/app.js
```

Todas las 35 pruebas pasan limpiamente con 0 errores.
