"""Monta plano.json (desejos de aniversário): cada plano = trecho de fala e/ou sopro da velinha, corte na batida.

Uso: python3 -I montar_plano.py dados/escolhas.json dados/orientacao.json dados/mapa_batidas_musica.json pasta_originais plano.json
Campos por plano em escolhas.json: clipe, ini (início do conteúdo, s), fim (fim do conteúdo: última palavra ou
vela apagada), voz (lista [a,b] de trechos com fala, para baixar a música), limite (s máx. de saída), janela_entrada (opc.), ini_min (opc.: entrada mais cedo aceitável).

Regras:
- entrada = início da resposta, ajustada para o silêncio mais próximo antes da 1ª palavra (sem pegar
  'minha parte favorita... é' nos planos 2+);
- saída = 1ª batida da música depois do fim da fala (+ folga), nunca entrando na próxima fala indesejada;
- último plano segura cauda_final_s depois da fala para o fade;
- ganho por clipe iguala o volume da fala (mediana -16 dB);
- zoom-in lento (100% -> 112%) nos planos marcados.
"""
import sys, json, subprocess
import numpy as np

esc_p, ori_p, mus_p, orig, saida = sys.argv[1:6]
E = json.load(open(esc_p)); O = json.load(open(ori_p)); MU = json.load(open(mus_p))
FPS = E.get("fps", 30); W, H = 720, 1280; ALVO_DB = -16.0; ZOOM = 1.12
m0 = E["musica"]["inicio"]
beats = np.array([t - m0 for t in MU["batidas"] if t >= m0 - 0.01]); beats[0] = 0.0


def pcm(arq, a, d):
    b = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{max(a, 0):.3f}", "-t", f"{d:.3f}", "-i", arq, "-ac", "1", "-ar", "16000",
                        "-f", "s16le", "-"], capture_output=True).stdout
    return np.frombuffer(b, np.int16).astype(np.float32) / 32768


def vale(arq, a, b):
    """instante de menor energia (janelas de 10 ms) entre a e b"""
    y = pcm(arq, a, b - a); n = 160
    e = [np.sqrt((y[i:i + n] ** 2).mean()) for i in range(0, max(len(y) - n, 1), n)]
    return a + int(np.argmin(e)) * 0.01


def probe(arq):
    j = json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                   "stream=width,height,r_frame_rate:format=duration", "-of", "json", arq], capture_output=True, text=True).stdout)
    s = j["streams"][0]; n, d = map(int, s["r_frame_rate"].split("/"))
    return {"w": s["width"], "h": s["height"], "fps": f"{n}/{d}", "fps_f": n / d, "dur": float(j["format"]["duration"])}


planos = []; t = 0.0; N = len(E["planos"])
for k, p in enumerate(E["planos"]):
    c = p["clipe"]; arq = f"{orig}/{c}.MP4"; info = probe(arq)
    ja = p.get("janela_entrada") or [p["ini"] - 0.20, p["ini"] + 0.03]
    ini = vale(arq, *ja)  # corte no silêncio antes do conteúdo
    fim_fala = p["fim"]
    folga = E["cauda_final_s"] if k == N - 1 else 0.12
    limite = min(info["dur"] - 0.05, p.get("limite") or 1e9)
    t_min = t + (fim_fala + folga - ini)
    cand = [b for b in beats if b >= t_min - 1e-6]
    t_out = cand[0]
    if ini + (t_out - t) > limite:  # a batida seguinte invade fala indesejada / fim do clipe
        ant = [b for b in beats if t + (fim_fala + 0.03 - ini) <= b < t_out]
        if ant:
            t_out = ant[-1]  # usa a batida anterior se ainda couber o conteúdo
        elif p.get("ini_min") is not None and limite - (t_out - t) >= p["ini_min"]:
            ini = limite - (t_out - t)  # recua a entrada (trecho parado/silencioso antes do conteúdo) para fechar na batida
        else:
            raise SystemExit(f"ERRO: {c} não cabe entre batidas sem cortar conteúdo (defina ini_min ou ajuste fim/limite)")
    f0, f1 = round(t * FPS), round(t_out * FPS)
    dur = (f1 - f0) / FPS
    if p.get("voz"):  # ganho para igualar a voz: mediana do nível das janelas ativas nos trechos de fala
        y = np.concatenate([pcm(arq, a, b - a) for a, b in p["voz"]]); n = 400
        r = np.array([np.sqrt((y[i:i + n] ** 2).mean()) for i in range(0, len(y) - n, n)])
        db = 20 * np.log10(r[r > r.max() * 0.1] + 1e-9); ganho = round(ALVO_DB - float(np.median(db)), 1)
    else:
        ganho = 0.0
    planos.append({
        "n": k + 1, "cena": p.get("cena", ""), "clipe": c, "arquivo": c + ".MP4", "texto": p["texto"], "motivo": p["motivo"],
        "timeline_in_f": f0, "timeline_out_f": f1,
        "timeline_in_tc": f"00:00:{f0 // FPS:02d}:{f0 % FPS:02d}",
        "in_s": round(ini, 3), "out_s": round(ini + dur, 3), "fala_fim_s": round(fim_fala, 3),
        "rotacao": "cw" if c in O["cw"] else "ccw", "zoom": p.get("zoom", False), "zoom_fim": ZOOM if p.get("zoom") else 1.0,
        "voz_s": p.get("voz", []), "som": p.get("som", True),
        "ganho_fala_db": max(-12.0, min(12.0, ganho)), "transicao_entrada": "corte",
        "fade_out": k == N - 1, "src": info,
    })
    print(f"{k + 1} {planos[-1]['timeline_in_tc']} {c} in={ini:6.2f} out={ini + dur:6.2f} dur={dur:5.2f} "
          f"conteúdo até {fim_fala:6.2f} ganho={planos[-1]['ganho_fala_db']:+.1f}dB")
    t = f1 / FPS

total = planos[-1]["timeline_out_f"]
plano = {"sequencia": {"nome": E.get("nome", "Sequencia"), "largura": W, "altura": H, "fps": FPS, "duracao_f": total, "duracao_s": round(total / FPS, 3),
                       "fonte": "configuração do vídeo de referência"},
         "musica": {"arquivo": E["musica"]["arquivo"], "in_s": m0, "out_s": round(m0 + total / FPS, 3),
                    "volume_fala_db": E["musica"]["volume_fala_db"], "volume_livre_db": E["musica"]["volume_livre_db"],
                    "falas_f": [[pl["timeline_in_f"] + max(0, round((a - pl["in_s"]) * FPS)), pl["timeline_in_f"] + min(pl["timeline_out_f"] - pl["timeline_in_f"], round((b - pl["in_s"]) * FPS))]
                                for pl in planos for a, b in pl["voz_s"]], "fade_out_s": E["musica"]["fade_out_s"],
                    "bpm": round(60 / np.diff(MU["batidas"]).mean(), 2)},
         "fade_video_f": 15, "planos": planos}
json.dump(plano, open(saida, "w"), ensure_ascii=False, indent=1)
print("total", plano["sequencia"]["duracao_s"], "s")
