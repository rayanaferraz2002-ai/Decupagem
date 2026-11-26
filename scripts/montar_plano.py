"""Gera plano.json: cada plano do escolhas.json vira um evento na timeline com corte na batida.

Uso:
  python3 -I montar_plano.py --escolhas dados/escolhas.json --orientacao dados/orientacao.json \
      --musica-json work/musica.json --proxies work/proxies --originais material/evento \
      --saida plano.json [--fixar plano_antigo.json]

--fixar: reaproveita entradas (in) já escolhidas num plano anterior para clipes que não mudaram,
  assim uma troca pontual não mexe no resto.
Para trocar um plano: edite o clipe/janela em escolhas.json (ou o campo "in_s" direto no plano.json
  e rode gerar_preview.py / gerar_xml.py, que leem só o plano.json).
"""
import argparse, json, os, subprocess
import cv2, numpy as np

SEQ_FPS = 30  # referência: 720x1280 @ 30 fps
ap = argparse.ArgumentParser()
for a in ["escolhas", "orientacao", "musica-json", "proxies", "originais", "saida"]:
    ap.add_argument("--" + a, required=True)
ap.add_argument("--fixar")
A = ap.parse_args()

esc = json.load(open(A.escolhas)); ori = json.load(open(A.orientacao)); mus = json.load(open(A.musica_json))
rot = {c: "cw" for c in ori["cw"]} | {c: "ccw" for c in ori["ccw"]}
fix = {}
if A.fixar and os.path.exists(A.fixar):
    for p in json.load(open(A.fixar))["planos"]:
        fix[(p["clipe"], tuple(p["janela"]), p["batidas"])] = p["in_s"]

m0 = esc["musica"]["inicio"]; nb = esc["musica"]["batidas"]
beats = [t for t in mus["batidas"] if t >= m0 - 0.02][: nb + 1]  # nb+1 marcas = nb intervalos
assert len(beats) == nb + 1, "música curta para o nº de batidas"
beat_frames = [round((t - m0) * SEQ_FPS) for t in beats]  # corte = batida mais próxima, em quadros de 30 fps
beat_frames[0] = 0


def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=width,height,r_frame_rate,nb_frames:format=duration", "-of", "json", path],
                         capture_output=True, text=True).stdout
    j = json.loads(out); s = j["streams"][0]; n, d = map(int, s["r_frame_rate"].split("/"))
    return {"w": s["width"], "h": s["height"], "fps_num": n, "fps_den": d, "dur": float(j["format"]["duration"])}


def metricas_finas(proxy, a, b):
    """amostra 8 quadros/s entre a e b: nitidez (Laplaciano no quadro endireitado), tremor (phaseCorrelate), brilho"""
    cap = cv2.VideoCapture(proxy); fps = cap.get(cv2.CAP_PROP_FPS)
    ts, sh, sk, br = [], [], [], []; prev = None; t = a
    while t <= b:
        cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000); ok, fr = cap.read()
        if not ok: break
        g = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
        small = cv2.resize(g, (320, 180)).astype(np.float32)
        ts.append(t); sh.append(cv2.Laplacian(g, cv2.CV_64F).var()); br.append(small.mean())
        sk.append(0.0 if prev is None else float(np.hypot(*cv2.phaseCorrelate(prev, small)[0])))
        prev = small; t += 1 / 8
    cap.release()
    return np.array(ts), np.array(sh), np.array(sk), np.array(br)


planos = []; i_beat = 0; n = 0
for bl in esc["blocos"]:
    for p in bl["planos"]:
        n += 1
        c = p["clipe"]; orig = os.path.join(A.originais, c + ".MP4"); info = probe(orig)
        f0, f1 = beat_frames[i_beat], beat_frames[i_beat + p["batidas"]]; i_beat += p["batidas"]
        dur_s = (f1 - f0) / SEQ_FPS
        handle = 0.2  # sobra para fusões
        a = max(p["janela"][0], handle); b = min(p["janela"][1], info["dur"] - handle) - dur_s
        key = (c, tuple(p["janela"]), p["batidas"])
        if key in fix:
            ins = fix[key]; nota = "fixado do plano anterior"
        elif b <= a:
            ins = max(0.0, min(p["janela"][0], info["dur"] - dur_s)); nota = "janela justa: usado o início da janela"
        else:
            ts, sh, sk, br = metricas_finas(os.path.join(A.proxies, c + ".mp4"), a, b + dur_s)
            best, ins = -1e9, a
            for s0 in np.arange(a, b + 1e-6, 1 / 8):
                m = (ts >= s0) & (ts <= s0 + dur_s)
                if m.sum() < 2: continue
                score = np.log1p(sh[m]).mean() - 0.35 * sk[m].mean() - 0.02 * abs(br[m].mean() - 70)
                if score > best: best, ins = score, float(s0)
            nota = "melhor trecho por nitidez/tremor/exposição"
        src_fps = info["fps_num"] / info["fps_den"]
        planos.append({
            "n": n, "bloco": bl["bloco"], "nome_bloco": bl["nome"], "clipe": c, "arquivo": c + ".MP4",
            "janela": p["janela"], "batidas": p["batidas"],
            "timeline_in_f": f0, "timeline_out_f": f1,
            "timeline_in_tc": f"00:{f0 // SEQ_FPS // 60:02d}:{f0 // SEQ_FPS % 60:02d}:{f0 % SEQ_FPS:02d}",
            "in_s": round(ins, 3), "out_s": round(ins + dur_s, 3),
            "in_src_f": round(ins * src_fps), "out_src_f": round((ins + dur_s) * src_fps),
            "rotacao": rot[c], "transicao_entrada": p.get("transicao_entrada", "corte"),
            "fade_out": p.get("fade_out", False), "motivo": p["motivo"], "nota_escolha": nota,
            "src": {"largura": info["w"], "altura": info["h"], "fps": f"{info['fps_num']}/{info['fps_den']}", "duracao": info["dur"]},
        })
        print(f"{n:2d} {planos[-1]['timeline_in_tc']} {c} {rot[c]:3s} in={ins:6.2f}s dur={dur_s:.2f}s {nota}")

total_f = beat_frames[nb]
plano = {
    "sequencia": {"largura": 720, "altura": 1280, "fps": SEQ_FPS, "duracao_f": total_f,
                  "duracao_s": round(total_f / SEQ_FPS, 3), "fonte": "configuração do vídeo de referência"},
    "musica": {"arquivo": esc["musica"]["arquivo"], "in_s": m0, "out_s": round(m0 + total_f / SEQ_FPS, 3),
               "fade_out_s": esc["musica"]["fade_out_s"], "bpm": round(60 / np.diff(beats).mean(), 2)},
    "dissolve_f": 8, "fade_video_f": 24,
    "planos": planos,
}
json.dump(plano, open(A.saida, "w"), ensure_ascii=False, indent=1)
print("total", plano["sequencia"]["duracao_s"], "s")
