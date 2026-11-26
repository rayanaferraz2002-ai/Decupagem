"""Indicadores objetivos de empolgação por depoimento, só no trecho da resposta.
Uso: python3 -I medir_empolgacao.py transcricoes.json pasta_clipes saida.json"""
import sys, json, subprocess, numpy as np, librosa, cv2
tr = json.load(open(sys.argv[1])); pasta = sys.argv[2]; res = {}
for k, segs in tr.items():
    ws = [w for s in segs for w in s["palavras"]]
    # resposta = a partir de "minha/melhor parte"; ignora conversa antes
    i0 = next((i for i, w in enumerate(ws) if w["p"].lower().strip(",.") in ("minha", "melhor", "a") and i + 1 < len(ws)
               and ws[i + 1]["p"].lower().strip(",.") in ("parte", "minha", "melhor")), 0)
    ws = ws[i0:]; a, b = ws[0]["ini"], ws[-1]["fim"]
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(a), "-t", str(b - a), "-i", f"{pasta}/{k}", "-ac", "1", "-ar", "16000",
                          "-f", "s16le", "-"], capture_output=True).stdout
    y = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768; sr = 16000
    rms = librosa.feature.rms(y=y)[0]; db = 20 * np.log10(rms[rms > rms.max() * 0.1] + 1e-9)
    f0 = librosa.yin(y, fmin=80, fmax=500, sr=sr); f0 = f0[(f0 > 80) & (f0 < 500)]
    st = 12 * np.log2(f0 / np.median(f0))  # semitons
    cap = cv2.VideoCapture(f"{pasta}/{k}"); fps = cap.get(cv2.CAP_PROP_FPS); prev = None; mov = []
    for t in np.arange(a, b, 0.25):
        cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000); ok, fr = cap.read()
        if not ok: break
        g = cv2.cvtColor(cv2.resize(fr, (320, 180)), cv2.COLOR_BGR2GRAY).astype(np.float32)
        if prev is not None: mov.append(np.abs(g - prev).mean())
        prev = g
    res[k] = {"resposta_ini": a, "resposta_fim": b, "dur": round(b - a, 2), "volume_db": round(float(np.median(db)), 1),
              "variacao_tom_st": round(float(np.std(st)), 2), "palavras_s": round(len(ws) / (b - a), 2),
              "movimento": round(float(np.mean(mov)), 2), "texto": " ".join(w["p"] for w in ws)}
# escore: média dos z-scores (volume, variação de tom, velocidade, movimento)
ks = list(res); M = np.array([[res[k][c] for c in ("volume_db", "variacao_tom_st", "palavras_s", "movimento")] for k in ks])
Z = (M - M.mean(0)) / (M.std(0) + 1e-9)
for k, z in zip(ks, Z.mean(1)): res[k]["escore_empolgacao"] = round(float(z), 2)
json.dump(res, open(sys.argv[3], "w"), ensure_ascii=False, indent=1)
for k in sorted(ks, key=lambda k: -res[k]["escore_empolgacao"]):
    r = res[k]; print(k, r["escore_empolgacao"], r["volume_db"], r["variacao_tom_st"], r["palavras_s"], r["movimento"], r["dur"])
