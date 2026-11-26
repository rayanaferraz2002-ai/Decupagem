"""Renderiza preview.mp4 a partir do plano.json (ffmpeg), direto dos originais (cópia; originais não mudam).

Uso: python3 -I gerar_preview.py plano.json pasta_originais musica.mp4 saida.mp4
Aplica: rotação, 720x1280 @ 30 fps, zoom-in lento nos planos marcados, fala de cada clipe com ganho
para igualar volume (micro-fade de 15 ms nas bordas), música baixa sob a fala com fade-out, fade p/ preto.
"""
import json, os, subprocess, sys, tempfile

plano_p, orig, musica, saida = sys.argv[1:5]
P = json.load(open(plano_p)); S = P["sequencia"]; FPS = S["fps"]; W, H = S["largura"], S["altura"]
tmp = tempfile.mkdtemp(prefix="prevdep_"); lista = []
for p in P["planos"]:
    nf = p["timeline_out_f"] - p["timeline_in_f"]; d = nf / FPS
    tr = "transpose=1" if p["rotacao"] == "cw" else "transpose=2"
    z = p["zoom_fim"] - 1
    # zoom: escala cresce linearmente de 100% a zoom_fim ao longo do plano, recorte central
    sc = (f"scale=w='trunc({W}*(1+{z}*t/{d:.4f})/2)*2':h='trunc({H}*(1+{z}*t/{d:.4f})/2)*2':eval=frame,crop={W}:{H}"
          if z > 0 else f"scale={W}:{H}")
    o = os.path.join(tmp, f"{p['n']:02d}.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{p['in_s']:.3f}", "-t", f"{d + 0.2:.3f}", "-i", os.path.join(orig, p["arquivo"]),
                    "-vf", f"{tr},{sc},fps={FPS},setsar=1,setpts=PTS-STARTPTS", "-frames:v", str(nf),
                    "-af", f"volume={p['ganho_fala_db']}dB,atrim=0:{d:.4f},afade=t=in:d=0.015,afade=t=out:st={d - 0.015:.4f}:d=0.015,"
                           f"aresample=48000,aformat=channel_layouts=stereo",
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "pcm_s16le", o + ".mov"],
                   check=True)
    lista.append(o + ".mov")
txt = os.path.join(tmp, "l.txt"); open(txt, "w").write("".join(f"file '{x}'\n" for x in lista))
total = S["duracao_f"] / FPS; M = P["musica"]; fv = P["fade_video_f"] / FPS
# ducking: durante cada fala a música desce (volume_fala_db - volume_livre_db), com rampas de 0,15 s
g = 10 ** ((M["volume_fala_db"] - M["volume_livre_db"]) / 20); r = 0.15
fala = "+".join(f"clip(min((t-{a / FPS - r:.3f})/{r},({b / FPS + r:.3f}-t)/{r}),0,1)" for a, b in M["falas_f"])
duck = f"1-(1-{g:.4f})*min(1,{fala})"
fc = (f"[0:v]trim=end_frame={S['duracao_f']},fade=t=out:st={total - fv:.4f}:d={fv:.4f}[v];"
      f"[1:a]atrim=start={M['in_s']}:duration={total:.4f},asetpts=PTS-STARTPTS,volume={M['volume_livre_db']}dB,"
      f"volume='{duck}':eval=frame,"
      f"afade=t=out:st={total - M['fade_out_s']:.4f}:d={M['fade_out_s']},aresample=48000[m];"
      f"[0:a]atrim=duration={total:.4f}[f];[f][m]amix=inputs=2:normalize=0:duration=first[a]")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", txt, "-i", musica, "-filter_complex", fc,
                "-map", "[v]", "-map", "[a]", "-r", str(FPS), "-c:v", "libx264", "-preset", "medium", "-crf", "22",
                "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", saida], check=True)
print("ok", saida)
