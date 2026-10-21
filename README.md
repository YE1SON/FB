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

## 🧭 Guía práctica de calidad para publicar

La aplicación ayuda a preparar guiones, audio, escenas y subtítulos; no puede garantizar alcance, retención ni viralidad. Antes de publicar cada Reel:

1. **Gancho claro:** empieza con una necesidad humana concreta, sin prometer milagros inmediatos ni afirmar que el video contiene un mensaje personal de Dios para cada espectador.
2. **Mensaje centrado:** desarrolla una idea principal y una oración natural; evita repetir la misma petición o llamada a la acción.
3. **Referencia bíblica:** revisa la cita y la traducción que quieres usar antes de publicar. La referencia automatizada debe tratarse como un punto de partida, no como una verificación editorial.
4. **Llamada a la acción natural:** invita a guardar o compartir cuando tenga sentido para la persona. No hay una frase que garantice distribución en Facebook.
5. **Control de calidad:** escucha la voz con la música, comprueba que el texto se lea en pantalla y revisa la duración y sincronización del MP4 exportado.

Los 26 temas están organizados en cinco pilares para facilitar la selección y reducir la sensación de repetición. La calidad final depende de revisar cada guion y cada video antes de publicarlo.

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
