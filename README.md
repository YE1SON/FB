# JesusReels Studio ✝️
### Creador de Vídeos y Reels Cristianos de Alta Retención para Facebook (Audiencia de EE. UU.)

Una aplicación completa, ligera y **100% gratuita** (sin costes de API, sin suscripciones y sin límites) diseñada específicamente para crear Reels y vídeos verticales (1080x1920) de alto impacto visual y emocional para una página de Facebook con público en Estados Unidos.

---

## 🚀 Cómo Iniciar la Aplicación

1. **Opción rápida:** Haz doble clic sobre el archivo **`start.bat`**.
2. **O desde la terminal:**
   ```bash
   python server.py
   ```
3. Se abrirá automáticamente tu navegador en **`http://127.0.0.1:8050`**.

---

## 🎯 La Fórmula de Retención Viral para Facebook (Público de EE. UU.)

Para que los vídeos no se pierdan en el scroll de Facebook en los primeros 2 segundos, el generador de guiones implementa una estructura psicológica probada:

1. **El Gancho Disruptivo (0s a 3s - The Hook):**
   * Frases directas al subconsciente del creyente:  
     * *"Do not scroll past this video. Jesus saw you crying last night in secret..."*  
     * *"Stop scrolling for 20 seconds. God has an urgent message for the battle you are fighting alone."*
2. **El Mensaje / Oración (4s a 35s - The Heart Message):**
   * Enfocado en **dolores y necesidades reales**: batallas silenciosas, ansiedad, crisis económica, sanidad familiar y oración nocturna de paz.
3. **El Llamado a la Acción (36s a 45s - The Viral CTA):**
   * En Facebook, **los comentarios disparan la distribución viral**. El guion invita a una declaración de fe:  
     * *"If you receive this promise tonight, comment 'AMEN', share this with someone who needs God's peace, and follow for your daily prayer."*

---

## 🛠️ Tecnologías y Motores Gratuitos Integrados

| Componente | Motor | Características |
| :--- | :--- | :--- |
| **Generador de Guiones** | Motor interno (`engine/scripts.py`) | Categorizado por los 5 temas más virales en EE. UU. con hooks, cuerpos y llamados a la acción dinámicos. |
| **Voz en Inglés (TTS)** | **Edge-TTS** (Microsoft Neural Voices) | **100% gratis, sin API Key.** Voces solemnes y humanas como `en-US-ChristopherNeural` (ideal para Jesús) y `en-US-GuyNeural`. |
| **Imágenes de Jesús** | Galería 8K Bundled (`assets/images/`) | Retratos cinematográficos verticales 9:16 hiperrealistas con mirada compasiva. Permite subir imágenes propias. |
| **Subtítulos Dinámicos** | Motor ASS (`engine/subtitles.py`) | Tipografía **Impact**, bloques de 2-3 palabras, resalte en oro brillante (`#FFD700`) y borde negro grueso en zona segura de Facebook. |
| **Animación de Cámara** | **FFmpeg Ken Burns** (`engine/video.py`) | Zoom suave hacia el rostro de Jesús durante la narración para dar vida y dinamismo al vídeo. |

---

## 📁 Estructura del Proyecto

* **`server.py`**: Servidor FastAPI local que gestiona la API y sirve la interfaz web.
* **`engine/`**:
  * `scripts.py`: Banco y generador de guiones virales en inglés.
  * `tts.py`: Síntesis de voz y extracción de marcas temporales con Edge-TTS.
  * `subtitles.py`: Generador de subtítulos `.ass` con resaltado estilo CapCut/Hormozi.
  * `video.py`: Procesamiento de vídeo con FFmpeg, animación zoompan y quemado de subtítulos.
* **`static/`**:
  * `index.html`: Panel de control intuitivo con simulador de móvil vertical en 9:16.
  * `style.css`: Estilo visual oscuro y profesional.
  * `app.js`: Lógica interactiva (preescucha de audio, cambio de imagen, renderizado en 1 clic).
* **`assets/images/`**: Galería de retratos realistas de Jesús en 8K vertical.
* **`outputs/`**: Carpeta donde se guardan automáticamente los vídeos generados (`.mp4`) listos para descargar y subir a Facebook.

---

¡Listo para producir contenido viral de bendición con un solo clic!
