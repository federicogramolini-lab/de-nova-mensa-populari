"""Aggiorna in index.html la riga SYNC_DATA con i nomi cambiati e le ricette eliminate su claude.ai.
Uso: python3 sync.py index.html '<json titoli {id: nome}>' '<json cestino [id, ...]>'
I nomi si accumulano (quelli già presenti restano se non vengono sostituiti); il cestino viene sostituito.
Stampa CHANGED se il file è cambiato, altrimenti UNCHANGED."""
import json, re, sys
path, titoli, cestino = sys.argv[1], json.loads(sys.argv[2] or "{}"), json.loads(sys.argv[3] or "[]")
s = open(path, encoding="utf-8").read()
m = re.search(r"/\*SYNC\*/const SYNC_DATA = (.*?);/\*/SYNC\*/", s)
if not m: sys.exit("riga SYNC_DATA non trovata")
old = json.loads(m.group(1))
new = {"titoli": {**old.get("titoli", {}), **{k: v for k, v in titoli.items() if isinstance(v, str) and v.strip()}},
       "cestino": sorted(set(c for c in cestino if isinstance(c, str)))}
line = "/*SYNC*/const SYNC_DATA = " + json.dumps(new, ensure_ascii=False, separators=(",", ":")) + ";/*/SYNC*/"
out = s[:m.start()] + line + s[m.end():]
if out == s: print("UNCHANGED")
else: open(path, "w", encoding="utf-8").write(out); print("CHANGED")
