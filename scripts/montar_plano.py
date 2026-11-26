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
        if p.get("faixa"):
            if "continuação" not in p["nota_escolha"]:
                fix[(p["clipe"], tuple(p["janela"]), p["faixa"])] = p["in_s"]
        elif "[tela cheia]" in p["motivo"]:
            fix[(p["clipe"], tuple(p["janela"]), "cheio")] = p["in_s"]
        else:
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


FAIXAS = {"topo": (0.0, 1 / 3), "meio": (1 / 3, 2 / 3), "base": (2 / 3, 1.0)}
CAMADA = {"meio": "V1", "topo": "V2", "base": "V3"}


def tc(f):
    return f"00:{f // SEQ_FPS // 60:02d}:{f // SEQ_FPS % 60:02d}:{f % SEQ_FPS:02d}"


def escolher(c, janela, dur_s, key, info):
    """melhor início dentro da janela (nitidez alta, pouco tremor, exposição ~70/255)"""
    handle = 0.2  # sobra para fusões
    a = max(janela[0], handle); b = min(janela[1], info["dur"] - handle) - dur_s
    if key in fix:
        return fix[key], "fixado do plano anterior"
    if b <= a:
        return max(0.0, min(janela[0], info["dur"] - dur_s)), "janela justa: usado o início da janela"
    ts, sh, sk, br = metricas_finas(os.path.join(A.proxies, c + ".mp4"), a, b + dur_s)
    best, ins = -1e9, a
    for s0 in np.arange(a, b + 1e-6, 1 / 8):
        m = (ts >= s0) & (ts <= s0 + dur_s)
        if m.sum() < 2: continue
        score = np.log1p(sh[m]).mean() - 0.35 * sk[m].mean() - 0.02 * abs(br[m].mean() - 70)
        if score > best: best, ins = score, float(s0)
    return ins, "melhor trecho por nitidez/tremor/exposição"


planos = []


def add(bl, c, janela, nbat, f0, f1, ins, nota, info, motivo, camada="V1", faixa=None, trans="corte", fade=False):
    dur_s = (f1 - f0) / SEQ_FPS; src_fps = info["fps_num"] / info["fps_den"]
    if ins + dur_s > info["dur"] + 1e-3:
        raise SystemExit(f"ERRO: {c} tem {info['dur']:.2f}s, não cobre {dur_s:.2f}s a partir de {ins:.2f}s. Troque o clipe/janela.")
    planos.append({
        "bloco": bl["bloco"], "nome_bloco": bl["nome"], "clipe": c, "arquivo": c + ".MP4",
        "janela": janela, "batidas": nbat, "camada": camada,
        "faixa": faixa, "recorte_y": list(FAIXAS[faixa]) if faixa else None,
        "timeline_in_f": f0, "timeline_out_f": f1, "timeline_in_tc": tc(f0),
        "in_s": round(ins, 3), "out_s": round(ins + dur_s, 3),
        "in_src_f": round(ins * src_fps), "out_src_f": round((ins + dur_s) * src_fps),
        "rotacao": rot[c], "transicao_entrada": trans, "fade_out": fade, "motivo": motivo, "nota_escolha": nota,
        "src": {"largura": info["w"], "altura": info["h"], "fps": f"{info['fps_num']}/{info['fps_den']}", "duracao": info["dur"]},
    })
    print(f"{tc(f0)} {camada} {faixa or 'cheio':5s} {c} {rot[c]:3s} in={ins:6.2f}s dur={dur_s:.2f}s {nota}")


i_beat = 0
for bl in esc["blocos"]:
    if "mosaico" in bl:
        M = bl["mosaico"]; b0 = i_beat; nb_m = M["batidas"]; i_beat += nb_m
        F = lambda k: beat_frames[b0 + k]
        trocas = M["trocas"]
        # o painel 'cheio' fica em tela cheia na batida 0 e continua na faixa do meio até a 1ª troca do meio
        fim_meio = min([t["batida"] for t in trocas if t["faixa"] == "meio"] + [nb_m])
        ch = M["cheio"]; info = probe(os.path.join(A.originais, ch["clipe"] + ".MP4"))
        tot = (F(fim_meio) - F(0)) / SEQ_FPS
        ins, nota = escolher(ch["clipe"], ch["janela"], tot, (ch["clipe"], tuple(ch["janela"]), "cheio"), info)
        add(bl, ch["clipe"], ch["janela"], 1, F(0), F(1), ins, nota, info, ch["motivo"] + " [tela cheia]")
        add(bl, ch["clipe"], ch["janela"], fim_meio - 1, F(1), F(fim_meio), ins + (F(1) - F(0)) / SEQ_FPS,
            "continuação do painel cheio", info, ch["motivo"] + " [faixa do meio]", "V1", "meio")
        for t in trocas:
            fim = min([u["batida"] for u in trocas if u["faixa"] == t["faixa"] and u["batida"] > t["batida"]] + [nb_m])
            info = probe(os.path.join(A.originais, t["clipe"] + ".MP4"))
            dur = (F(fim) - F(t["batida"])) / SEQ_FPS
            ins, nota = escolher(t["clipe"], t["janela"], dur, (t["clipe"], tuple(t["janela"]), t["faixa"]), info)
            add(bl, t["clipe"], t["janela"], fim - t["batida"], F(t["batida"]), F(fim), ins, nota, info, t["motivo"],
                CAMADA[t["faixa"]], t["faixa"])
        continue
    for p in bl["planos"]:
        c = p["clipe"]; info = probe(os.path.join(A.originais, c + ".MP4"))
        f0, f1 = beat_frames[i_beat], beat_frames[i_beat + p["batidas"]]; i_beat += p["batidas"]
        ins, nota = escolher(c, p["janela"], (f1 - f0) / SEQ_FPS, (c, tuple(p["janela"]), p["batidas"]), info)
        add(bl, c, p["janela"], p["batidas"], f0, f1, ins, nota, info, p["motivo"], trans=p.get("transicao_entrada", "corte"),
            fade=p.get("fade_out", False))

planos.sort(key=lambda p: (p["timeline_in_f"], p["camada"]))
for k, p in enumerate(planos): p["n"] = k + 1
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
