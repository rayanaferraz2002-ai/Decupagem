"""Gera checklist_premiere.md e tabela_planos.md a partir do plano.json (planos com fala + música).
Uso: python3 -I gerar_docs.py plano.json pasta_saida [preview.mp4]
Com a prévia, mede o brilho médio de cada plano para a seção de cor."""
import json, sys, os

P = json.load(open(sys.argv[1])); out = sys.argv[2]; prev = sys.argv[3] if len(sys.argv) > 3 else None
S = P["sequencia"]; FPS = S["fps"]; DUR = S["duracao_f"]; M = P["musica"]; pl = P["planos"]


def tc(f): s = int(f // FPS); return f"00:{s // 60:02d}:{s % 60:02d}:{int(f % FPS):02d}"


def stc(sec): f = round(sec * 24000 / 1001); return f"{f // 24 // 60:02d}:{f // 24 % 60:02d}:{f % 24:02d}"


L = ["| # | Cena | Timeline | Dur. | Arquivo original | Entrada → saída no original | Rotação | Zoom | Áudio da câmera | Conteúdo | Motivo |",
     "|---|---|---|---|---|---|---|---|---|---|---|"]
for p in pl:
    d = (p["timeline_out_f"] - p["timeline_in_f"]) / FPS
    som = f"{p['ganho_fala_db']:+.1f} dB" if p.get("som", True) else "mudo"
    L.append(f"| {p['n']} | {p.get('cena', p['n'])} | {tc(p['timeline_in_f'])} | {d:.2f}s | {p['arquivo']} | {p['in_s']:.2f}s → {p['out_s']:.2f}s "
             f"({stc(p['in_s'])} → {stc(p['out_s'])}) | {'90° horário' if p['rotacao'] == 'cw' else '90° anti-horário'} | "
             f"{'100→' + str(round(p['zoom_fim'] * 100)) + '%' if p.get('zoom') else '—'} | {som} | {p['texto']} | {p['motivo']} |")
open(os.path.join(out, "tabela_planos.md"), "w").write("\n".join(L) + "\n")

# pausas sem fala (>= 1/4 s): onde a música sobe
cob = [False] * DUR
for a, b in M["falas_f"]:
    for f in range(max(0, a), min(DUR, b)): cob[f] = True
pausas, f = [], 0
while f < DUR:
    if not cob[f]:
        g = f
        while g < DUR and not cob[g]: g += 1
        if g - f >= FPS // 4: pausas.append((f, g))
        f = g
    else:
        f += 1

brilho = {}
if prev:
    import cv2
    cap = cv2.VideoCapture(prev)
    for p in pl:
        v = []
        for fr in range(p["timeline_in_f"] + 2, p["timeline_out_f"] - FPS // 2, max(1, FPS // 3)):
            cap.set(cv2.CAP_PROP_POS_FRAMES, fr); ok, im = cap.read()
            if ok: v.append(cv2.cvtColor(im, cv2.COLOR_BGR2GRAY).mean())
        if v: brilho[p["n"]] = sum(v) / len(v)
esc = 100 * S["altura"] / pl[0]["src"]["w"]
zooms = [p for p in pl if p.get("zoom")]
mudos = [p for p in pl if not p.get("som", True)]
altos = [p for p in pl if p.get("som", True) and p["ganho_fala_db"] >= 10]
nomes = sorted({p["arquivo"] for p in pl})
C = f"""# Checklist — o que conferir/aplicar no Premiere

Sequência **{S['largura']}×{S['altura']}, {FPS} fps, {S['duracao_s']} s ({DUR} quadros)**. Timecodes = timeline.
Trilhas: **V1** vídeo · **A1** áudio dos próprios clipes (falas/sopros) · **A2** música.

## 1. Importar
- [ ] File → Import → `sequencia.xml`. Em "Link Media", aponte a pasta dos originais ({', '.join(nomes)}) e a música
      `{M['arquivo']}`, com *Align by: File Name*. (Ou gere com `--base "/sua/pasta"` para já sair com o caminho.)

## 2. Rotação e escala (os originais estão deitados)
- [ ] Rotation **90**: {', '.join(f"#{p['n']} {p['clipe']} ({tc(p['timeline_in_f'])})" for p in pl if p['rotacao'] == 'cw') or '—'}
- [ ] Rotation **−90**: {', '.join(f"#{p['n']} {p['clipe']} ({tc(p['timeline_in_f'])})" for p in pl if p['rotacao'] == 'ccw') or '—'}
- [ ] Se um grupo vier de cabeça para baixo, inverta o sinal (90 ↔ −90) desse grupo. Scale base = {esc:.2f}%.
- [ ] Dica: os originais em pé têm 1080×1920; para exportar em resolução cheia, mude a sequência para 1080×1920 e Scale = 100.
"""
if zooms:
    C += "\n## 3. Zoom-in (keyframes de Scale — confira se vieram)\n" + "\n".join(
        f"- [ ] #{p['n']} {p['clipe']}: Scale {esc:.2f}% em {tc(p['timeline_in_f'])} → {esc * p['zoom_fim']:.2f}% em {tc(p['timeline_out_f'] - 1)} (linear)."
        for p in zooms) + "\n- Se os keyframes não vierem no import, crie-os à mão (Effect Controls → Motion → Scale).\n"
else:
    C += "\n## 3. Zoom\n- Nenhum zoom nesta edição.\n"
C += f"""
## 4. Áudio
- [ ] A1: ganho por clipe já no XML (Audio Levels) para igualar as vozes: {', '.join(f"#{p['n']} {p['ganho_fala_db']:+.1f} dB" for p in pl if p.get('som', True))}.
"""
if altos:
    C += f"      Gravados baixo (ganho ≥ +10 dB, limite +12): {', '.join(f'#{p['n']} {p['clipe']}' for p in altos)}. Confira ruído de fundo; se precisar, use DeNoise.\n"
if mudos:
    C += f"- [ ] Sem áudio da câmera (só música): {', '.join(f'#{p['n']} {p['clipe']} ({tc(p['timeline_in_f'])})' for p in mudos)}. Não há clipe de áudio na A1 nesses trechos.\n"
C += f"""- [ ] A2 (música): no XML está fixa em **{M['volume_fala_db']} dB** (nível sob a fala). Suba para **{M['volume_livre_db']} dB** nos trechos sem fala
      (rampas de ~0,15 s), como na prévia:
""" + "\n".join(f"      - {tc(a)} → {tc(b)}" for a, b in pausas) + f"""
      (Alternativa: Essential Sound → música como *Music* com **Ducking** em relação ao *Dialogue*.)
- [ ] Fade-out da música: Cross Fade de {M['fade_out_s']} s em {tc(DUR - round(M['fade_out_s'] * FPS))} → {tc(DUR)}. Se não vier, faça com keyframes de volume.
- [ ] Música começa em {M['in_s']:.3f} s da faixa (XML: quadro {round(M['in_s'] * FPS)} = {round(M['in_s'] * FPS) / FPS:.3f} s, diferença de {abs(round(M['in_s'] * FPS) / FPS - M['in_s']) * 1000:.0f} ms).

## 5. Transições e fim
- Cortes secos, todos na batida.
- [ ] Fade para preto no fim: {tc(DUR - P['fade_video_f'])} → {tc(DUR)}.

## 6. Velocidade / textos
- Nenhuma alteração de velocidade. Sem texto na tela e sem legenda (decisão confirmada), por isso não há .srt.

## 7. Cor (não vai no XML)
- [ ] Lumetri leve na sequência toda (exposição/contraste e tons de pele).
"""
if brilho:
    o = sorted(brilho.items(), key=lambda kv: kv[1])
    C += (f"- [ ] Brilho médio por plano (0–255): {', '.join(f'#{n} {b:.0f}' for n, b in sorted(brilho.items()))}. "
          f"Mais escuros: {', '.join(f'#{n}' for n, _ in o[:2])}; mais claros: {', '.join(f'#{n}' for n, _ in o[-2:])}. Iguale a exposição entre eles.\n")
open(os.path.join(out, "checklist_premiere.md"), "w").write(C)
print("ok")
