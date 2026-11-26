"""Analisa uma faixa: BPM, batidas, downbeats (tempos fortes estimados) e seções de energia.
Uso: python3 analisar_musica.py audio.(mp4|wav|mp3) saida.json"""
import sys, json, numpy as np, librosa
path, out = sys.argv[1], sys.argv[2]
y, sr = librosa.load(path, sr=22050, mono=True)
dur = len(y) / sr
tempo, beats = librosa.beat.beat_track(y=y, sr=sr, units='frames')
bt = librosa.frames_to_time(beats, sr=sr)
tempo = float(np.atleast_1d(tempo)[0])
onset = librosa.onset.onset_strength(y=y, sr=sr)
rms = librosa.feature.rms(y=y)[0]
rms_t = librosa.times_like(rms, sr=sr)
# downbeat: fase (0-3) cujo conjunto de batidas tem maior energia de onset
strength = onset[np.clip(beats, 0, len(onset)-1)]
phase = int(np.argmax([strength[p::4].mean() for p in range(4)]))
downbeats = bt[phase::4]
# energia por compasso (4 batidas) -> seções
bars = []
for i in range(phase, len(bt) - 4, 4):
    a, b = bt[i], bt[i + 4]
    m = (rms_t >= a) & (rms_t < b)
    bars.append({"t0": round(float(a), 3), "t1": round(float(b), 3), "rms": float(rms[m].mean())})
e = np.array([b["rms"] for b in bars]); en = (e - e.min()) / (np.ptp(e) + 1e-9)
for b, v in zip(bars, en): b["energia"] = round(float(v), 3)
# rótulos simples por nível de energia suavizado
sm = np.convolve(en, np.ones(4) / 4, mode='same')
lab = np.where(sm > 0.75, "clímax", np.where(sm > 0.45, "subida/alto", "baixo"))
secs = []
for b, l in zip(bars, lab):
    if secs and secs[-1]["tipo"] == l: secs[-1]["t1"] = b["t1"]
    else: secs.append({"tipo": str(l), "t0": b["t0"], "t1": b["t1"]})
json.dump({"arquivo": path, "duracao": round(dur, 3), "bpm": round(tempo, 2),
           "periodo_batida": round(60 / tempo, 4), "fase_downbeat": phase,
           "batidas": [round(float(t), 3) for t in bt],
           "downbeats": [round(float(t), 3) for t in downbeats],
           "compassos": bars, "secoes": secs}, open(out, "w"), ensure_ascii=False, indent=1)
print(f"dur={dur:.2f}s bpm={tempo:.2f} batidas={len(bt)} 1a batida={bt[0]:.3f} fase={phase}")
for s in secs: print(f"  {s['t0']:7.2f}-{s['t1']:7.2f} {s['tipo']}")
