import re, html, sys, time, urllib.request
from pathlib import Path
def bajar(nombre, url):
    try:
        r = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=60)
        b = r.read()
    except Exception as e:
        print(nombre, "ERROR", e); return
    if url.lower().endswith(".pdf") or b[:4] == b"%PDF":
        Path(nombre + ".pdf").write_bytes(b)
        import pypdf, io
        t = "\n".join(p.extract_text() or "" for p in pypdf.PdfReader(io.BytesIO(b)).pages)
    else:
        t = b.decode("utf-8", "replace")
        t = re.sub(r"<script.*?</script>|<style.*?</style>", "", t, flags=re.S)
        t = html.unescape(re.sub(r"<[^>]+>", " ", t)); t = re.sub(r"[ \t]+", " ", t); t = re.sub(r"\n\s*\n+", "\n", t)
    Path(nombre + ".txt").write_text(f"Fuente: {url}\nConsultada: 2026-10-07\n\n" + t)
    print(nombre, len(t))
for n, u in [l.split(" ", 1) for l in sys.argv[1:]]:
    bajar(n, u); time.sleep(1)
