"""Transcreve a prévia plano a plano e mostra a 1ª/última palavra de cada um (confere cortes de fala).
Uso: HF_HUB_DISABLE_XET=1 python3 -I verificar_falas.py plano.json preview.mp4"""
import sys, json, subprocess, numpy as np
from faster_whisper import WhisperModel
P = json.load(open(sys.argv[1])); prev = sys.argv[2]; FPS = P["sequencia"]["fps"]
m = WhisperModel("medium", device="cpu", compute_type="int8")
for p in P["planos"]:
    a = p["timeline_in_f"] / FPS; d = (p["timeline_out_f"] - p["timeline_in_f"]) / FPS
    b = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{a:.3f}", "-t", f"{d:.3f}", "-i", prev, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
                       capture_output=True).stdout
    y = np.frombuffer(b, np.int16).astype(np.float32) / 32768
    segs, _ = m.transcribe(y, language="pt", initial_prompt="Quintão, T.T., chopp, Mabros, hambúrguer")
    txt = " ".join(s.text.strip() for s in segs)
    print(f"#{p['n']} {p['clipe']} {p['timeline_in_tc']}: {txt}")
    print(f"     esperado: {p['texto']}")
