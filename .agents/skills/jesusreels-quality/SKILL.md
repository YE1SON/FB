---
name: jesusreels-quality
description: Guía de calidad, auditoría narrativa y verificación técnica audiovisual para JesusReels Studio. Utilizar al evaluar guiones, sintetizar locuciones, alinear subtítulos, componer videos o validar cambios en el proyecto. Invocable manualmente mediante /jesusreels-quality.
---

# JesusReels Quality Skill

Esta habilidad define los estándares de calidad narrativa, teológica y audiovisual para **JesusReels Studio**, orientada a crear videos devocionales y reflexivos en formato vertical (9:16) para una audiencia adulta de Estados Unidos.

Invocación manual: `/jesusreels-quality`

---

## 1. Los 9 Principios de Calidad

### 1. Calidad Narrativa y Especificidad Humana
- Cada guion debe responder a una situación o necesidad humana concreta (ej. agotamiento al final del día, incertidumbre laboral, soledad, preocupación por un hijo).
- **Prohibido:** Afirmar conocer la vida privada del espectador de forma mágica, prometer soluciones financieras inmediatas, curaciones garantizadas o convertir la visualización del video en una señal de intervención divina.

### 2. Detección y Prevención de Repeticiones
- Un guion no es diferente solo por cambiar una palabra o un nombre propio.
- Alternar entre distintas perspectivas dentro del catálogo temático: oración íntima, reflexión bíblica, relato breve con moraleja espiritual, acompañamiento en el dolor o pausa de gratitud.

### 3. Coherencia Escénica y Visual (3 Escenas)
- **Escena 1 (Apertura):** Establece el contexto y la atmósfera de la situación sin recurrir a imágenes desconectadas.
- **Escena 2 (Desarrollo):** Ilustra visualmente el mensaje central o la acción de fe (oración, reflexión, lectura de las Escrituras).
- **Escena 3 (Resolución / Cierre):** Acompaña el cierre con un tono de serenidad y esperanza coherente con el desenlace del guion.
- Evitar sobrecargar los prompts con adjetivos vacíos ("8k, cinematic, masterpiece"); describir sujeto, acción, iluminación y composición.

### 4. Naturalidad de la Narración en Inglés Estadounidense
- Redacción en inglés estadounidense contemporáneo, claro y digno.
- Evitar estructuras calco del español o frases rimbombantes artificiales.
- El tono debe transmitir serenidad, empatía y reverencia sin teatralidad forzada.

### 5. Correspondencia Texto-Audio y Pausas Naturales
- El audio sintetizado debe reproducir con fidelidad el texto del guion.
- Las transiciones entre Gancho, Desarrollo y Cierre deben contener pausas naturales (~300-500ms) sin cortes de volumen abruptos ni degradación acústica.

### 6. Subtítulos: Legibilidad, Sincronización y Zonas Seguras
- **Estilo Predeterminado:** Tipografía sans-serif limpia (Montserrat o DejaVu Sans), alto contraste, 1 a 2 líneas como máximo.
- **Zonas Seguras:** Mantener un margen inferior de al menos 420px (en resolución 1080x1920) para evitar que los subtítulos queden ocultos bajo la descripción o controles de la interfaz de Reels.
- **Sincronización:** Basada en marcas por palabra reales (Faster-Whisper con VAD). Si se usa un método de respaldo, no simular precisión al milisegundo por palabra: presentar bloques a nivel de segmento.

### 7. Publicaciones, Descripciones y Hashtags
- La descripción de la publicación debe redactarse a partir del mensaje real del video.
- Incluir la cita bíblica verificada cuando corresponda.
- Utilizar entre 3 y 5 hashtags estrictamente pertinentes a la temática tratada; evitar listas globales fijas e indiscriminadas.

### 8. Control de Duración (Objetivo vs. Real)
- Formato habitual recomendado: **18 a 25 segundos**.
- Distinguir y reportar siempre:
  1. *Duración objetivo* (seleccionada en la configuración).
  2. *Duración estimada del audio* (basada en recuento de palabras).
  3. *Duración real del archivo exportado* (inspeccionada con `ffprobe`).
- Registrar cualquier discrepancia significativa (>3 segundos).

### 9. Verificación Obligatoria Antes de Publicar Cambios
- Antes de dar por terminado cualquier cambio en el motor o la interfaz:
  - Compilar archivos modificados con `py_compile`.
  - Ejecutar el script de validación reproducible de la habilidad.
  - Verificar que las rutas HTTP conservan compatibilidad.

---

## 2. Procedimiento de Validación Reproducible

Para verificar que un lote o una actualización cumple con estos criterios, ejecutar:

```powershell
python .agents/skills/jesusreels-quality/scripts/validate_script_quality.py
```

### Criterios de Aceptación del Validador:
1. `valid_json`: La respuesta es un objeto JSON válido con todos los campos requeridos (`theme_key`, `hook`, `body`, `closing`, `cta`, `scripture`, `hashtags`, `scene_1_prompt`, `scene_2_prompt`, `scene_3_prompt`).
2. `no_clickbait`: Ausencia de términos prohibidos (`stop scrolling`, `comment amen to receive`, `urgent message from god`, `financial miracle`).
3. `duration_in_range`: Duración estimada entre 15.0s y 35.0s (con objetivo estándar en 18–25s).
4. `biblical_accuracy`: La referencia bíblica corresponde al catálogo validado.
5. `clean_prompts`: Prompts de imagen sin relleno de palabras vacías ("8k, photorealistic masterpiece").
