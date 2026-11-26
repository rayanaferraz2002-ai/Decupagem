"""Folhas de contato com rotação aplicada (padrão transpose=1, 90° horário), 6 quadros por clipe,
4 clipes por imagem. Uso: python3 folhas_verticais.py pasta_proxies metricas.json pasta_saida [transpose]"""
import sys, os, json, subprocess
src, met, out = sys.argv[1], sys.argv[2], sys.argv[3]; tr = sys.argv[4] if len(sys.argv) > 4 else "1"
os.makedirs(out, exist_ok=True); m = json.load(open(met)); names = sorted(m)
rows = []
for n in names:
    d = m[n]["duracao"]; fps = m[n]["fps"]; ts = [d * (j + .5) / 6 for j in range(6)]
    sel = "+".join(f"eq(n\\,{int(t*fps)})" for t in ts); o = f"{out}/{n}.jpg"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{src}/{n}.mp4", "-vf",
        f"select='{sel}',transpose={tr},scale=180:320,drawtext=text='{n} %{{pts\\:hms}}':x=3:y=3:fontsize=14:fontcolor=yellow:box=1:boxcolor=black@0.6,tile=6x1",
        "-vsync", "0", "-frames:v", "1", o], check=True)
    rows.append(o)
for i in range(0, len(rows), 4):
    g = rows[i:i+4]; args = sum([["-i", x] for x in g], [])
    subprocess.run(["ffmpeg", "-v", "error", "-y", *args, "-filter_complex", f"vstack=inputs={len(g)}" if len(g) > 1 else "null", "-q:v", "4", f"{out}/grupo_{i//4:02d}.jpg"], check=True)
print(len(rows), "clipes")
