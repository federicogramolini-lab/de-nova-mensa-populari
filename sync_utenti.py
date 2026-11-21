"""Copia nella pagina di GitHub i menù e le liste della spesa salvati su claude.ai (account di Federico).
Uso: python3 sync_utenti.py index.html '<JSON del campo list del documento menus>' '<testo JSON del campo liste del documento spesa>'
I menù senza profilo sono di Federico. Aggiorna solo la riga SYNC_UTENTI e stampa CHANGED o UNCHANGED."""
import json, re, sys
path = sys.argv[1]
menus = json.loads(sys.argv[2] or "[]")
spesa = sys.argv[3] if len(sys.argv) > 3 else "{}"
spesa = json.loads(spesa or "{}")
if isinstance(spesa, str): spesa = json.loads(spesa or "{}")
for m in menus:
    if not m.get("profilo"): m["profilo"] = "federico"
new = {"menus": menus, "spesa": {k: v for k, v in spesa.items() if isinstance(v, list)}}
s = open(path, encoding="utf-8").read()
mm = re.search(r"/\*SYNCU\*/const SYNC_UTENTI = (.*?);/\*/SYNCU\*/", s)
if not mm: sys.exit("riga SYNC_UTENTI non trovata")
line = "/*SYNCU*/const SYNC_UTENTI = " + json.dumps(new, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/") + ";/*/SYNCU*/"
out = s[:mm.start()] + line + s[mm.end():]
if out == s: print("UNCHANGED")
else: open(path, "w", encoding="utf-8").write(out); print("CHANGED")
