"""Para cada proxy: métricas por segundo (nitidez=var. do Laplaciano, exposição=brilho médio,
tremor=deslocamento global entre quadros por phaseCorrelate, movimento) + cortes de cena (PySceneDetect)
+ folha de contato com timecode. Uso: python3 analisar_clipes.py pasta_proxies pasta_saida"""
import sys, os, json, glob, subprocess, cv2, numpy as np
src, out = sys.argv[1], sys.argv[2]
os.makedirs(f"{out}/folhas", exist_ok=True)
res = json.load(open(f"{out}/metricas.json")) if os.path.exists(f"{out}/metricas.json") else {}
for p in sorted(glob.glob(f"{src}/*.mp4")):
    name = os.path.basename(p)[:-4]
    if name in res: continue
    cap = cv2.VideoCapture(p); fps = cap.get(cv2.CAP_PROP_FPS); n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    step = max(1, round(fps / 6)); prev = None; per = {}
    for i in range(0, n, step):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i); ok, fr = cap.read()
        if not ok: break
        g = cv2.cvtColor(cv2.resize(fr, (320, 180)), cv2.COLOR_BGR2GRAY).astype(np.float32)
        # nitidez medida no terço central (onde fica o recorte vertical)
        c = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)[:, fr.shape[1]//2 - fr.shape[0]*9//32: fr.shape[1]//2 + fr.shape[0]*9//32]
        sharp = float(cv2.Laplacian(c, cv2.CV_64F).var())
        shake = 0.0; motion = 0.0
        if prev is not None:
            (dx, dy), _ = cv2.phaseCorrelate(prev, g); shake = float(np.hypot(dx, dy)) / step
            motion = float(np.abs(g - prev).mean()) / step
        prev = g
        s = int(i / fps); d = per.setdefault(s, {"sharp": [], "bright": [], "shake": [], "motion": []})
        d["sharp"].append(sharp); d["bright"].append(float(g.mean())); d["shake"].append(shake); d["motion"].append(motion)
    cap.release()
    secs = [{"t": s, **{k: round(float(np.mean(v)), 2) for k, v in d.items()}} for s, d in sorted(per.items())]
    # cenas
    try:
        from scenedetect import detect, AdaptiveDetector
        sc = [(round(a.get_seconds(), 2), round(b.get_seconds(), 2)) for a, b in detect(p, AdaptiveDetector())]
    except Exception as e:
        sc = []
    dur = n / fps
    res[name] = {"fps": fps, "duracao": round(dur, 3), "segundos": secs, "cenas": sc}
    # folha de contato: até 12 quadros, com timecode
    k = min(12, max(4, int(dur // 1.5))); ts = [dur * (j + 0.5) / k for j in range(k)]
    sel = "+".join(f"eq(n\\,{int(t*fps)})" for t in ts)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", p, "-vf",
        f"select='{sel}',scale=320:-1,drawtext=text='{name} %{{pts\\:hms}}':x=4:y=4:fontsize=16:fontcolor=yellow:box=1:boxcolor=black@0.6,tile=4x3",
        "-vsync", "0", "-frames:v", "1", f"{out}/folhas/{name}.jpg"], check=False)
    json.dump(res, open(f"{out}/metricas.json", "w"))
    print(name, round(dur, 1), "s", len(sc), "cenas", flush=True)
