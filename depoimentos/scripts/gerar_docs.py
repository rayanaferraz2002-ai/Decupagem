"""Gera checklist_premiere.md e tabela_planos.md a partir do plano.json dos depoimentos.
Uso: python3 -I gerar_docs.py plano.json pasta_saida"""
import json, sys, os

P = json.load(open(sys.argv[1])); out = sys.argv[2]; FPS = P["sequencia"]["fps"]; DUR = P["sequencia"]["duracao_f"]
M = P["musica"]; pl = P["planos"]


def tc(f): s = int(f // FPS); return f"00:00:{s:02d}:{int(f % FPS):02d}"


def stc(sec): f = round(sec * 24000 / 1001); return f"{f // 24 // 60:02d}:{f // 24 % 60:02d}:{f % 24:02d}"


L = ["| # | Timeline | Dur. | Arquivo original | Entrada → saída no original | Rotação | Zoom | Ganho fala | Fala | Motivo |",
     "|---|---|---|---|---|---|---|---|---|---|"]
for p in pl:
    d = (p["timeline_out_f"] - p["timeline_in_f"]) / FPS
    L.append(f"| {p['n']} | {tc(p['timeline_in_f'])} | {d:.2f}s | {p['arquivo']} | {p['in_s']:.2f}s → {p['out_s']:.2f}s ({stc(p['in_s'])} → {stc(p['out_s'])}) | "
             f"{'90° horário' if p['rotacao'] == 'cw' else '90° anti-horário'} | {'sim, 100→' + str(round(p['zoom_fim'] * 100)) + '%' if p['zoom'] else '—'} | "
             f"{p['ganho_fala_db']:+.1f} dB | “{p['texto']}” | {p['motivo']} |")
open(os.path.join(out, "tabela_planos.md"), "w").write("\n".join(L) + "\n")

esc = 100 * 1280 / 1920
pausas = []
for k, (a, b) in enumerate(M["falas_f"]):
    fim = pl[k]["timeline_out_f"]
    if fim - b >= 6: pausas.append((b, fim if k == len(pl) - 1 else min(fim, M["falas_f"][k + 1][0])))
C = f"""# Checklist — o que conferir/aplicar no Premiere

Sequência **720×1280, 30 fps, {P['sequencia']['duracao_s']} s ({DUR} quadros)**. Timecodes = timeline.
Trilhas: **V1** depoimentos · **A1** fala dos próprios clipes · **A2** música.

## 1. Importar
- [ ] File → Import → `sequencia.xml`. Em "Link Media", aponte a pasta dos originais (`MVI_0585…0598.MP4`) e a música
      `{M['arquivo']}`, com *Align by: File Name*. (Ou gere com `--base "/sua/pasta"` para já sair com o caminho.)

## 2. Rotação e escala (os originais estão deitados)
- [ ] Rotation **90**: {', '.join(f"#{p['n']} {p['clipe']} ({tc(p['timeline_in_f'])})" for p in pl if p['rotacao'] == 'cw')}
- [ ] Rotation **−90**: {', '.join(f"#{p['n']} {p['clipe']} ({tc(p['timeline_in_f'])})" for p in pl if p['rotacao'] == 'ccw')}
- [ ] Se um grupo vier de cabeça para baixo, inverta o sinal (90 ↔ −90) desse grupo. Scale base = {esc:.2f}%.
- [ ] Dica: os originais em pé têm 1080×1920; para exportar em resolução cheia, mude a sequência para 1080×1920 e Scale = 100 (zoom: 100 → 112).

## 3. Zoom-in (keyframes de Scale — confira se vieram)
""" + "\n".join(f"- [ ] #{p['n']} {p['clipe']}: Scale {esc:.2f}% em {tc(p['timeline_in_f'])} → {esc * p['zoom_fim']:.2f}% em {tc(p['timeline_out_f'] - 1)} (linear)."
                for p in pl if p["zoom"]) + f"""
- Se os keyframes não vierem no import, crie os dois keyframes de Scale à mão com esses valores (Effect Controls → Motion → Scale).

## 4. Áudio
- [ ] A1 (fala): ganho por clipe já no XML (Audio Levels/Clip Volume) para igualar as vozes:
      {', '.join(f"#{p['n']} {p['ganho_fala_db']:+.1f} dB" for p in pl)}. O #3 (MVI_0587) foi gravado baixo: confira se não ficou com ruído.
- [ ] A2 (música): no XML está fixa em **{M['volume_fala_db']} dB** (nível sob a fala). Suba para **{M['volume_livre_db']} dB** nas pausas sem fala
      (com rampas de ~0,15 s), como na prévia:
""" + "\n".join(f"      - {tc(a)} → {tc(b)}" for a, b in pausas) + f"""
      (Alternativa: Essential Sound → música como *Music* com **Ducking** ativado em relação ao *Dialogue*.)
- [ ] Fade-out da música: Cross Fade de {M['fade_out_s']} s em {tc(DUR - round(M['fade_out_s'] * FPS))} → {tc(DUR)}. Se não vier, faça com keyframes de volume.
- [ ] Música começa em {M['in_s']:.3f} s da faixa (XML: quadro {round(M['in_s'] * FPS)} = {round(M['in_s'] * FPS) / FPS:.3f} s, diferença de {abs(round(M['in_s'] * FPS) / FPS - M['in_s']) * 1000:.0f} ms).

## 5. Transições e fim
- Cortes secos na batida entre os depoimentos (como na referência, que corta a cada troca de pessoa).
- [ ] Fade para preto no fim: {tc(DUR - P['fade_video_f'])} → {tc(DUR)}.

## 6. Velocidade / textos
- Nenhuma alteração de velocidade. Sem texto na tela e sem legenda (decisão confirmada), por isso não há .srt.

## 7. Cor (não vai no XML)
- [ ] Material noturno e quente. Lumetri leve na sequência toda (exposição/contraste e tons de pele); os mais escuros são o #3 (MVI_0587, brilho médio 42/255) e o #6 (MVI_0589, 43/255); o mais claro é o #5 (MVI_0586, 76/255). Iguale a exposição entre eles.
"""
open(os.path.join(out, "checklist_premiere.md"), "w").write(C)
print("ok")
