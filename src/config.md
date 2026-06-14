## Configuración de AutoTranslate

- **deck**: nombre del mazo cuyas notas se revisarán (ej. `"Mi Vocabulario"`).
- **also_scan_notetype**: (opcional) nombre de un tipo de nota adicional a revisar, esté en el mazo que esté. Déjalo en `""` para ignorarlo.
- **source_lang**: código del idioma de origen (ISO, ej. `"en"`).
- **target_lang**: código del idioma de destino (ISO, ej. `"es"`).
- **field_pairs**: lista de pares `[campo_origen, campo_destino]`. Se usa el **primer** par que exista en la nota. Por defecto intenta `English → Español` y luego `Front → Back`.
- **menu_label**: texto del botón que aparece en el menú *Herramientas*.
- **request_delay_seconds**: pausa entre peticiones para no saturar el servicio.
- **overwrite_existing**: si es `true`, retraduce aunque el campo destino ya tenga texto. Por defecto `false` (solo rellena vacíos).
