"""Monta plano.json dos depoimentos: cada resposta vira um plano com corte na batida.

Uso: python3 -I montar_plano.py dados/escolhas.json dados/orientacao.json dados/mapa_batidas_musica.json \
        dados/empolgacao.json pasta_originais plano.json

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

esc_p, ori_p, mus_p, emp_p, orig, saida = sys.argv[1:7]
E = json.load(open(esc_p)); O = json.load(open(ori_p)); MU = json.load(open(mus_p)); EMP = json.load(open(emp_p))
FPS = 30; W, H = 720, 1280; ALVO_DB = -16.0; ZOOM = 1.12
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
    ja = p.get("janela_entrada") or [p["resposta_ini"] - 0.20, p["resposta_ini"] + 0.03]
    ini = vale(arq, *ja)  # corte no silêncio antes da 1ª palavra
    fim_fala = vale(arq, p["resposta_fim"] - 0.02, p["resposta_fim"] + 0.20)  # fim real da última palavra
    folga = E["cauda_final_s"] if k == N - 1 else 0.12
    limite = min(info["dur"] - 0.05, (p["proxima_fala_s"] or 1e9) - 0.06)
    t_min = t + (fim_fala + folga - ini)
    cand = [b for b in beats if b >= t_min - 1e-6]
    t_out = cand[0]
    if ini + (t_out - t) > limite:  # a batida seguinte invade fala indesejada / fim do clipe: usa a anterior se ainda couber a fala
        ant = [b for b in beats if t + (fim_fala + 0.03 - ini) <= b < t_out]
        if not ant: raise SystemExit(f"ERRO: {c} não cabe entre batidas sem cortar fala")
        t_out = ant[-1]
    f0, f1 = round(t * FPS), round(t_out * FPS)
    dur = (f1 - f0) / FPS
    em = EMP.get(c + ".MP4", {}); ganho = round(ALVO_DB - em.get("volume_db", ALVO_DB), 1)
    planos.append({
        "n": k + 1, "clipe": c, "arquivo": c + ".MP4", "texto": p["texto"], "motivo": p["motivo"],
        "timeline_in_f": f0, "timeline_out_f": f1,
        "timeline_in_tc": f"00:00:{f0 // FPS:02d}:{f0 % FPS:02d}",
        "in_s": round(ini, 3), "out_s": round(ini + dur, 3), "fala_fim_s": round(fim_fala, 3),
        "rotacao": "cw" if c in O["cw"] else "ccw", "zoom": p["zoom"], "zoom_fim": ZOOM if p["zoom"] else 1.0,
        "ganho_fala_db": max(-12.0, min(12.0, ganho)), "transicao_entrada": "corte",
        "fade_out": k == N - 1, "src": info,
    })
    print(f"{k + 1} {planos[-1]['timeline_in_tc']} {c} in={ini:6.2f} out={ini + dur:6.2f} dur={dur:5.2f} "
          f"fala até {fim_fala:6.2f} zoom={p['zoom']} ganho={planos[-1]['ganho_fala_db']:+.1f}dB")
    t = f1 / FPS

total = planos[-1]["timeline_out_f"]
plano = {"sequencia": {"largura": W, "altura": H, "fps": FPS, "duracao_f": total, "duracao_s": round(total / FPS, 3),
                       "fonte": "configuração do vídeo de referência"},
         "musica": {"arquivo": E["musica"]["arquivo"], "in_s": m0, "out_s": round(m0 + total / FPS, 3),
                    "volume_fala_db": E["musica"]["volume_fala_db"], "volume_livre_db": E["musica"]["volume_livre_db"],
                    "falas_f": [[pl["timeline_in_f"], pl["timeline_in_f"] + round((pl["fala_fim_s"] - pl["in_s"]) * FPS)] for pl in planos], "fade_out_s": E["musica"]["fade_out_s"],
                    "bpm": round(60 / np.diff(MU["batidas"]).mean(), 2)},
         "fade_video_f": 15, "planos": planos}
json.dump(plano, open(saida, "w"), ensure_ascii=False, indent=1)
print("total", plano["sequencia"]["duracao_s"], "s")
