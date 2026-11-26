"""Transcreve arquivos (pt-BR) com tempo por palavra (faster-whisper).
Uso: python3 -I transcrever.py saida.json arquivo1 [arquivo2 ...]  (modelo: env WHISPER_MODEL, padrão medium)"""
import sys, os, json, subprocess
import numpy as np
from faster_whisper import WhisperModel
out = sys.argv[1]; res = json.load(open(out)) if os.path.exists(out) else {}
m = WhisperModel(os.environ.get("WHISPER_MODEL", "medium"), device="cpu", compute_type="int8")
for f in sys.argv[2:]:
    k = os.path.basename(f)
    if k in res: continue
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"], capture_output=True, check=True).stdout
    audio = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
    segs, info = m.transcribe(audio, language="pt", word_timestamps=True, vad_filter=False, beam_size=5, initial_prompt=os.environ.get("WHISPER_PROMPT"))
    S = []
    for s in segs:
        S.append({"ini": round(s.start, 2), "fim": round(s.end, 2), "texto": s.text.strip(),
                  "palavras": [{"p": w.word.strip(), "ini": round(w.start, 2), "fim": round(w.end, 2), "prob": round(w.probability, 2)} for w in s.words]})
    res[k] = S; json.dump(res, open(out, "w"), ensure_ascii=False, indent=1)
    print(f"== {k}"); [print(f"  [{s['ini']:6.2f}-{s['fim']:6.2f}] {s['texto']}") for s in S]
