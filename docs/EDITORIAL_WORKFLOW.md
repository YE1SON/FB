# Estudio editorial: estructura y alcance de la primera versión

## Flujo principal

1. **Idea y destinatario.** Selecciona una serie, un tema y un tipo de mensaje.
   Puedes escribir una situación y una idea en inglés. La interfaz del operador
   sigue en español; las entradas públicas deben revisarse en inglés estadounidense.
2. **Apertura.** Compara tres propuestas editables. Los temas tienen aperturas
   concretas y rotación local; una situación personalizada también produce tres
   alternativas. Son propuestas para experimentar, no predicciones de alcance.
3. **Guion.** Oración, reflexión bíblica y relato ilustrativo tienen estructuras
   diferentes. Los relatos locales se identifican como imaginados. La despedida
   es opcional. Un cierre en bucle no añade frases inconclusas.
4. **Voz.** Guy y Christopher aparecen primero; el control de opciones avanzadas
   permite acceder a todas las voces operativas. Se conserva la preescucha existente.
5. **Escenas.** Los prompts utilizan el texto de la narración, incluidos apertura,
   desarrollo y cierre, en vez de elegir solo una plantilla según el tema.
6. **Revisión.** Escucha una maqueta de los primeros tres segundos con la primera
   imagen seleccionada. No representa los subtítulos ni las transiciones del MP4.
   Revisa avisos concretos sobre idioma, repetición, cierre y duración estimada.
7. **Exportación.** Se mantiene el render existente. La duración objetivo se envía
   explícitamente al servidor; la duración real sigue dependiendo del audio y se
   inspecciona al exportar. No se acelera ni corta la voz para imponer un objetivo.
8. **Resultados.** En Exportar, registra manualmente observaciones a las 48 horas
   y los siete días. Son etiquetas de seguimiento, no recordatorios automáticos.

## Organización del catálogo

El catálogo conserva los 26 temas y los cinco pilares internos. Las dos series
son accesos editoriales, no categorías nuevas que eliminen contenido:

| Serie | Temas |
| --- | --- |
| Faith for Everyday Life | Hijos distanciados, padres ancianos, economía, matrimonio, crianza en solitario, nietos enfermos, empleo, incertidumbre médica, citas legales, trabajo, adicciones y decisiones. |
| A Quiet Moment with God | Inicio del día, ansiedad nocturna, descanso, duelo, paz familiar, soledad, depresión, gratitud, oración sin palabras, temor espiritual, perdón, cansancio, pruebas y gracia. |

El selector permite mostrar el catálogo completo. El idioma de sus etiquetas es
interno; los títulos automáticos para publicar se obtienen de un catálogo en inglés.

## Motor y límites editoriales

- Se conserva Ollama si está disponible, con destinatario y perspectiva en el prompt.
  Cuando no está disponible, la interfaz indica el respaldo de plantillas.
- El motor local tiene contenido finito; la rotación evita algunas repeticiones,
  pero no equivale a creatividad ilimitada ni a una revisión humana.
- Las citas siguen viniendo del catálogo existente. El revisor automático no
  autentica traducciones, testimonios ni exactitud teológica.
- Los guiones y resultados se revisan antes de publicar. La aplicación no cambia
  publicaciones de Facebook ni determina el país al que Meta distribuirá un Reel.
- Esta versión no añade subida de narración propia, integración automática con
  Meta, puntuaciones de viralidad ni cortes de escena alineados por frase.

## Registro de resultados

`data/editorial_results.json` conserva el guion, apertura seleccionada, serie,
formato, voz y motor junto a observaciones manuales. Al seleccionar una publicación
existente, se añade una observación sin reemplazar su guion original. Vacío se
guarda como `null`; un cero observado permanece como cero.

Se pueden registrar duración, vistas, tiempo medio visto, porcentaje medio visto,
seguidores atribuidos, compartidos, porcentaje de espectadores de EE. UU. y punto
de abandono. No se calcula retención dividiendo métricas de distinto alcance.
No se almacenan contraseñas ni tokens de Meta.

Este archivo no se sirve bajo `/outputs` y se excluye de Git. Guarda una copia
de seguridad de `data/` al actualizar o cambiar de servidor; en Docker debe estar
en un volumen persistente. La escritura atómica y el bloqueo cubren el proceso
único que utiliza el servidor actual; varios procesos requerirían una base de datos.

Las nuevas rutas comparten el modelo de acceso del servidor existente: no añaden
autenticación. El diario está pensado para el estudio de un operador. No introducir
datos personales de seguidores en los campos de contenido.

## Compatibilidad y comprobaciones

Las nuevas rutas tienen alias `/api/` y `/studio/api/`: `editorial-config`,
`editorial-review` y `editorial-results`. `generate-script` acepta opcionalmente
`brief`; las peticiones antiguas siguen funcionando. Se mantiene el catálogo
de voces de `/api/voices`. El render acepta una despedida vacía.

Pruebas locales sin llamadas a proveedores:

```bash
SCRIPT_PROVIDER=template python -m unittest discover -s tests -p test_editorial_workflow.py -v
SCRIPT_PROVIDER=template python .agents/skills/jesusreels-quality/scripts/validate_script_quality.py
python -m compileall -q engine server.py
node --check static/app.js
node --check static/editorial.js
```

El smoke test de interfaz necesita `jsdom` disponible en el entorno de pruebas:
`node tests/editorial_ui_smoke.cjs`. No es una dependencia de producción.

## Activación

Revisar y fusionar la propuesta de GitHub. Actualizar el checkout del servidor,
instalar sus requisitos y reiniciar el servicio `jesus-reels` según el README.
Este documento y la propuesta no implican que el servidor ya se haya actualizado.
