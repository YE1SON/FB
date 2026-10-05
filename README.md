# JesusReels Studio ✝️ v4.0.0
### Creador de Vídeos y Reels Cristianos de Alta Retención para Facebook (Audiencia de EE. UU.)

Una aplicación completa, ligera y **100% gratuita** (sin costes de API, sin suscripciones y sin límites) diseñada específicamente para crear Reels y vídeos verticales (1080x1920) de alto impacto visual y emocional para una página de Facebook con público en Estados Unidos.

---

## 🚀 Despliegue y Ejecución

### 1. En Servidor en la Nube (Oracle Cloud Always Free VPS)
El servidor corre en segundo plano como servicio permanente de Linux con **Systemd** y **Nginx**:
```bash
# Estado del servicio
sudo systemctl status jesus-reels

# Reiniciar servicio tras actualizar código
sudo systemctl restart jesus-reels
```
Acceso web directo: `http://<IP_PUBLICA>`

### 2. En Local (Windows)
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
   * En Facebook, **los shares privados y comentarios de oración disparan la distribución viral**.
4. **Comentario Fijado Estratégico (Meta 2026 Boost):**
   * Cada video incluye una oración o pregunta estratégica lista para fijar en el primer comentario, multiplicando el engagement orgánico.

---

## 🛠️ Tecnologías Integradas

| Componente | Motor | Características |
| :--- | :--- | :--- |
| **Generador de Guiones** | Motor interno (`engine/scripts.py`) | Categorizado por los temas más virales en EE. UU. con ganchos, oraciones, CTAs y comentarios fijados. |
| **Voz en Inglés (TTS)** | **Edge-TTS** (Microsoft Neural Voices) | **100% gratis, sin API Key.** Voces solemnes y humanas como `en-US-ChristopherNeural` (Voz de Jesús) y `en-US-GuyNeural`. |
| **Generador de Imágenes IA** | Motor Directo FLUX (`1080x1920`) | Generación instantánea en formato vertical 9:16 sin coste ni límites, con iluminación cinematográfica y detalles hiperrealistas. |
| **Galería de Imágenes** | Galería Bundled (`assets/images/`) | Retratos cinematográficos verticales 9:16 con mirada compasiva. Permite subir imágenes propias. |
| **Subtítulos Dinámicos** | Motor ASS (`engine/subtitles.py`) | Tipografía **Impact**, bloques dinámicos, resalte en oro brillante (`#FFD700`) y zona segura de Facebook. |
| **Renderizado de Video** | **FFmpeg Multi-core** (`engine/video.py`) | Composición a 30 FPS, efectos visuales de partículas doradas/luz divina, música de adoración y renderizado en segundos. |

---

## 📁 Estructura del Proyecto

* **`server.py`**: Servidor FastAPI local/VPS que gestiona la API y sirve la interfaz web.
* **`engine/`**:
  * `scripts.py`: Banco y generador de guiones virales y comentarios fijados en inglés.
  * `tts.py`: Síntesis de voz y extracción de marcas temporales con Edge-TTS.
  * `subtitles.py`: Generador de subtítulos `.ass` con resaltado estilo CapCut/Hormozi.
  * `video.py`: Procesamiento de vídeo con FFmpeg, animación y efectos.
* **`static/`**:
  * `index.html`: Panel de control intuitivo con simulador de móvil vertical en 9:16.
  * `style.css`: Estilo visual oscuro y profesional.
  * `app.js`: Lógica interactiva (creación de imágenes IA, preescucha, selección de temas, renderizado).
* **`assets/images/`**: Galería de retratos de Jesús en alta definición vertical.
* **`assets/audio/`**: Pistas instrumentales de adoración (piano, cuerdas, acústico).
* **`outputs/`**: Carpeta donde se guardan automáticamente los vídeos generados (`.mp4`) listos para descargar y subir a Facebook.

---

¡Listo para producir contenido viral de bendición con un solo clic!
