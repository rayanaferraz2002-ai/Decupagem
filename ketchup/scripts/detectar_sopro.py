"""Detecta quando a velinha apaga: conta pixels muito claros (chama) numa região acima do burger.
Uso: python3 -I detectar_sopro.py orientacao.json pasta_clipes saida.json [clipes...]
Região (fração do quadro já endireitado): x 0.35–0.65, y roi_y0–roi_y1 (padrão 0.45–0.80)."""
import sys, json, cv2, numpy as np
O = json.load(open(sys.argv[1])); pasta = sys.argv[2]; saida = sys.argv[3]; clips = sys.argv[4:]
rot = {c: cv2.ROTATE_90_CLOCKWISE for c in O["cw"]} | {c: cv2.ROTATE_90_COUNTERCLOCKWISE for c in O["ccw"]}
res = {}
for c in clips:
    cap = cv2.VideoCapture(f"{pasta}/{c}.MP4"); fps = cap.get(cv2.CAP_PROP_FPS); serie = []; i = 0
    y0, y1 = O.get("roi_y", {}).get(c, [0.45, 0.80])
    while True:
        ok, fr = cap.read()
        if not ok: break
        if i % 2 == 0:
            f = cv2.rotate(cv2.resize(fr, (480, 270)), rot[c]); h, w = f.shape[:2]
            roi = f[int(y0 * h):int(y1 * h), int(0.35 * w):int(0.65 * w)]
            hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
            chama = int(((hsv[..., 2] > 235) & (hsv[..., 1] < 140)).sum())
            serie.append((round(i / fps, 2), chama))
        i += 1
    v = np.array([s[1] for s in serie], float); t = np.array([s[0] for s in serie])
    sm = np.convolve(v, np.ones(5) / 5, mode="same")
    acesa = sm > max(3, 0.35 * np.percentile(sm, 90))
    # apagou = último instante aceso antes de ficar apagada por >= 1 s
    apagou = None
    for k in range(len(t) - 1):
        if acesa[k] and not acesa[k + 1:k + 1 + int(1.0 * fps / 2)].any():
            apagou = float(t[k + 1])
    res[c] = {"apagou_s": apagou, "chama_p90": float(np.percentile(v, 90)),
              "acesa_inicio": bool(acesa[:10].any())}
    print(c, res[c], " ".join(f"{a:.1f}:{int(b)}" for a, b in serie[::6]))
json.dump(res, open(saida, "w"), indent=1)
