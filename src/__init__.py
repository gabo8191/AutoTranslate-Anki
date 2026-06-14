# AutoTranslate-Anki
# Add-on de Anki que rellena automáticamente la traducción de las notas de un
# mazo concreto mediante un botón en el menú Herramientas.
#
# La traducción usa el endpoint público (no oficial) de Google Translate, que es
# gratuito y NO requiere API key. El texto del campo de origen se envía a
# translate.googleapis.com para obtener la traducción.

import json
import re
import time
import urllib.parse
import urllib.request

from aqt import gui_hooks, mw
from aqt.operations import QueryOp
from aqt.qt import QAction
from aqt.utils import tooltip

GTX_URL = "https://translate.googleapis.com/translate_a/single"

# Configuración por defecto (se sobreescribe con config.json del add-on).
DEFAULTS = {
    "deck": "Mi Vocabulario",
    "also_scan_notetype": "",
    "source_lang": "en",
    "target_lang": "es",
    "field_pairs": [["English", "Español"], ["Front", "Back"]],
    "menu_label": "Rellenar traducciones – AutoTranslate",
    "request_delay_seconds": 0.3,
    "overwrite_existing": False,
}


def get_config() -> dict:
    """Carga la config del add-on fusionada con los valores por defecto."""
    cfg = dict(DEFAULTS)
    user = mw.addonManager.getConfig(__name__) or {}
    cfg.update({k: v for k, v in user.items() if v is not None})
    return cfg


def _plain(text: str) -> str:
    """Quita etiquetas HTML y referencias [sound:...] del campo."""
    text = re.sub(r"\[sound:[^\]]*\]", "", text)
    text = re.sub(r"<[^>]+>", " ", text)
    return text.strip()


def translate(text: str, source_lang: str, target_lang: str) -> str:
    """Traduce texto vía el endpoint gratuito de Google (sin API key)."""
    params = urllib.parse.urlencode(
        {"client": "gtx", "sl": source_lang, "tl": target_lang, "dt": "t", "q": text}
    )
    req = urllib.request.Request(
        f"{GTX_URL}?{params}", headers={"User-Agent": "Mozilla/5.0"}
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    # data[0] es una lista de segmentos; cada segmento[0] es el texto traducido.
    return "".join(seg[0] for seg in data[0] if seg and seg[0]).strip()


def _pick_fields(note, field_pairs):
    """Devuelve el primer par (origen, destino) presente en la nota."""
    names = note.keys()
    for pair in field_pairs:
        src, dst = pair[0], pair[1]
        if src in names and dst in names:
            return src, dst
    return None, None


def _collect_note_ids(col, cfg):
    nids = set()
    if cfg["deck"]:
        nids |= set(col.find_notes(f'deck:"{cfg["deck"]}"'))
    if cfg["also_scan_notetype"]:
        nids |= set(col.find_notes(f'note:"{cfg["also_scan_notetype"]}"'))
    return nids


def _fill_translations(col, cfg):
    nids = _collect_note_ids(col, cfg)
    to_update = []
    errors = 0
    for nid in nids:
        note = col.get_note(nid)
        src, dst = _pick_fields(note, cfg["field_pairs"])
        if not src:
            continue
        source = _plain(note[src])
        if not source:
            continue
        if note[dst].strip() and not cfg["overwrite_existing"]:
            continue
        try:
            result = translate(source, cfg["source_lang"], cfg["target_lang"])
            if result:
                note[dst] = result
                to_update.append(note)
            time.sleep(cfg["request_delay_seconds"])
        except Exception:
            errors += 1
    if to_update:
        col.update_notes(to_update)
    return {"updated": len(to_update), "errors": errors, "scanned": len(nids)}


def _on_done(result):
    msg = (
        f"AutoTranslate: {result['updated']} traducciones añadidas "
        f"de {result['scanned']} notas revisadas."
    )
    if result["errors"]:
        msg += f"\n{result['errors']} fallaron (revisa tu conexión a internet)."
    if result["updated"]:
        mw.reset()
    tooltip(msg, period=4000)


def run_fill():
    if mw.col is None:
        return
    cfg = get_config()
    QueryOp(
        parent=mw, op=lambda col: _fill_translations(col, cfg), success=_on_done
    ).with_progress("Traduciendo…").run_in_background()


def _add_menu():
    cfg = get_config()
    action = QAction(cfg["menu_label"], mw)
    action.triggered.connect(run_fill)
    mw.form.menuTools.addAction(action)


gui_hooks.main_window_did_init.append(_add_menu)
