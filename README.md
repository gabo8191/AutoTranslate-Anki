# AutoTranslate-Anki

Add-on de [Anki](https://apps.ankiweb.net/) que **rellena automáticamente la traducción** de las notas de un mazo con un solo clic, usando el servicio **gratuito** de Google Translate (sin API key).

Pensado para quienes capturan vocabulario rápido (por ejemplo desde el móvil con AnkiDroid) escribiendo **solo el término en el idioma de origen**, y dejan que el PC complete la traducción después.

> Ejemplo de uso original: aprender inglés (B2→C1). Escribes solo el inglés en el campo `English`; al pulsar el botón, se rellena el campo `Español`. La pronunciación se resuelve aparte con la etiqueta nativa `{{tts en_US:English}}` en la plantilla.

---

## ✨ Características

- Botón en **Herramientas → "Rellenar traducciones – AutoTranslate"**.
- Barre un mazo concreto y traduce **solo las notas con el campo destino vacío**.
- Detección flexible de campos: `English → Español` o `Front → Back` (configurable).
- Idiomas configurables (cualquier par soportado por Google Translate).
- Se ejecuta en segundo plano con barra de progreso; no congela Anki.
- Gratis y sin cuenta: usa el endpoint público de Google Translate.

---

## ⚙️ Cómo funciona

1. Agregas notas a tu mazo escribiendo **solo el idioma de origen** (deja el campo destino vacío).
2. En el PC, con Anki abierto, pulsas el botón del menú *Herramientas*.
3. El add-on busca las notas del mazo, traduce las que tengan el destino vacío y las completa.
4. (Opcional) Sincronizas para que la traducción llegue a tus otros dispositivos.

> La traducción solo puede generarse en el escritorio: AnkiDroid/AnkiMobile no ejecutan add-ons. Por eso es un botón en el PC y no algo instantáneo en el móvil.

---

## 📦 Instalación

### Opción A — Desde el archivo `.ankiaddon` (recomendada)

1. Descarga `AutoTranslate-Anki.ankiaddon` desde la sección [Releases](https://github.com/gabo8191/AutoTranslate-Anki/releases) (o genéralo con `./build.sh`).
2. En Anki: **Herramientas → Complementos → Instalar desde archivo…** y selecciona el `.ankiaddon`.
3. Reinicia Anki.

### Opción B — Manual (copiando la carpeta)

1. En Anki: **Herramientas → Complementos → Ver archivos** para abrir la carpeta `addons21`.
2. Copia el contenido de `src/` dentro de una carpeta nueva, por ejemplo `addons21/autotranslate_anki/`.
3. Reinicia Anki.

---

## 🔧 Configuración

En **Herramientas → Complementos → AutoTranslate → Configuración**:

| Clave | Descripción | Por defecto |
|-------|-------------|-------------|
| `deck` | Mazo cuyas notas se revisan | `"Mi Vocabulario"` |
| `also_scan_notetype` | Tipo de nota extra a revisar (opcional) | `""` |
| `source_lang` | Idioma de origen (ISO) | `"en"` |
| `target_lang` | Idioma de destino (ISO) | `"es"` |
| `field_pairs` | Pares `[origen, destino]`; se usa el primero que exista | `[["English","Español"],["Front","Back"]]` |
| `menu_label` | Texto del botón | `"Rellenar traducciones – AutoTranslate"` |
| `request_delay_seconds` | Pausa entre peticiones | `0.3` |
| `overwrite_existing` | Retraducir aunque el destino tenga texto | `false` |

---

## 🗣️ Pronunciación automática (TTS) — sin complicaciones

**Aclaración importante:** este add-on **solo traduce**, no genera ni guarda audio. Pero no lo necesita: Anki ya trae una **lectura en voz alta automática** que funciona en escritorio **y** en AnkiDroid, gratis y sin archivos. Se activa con una etiqueta en la plantilla de la tarjeta.

### Cómo activarla (una sola vez)

1. Abre el **Explorador** (botón *Examinar*) → selecciona una tarjeta de tu mazo.
2. Pulsa **Tarjetas…** (editor de plantillas).
3. En la plantilla **Anverso** (Front), añade la etiqueta apuntando a tu campo de origen. Ejemplo para un campo llamado `English`:

   ```
   {{English}}
   {{tts en_US:English}}
   ```

   - `en_US` = inglés de EE. UU. Cámbialo según el idioma (`en_GB`, `es_ES`, `fr_FR`, …).
   - Reemplaza `English` por el nombre real de tu campo de origen.
4. Guarda. Listo: al mostrarse la tarjeta, el dispositivo **lee el texto en voz alta solo**, en el PC y en el móvil.

> Así tienes el combo completo y automático: **escribes solo el término → el botón rellena la traducción → la tarjeta se pronuncia sola**. Todo gratis y sin API keys.

### ¿Quieres un archivo de audio guardado en su lugar?

La etiqueta `{{tts}}` usa la voz del sistema (varía por dispositivo) y necesita ejecutarse en cada repaso. Si prefieres **guardar un MP3** con voz fija (offline, consistente), usa el add-on gratuito [HyperTTS](https://ankiweb.net/shared/info/111623432) con su servicio *Google Translate*. Eso sí: el audio solo se genera en el escritorio y pesa más. La etiqueta `{{tts}}` es lo más cómodo y ligero para la mayoría.

---

## ✅ Requisitos

- Anki de escritorio 2.1.50+ (probado en 25.09).
- Conexión a internet (para traducir).

---

## ⚠️ Limitaciones y privacidad

- Usa el endpoint **no oficial** de Google Translate (`translate.googleapis.com`). Es gratuito pero podría cambiar o limitar peticiones; por eso hay una pausa configurable entre llamadas.
- Al traducir, **el texto del campo de origen se envía a los servidores de Google**. No uses el add-on con datos sensibles.
- La calidad es la de Google Translate (muy buena para vocabulario y expresiones comunes; revisa matices).

---

## 🛠️ Desarrollo

Estructura del repo:

```
src/                 código del add-on (esto es lo que se empaqueta)
  __init__.py
  config.json        configuración por defecto
  config.md          ayuda mostrada en el editor de configuración
  manifest.json
build.sh             genera AutoTranslate-Anki.ankiaddon
```

Empaquetar:

```bash
./build.sh
```

Para desarrollar en vivo, enlaza `src/` dentro de tu carpeta `addons21/` y reinicia Anki tras cada cambio de código.

---

## 📄 Licencia

MIT © Gabriel Castillo ([@gabo8191](https://github.com/gabo8191))
