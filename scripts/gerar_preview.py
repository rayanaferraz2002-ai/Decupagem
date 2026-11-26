"""Renderiza preview.mp4 a partir do plano.json (ffmpeg), usando os proxies 720p.

Uso: python3 -I gerar_preview.py plano.json pasta_proxies musica.(mp4|wav) saida.mp4
Aplica: rotação por clipe, 720x1280 @ 30 fps, cortes nas batidas, fusões (dissolve) marcadas,
fade para preto no fim e fade-out da música.
"""
import json, os, subprocess, sys, tempfile

plano_p, prox, musica, saida = sys.argv[1:5]
P = json.load(open(plano_p)); S = P["sequencia"]; FPS = S["fps"]; W, H = S["largura"], S["altura"]
D = P["dissolve_f"]; h = D // 2
tmp = tempfile.mkdtemp(prefix="prev_")
planos = P["planos"]


def seg(p, extra_pre=0, extra_post=0, idx=0):
    """renderiza um plano (com sobras para fusão) em arquivo intermediário com nº exato de quadros"""
    nf = p["timeline_out_f"] - p["timeline_in_f"] + extra_pre + extra_post
    ss = p["in_s"] - extra_pre / FPS
    tr = "transpose=1" if p["rotacao"] == "cw" else "transpose=2"
    o = os.path.join(tmp, f"s{idx:02d}.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{ss:.4f}", "-i", os.path.join(prox, p["clipe"] + ".mp4"),
                    "-an", "-vf", f"{tr},scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},setsar=1",
                    "-frames:v", str(nf), "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", o],
                   check=True)
    return o, nf


# grupos separados nas fusões
grupos, atual = [], []
for i, p in enumerate(planos):
    if p["transicao_entrada"] == "dissolve" and atual:
        grupos.append(atual); atual = []
    atual.append(i)
grupos.append(atual)

arquivos = []
for gi, g in enumerate(grupos):
    lst = os.path.join(tmp, f"g{gi}.txt"); total = 0
    with open(lst, "w") as f:
        for k, i in enumerate(g):
            pre = h if (k == 0 and gi > 0) else 0
            post = h if (k == len(g) - 1 and gi < len(grupos) - 1) else 0
            o, nf = seg(planos[i], pre, post, i); total += nf
            f.write(f"file '{o}'\n")
    go = os.path.join(tmp, f"g{gi}.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", go], check=True)
    arquivos.append((go, total))

# encadeia grupos com xfade
inputs = sum([["-i", a] for a, _ in arquivos], [])
fc, last, acc = [], "[0:v]", arquivos[0][1]
for k in range(1, len(arquivos)):
    off = (acc - D) / FPS
    fc.append(f"{last}[{k}:v]xfade=transition=fade:duration={D / FPS:.4f}:offset={off:.4f}[x{k}]")
    last = f"[x{k}]"; acc = acc + arquivos[k][1] - D
total_s = S["duracao_f"] / FPS
fv = P["fade_video_f"] / FPS
fc.append(f"{last}trim=end_frame={S['duracao_f']},fade=t=out:st={total_s - fv:.4f}:d={fv:.4f}[v]")
M = P["musica"]; na = len(arquivos)
fc.append(f"[{na}:a]atrim=start={M['in_s']}:duration={total_s:.4f},asetpts=PTS-STARTPTS,"
          f"afade=t=out:st={total_s - M['fade_out_s']:.4f}:d={M['fade_out_s']}[a]")
subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-i", musica, "-filter_complex", ";".join(fc),
                "-map", "[v]", "-map", "[a]", "-r", str(FPS), "-c:v", "libx264", "-preset", "medium", "-crf", "23",
                "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", saida], check=True)
print("ok", saida)
