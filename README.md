# JesusReels Studio ✝️ v4.0.0
### Creador de Vídeos y Reels Cristianos de Alta Calidad para Facebook (Audiencia de EE. UU.)

Una aplicación completa, ligera y de código abierto (sin costes obligatorios de API ni límites artificiales) diseñada específicamente para crear Reels y vídeos verticales (1080x1920) con narrativa cuidada, calidad visual y respeto editorial para una audiencia de habla inglesa.

---

## Estudio editorial y seguimiento de publicaciones

El flujo editorial organiza el catálogo existente en dos series, permite comparar
tres aperturas y ofrece oración, reflexión bíblica y relato ilustrativo. Expone únicamente Guy, Christopher y Brian mediante Edge-TTS. Incluye revisión
de texto, una maqueta de los primeros tres segundos y un diario manual de resultados.

Consulta [estructura, límites, pruebas y activación](docs/EDITORIAL_WORKFLOW.md).

## Investigación y mejoras editoriales (octubre de 2026)

El motor local ofrece cuatro narraciones (oración, reflexión, relato ilustrativo y consuelo), rota ganchos y estructuras, y desarrolla tres escenas cristianas relacionadas con la narración. Cuando la voz tiene marcas temporales, las transiciones de imagen se alinean con ellas. Consulta la [estrategia, limitaciones y experimentos](docs/REELS_CONTENT_STRATEGY_2026.md).

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
| **Generador de Guiones** | Compositor local (`engine/narrative_composer.py`) | Categorizado en 5 pilares temáticos con ganchos, oraciones, CTAs y referencias bíblicas verificadas. |
| **Voz en Inglés (TTS)** | **Edge-TTS** (Microsoft Neural Voices) | Tres voces seleccionables: `en-US-GuyNeural`, `en-US-ChristopherNeural` y `en-US-BrianNeural`. |
| **Generador de Imágenes IA** | Motor Directo FLUX (`1080x1920`) | Generación en formato vertical 9:16 con iluminación cinematográfica y composición equilibrada. |
| **Galería de Imágenes** | Galería Bundled (`assets/images/`) | Retratos cinematográficos verticales 9:16 con mirada compasiva. Permite subir imágenes propias con validación estricta de formato y tamaño. |
| **Subtítulos Dinámicos** | Motor ASS (`engine/subtitles.py`) | Tipografía configurable (**Clean**, **Karaoke**, **Pop**, **Cinematic**), acotados a la duración exacta del audio y respetando la zona segura de Facebook. |
| **Renderizado de Video** | **FFmpeg Multi-core** (`engine/video.py`) | Composición a 30 FPS en 1080x1920 MP4, efectos visuales sutiles, mezcla de audio masterizada y exportación de métricas reales de duración. |

---

## 📁 Estructura del Proyecto

* **`server.py`**: Servidor FastAPI local/VPS que gestiona la API y sirve la interfaz web.
* **`engine/`**:
  * `scripts.py`: Catálogo de 26 temas estructurados en 5 pilares, citas bíblicas documentadas y generador de guiones.
  * `tts.py`: Síntesis de voz y extracción de marcas temporales con Edge-TTS.
  * `subtitles.py`: Generador de subtítulos `.ass` con estilos Clean, Karaoke, Pop y Cinematic.
  * `video.py`: Procesamiento de vídeo con FFmpeg, animación multicapa y mezcla de audio.
* **`static/`**:
  * `index.html`: Panel de control intuitivo con simulador de móvil vertical en 9:16.
  * `style.css`: Estilo visual oscuro y profesional adaptado a escritorio y móviles.
  * `app.js`: Lógica interactiva (creación de imágenes IA, preescucha, selección de temas sincronizada, renderizado).
* **`assets/images/`**: Galería de imágenes de alta definición vertical.
* **`assets/audio/`**: Pistas instrumentales de adoración (piano, cuerdas, acústico).
* **`outputs/`**: Carpeta donde se guardan automáticamente los vídeos generados (`.mp4`) listos para descargar y publicar.

---

¡Listo para producir contenido edificante, sincero y técnicamente cuidado para tu comunidad!

