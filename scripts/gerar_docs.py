"""Gera checklist_premiere.md e a tabela cena->clipe (tabela_planos.md) a partir do plano.json.

Uso: python3 -I gerar_docs.py plano.json pasta_saida
"""
import json, sys, os

P = json.load(open(sys.argv[1])); out = sys.argv[2]; FPS = P["sequencia"]["fps"]; DUR = P["sequencia"]["duracao_f"]


def tc(f, fps=FPS):
    s = int(f // fps); return f"00:{s // 60:02d}:{s % 60:02d}:{int(f % fps):02d}"


def src_tc(sec):  # timecode do original (23,976 fps -> exibido em 24 quadros/s)
    f = round(sec * 24000 / 1001); s = f // 24; return f"{s // 60:02d}:{s % 60:02d}:{f % 24:02d}"


# tabela de planos
L = ["| # | Bloco | Timeline (entrada) | Dur. | Batidas | Arquivo original | Entrada → saída no original | Rotação | Transição | Motivo |",
     "|---|---|---|---|---|---|---|---|---|---|"]
for p in P["planos"]:
    d = (p["timeline_out_f"] - p["timeline_in_f"]) / FPS
    L.append(f"| {p['n']} | {p['bloco']}. {p['nome_bloco']} | {tc(p['timeline_in_f'])} | {d:.2f}s | {p['batidas']} | {p['arquivo']} | "
             f"{p['in_s']:.2f}s → {p['out_s']:.2f}s ({src_tc(p['in_s'])} → {src_tc(p['out_s'])}) | "
             f"{'90° horário' if p['rotacao'] == 'cw' else '90° anti-horário'} | {p['transicao_entrada']}{' + fade p/ preto' if p['fade_out'] else ''} | {p['motivo']} |")
open(os.path.join(out, "tabela_planos.md"), "w").write("\n".join(L) + "\n")

cw = [p for p in P["planos"] if p["rotacao"] == "cw"]; ccw = [p for p in P["planos"] if p["rotacao"] == "ccw"]
diss = [p for p in P["planos"] if p["transicao_entrada"] == "dissolve"]
h = P["dissolve_f"] // 2; fv = P["fade_video_f"]; M = P["musica"]; fo = round(M["fade_out_s"] * FPS)
C = f"""# Checklist — o que conferir/aplicar no Premiere

Sequência: **720×1280, 30 fps, {P['sequencia']['duracao_s']} s ({DUR} quadros)**. Timecodes abaixo = timeline da sequência.

## 1. Ao importar
- [ ] File → Import → `sequencia.xml`. Vai aparecer "Link Media": aponte a pasta com os originais
      (MVI_xxxx.MP4) e marque *Align by: File Name*. A música é `{M['arquivo']}`.
      (Ou gere o XML com o caminho certo: `python3 -I scripts/gerar_xml.py ... --base "/sua/pasta"`.)
- [ ] O áudio de câmera dos clipes **não** foi incluído (só música na A1). Se quiser ambiente, adicione manualmente.

## 2. Rotação (o XML leva, mas confira) — o que o XML pode não carregar bem
Os originais foram gravados com a câmera em pé e estão salvos deitados (1920×1080). Cada clipe tem
Motion → Rotation ±90 e Scale 66,67% no XML.
- [ ] Rode a timeline e veja se algum plano aparece **de cabeça para baixo**. Se acontecer com todos de um
      grupo, inverta o sinal da rotação desse grupo (90 ↔ −90): o sinal de rotação do FCP7 XML pode ser
      interpretado ao contrário em algumas versões.
  - Rotation **90** (giro horário): {', '.join(f"#{p['n']} {p['clipe']} ({tc(p['timeline_in_f'])})" for p in cw)}
  - Rotation **−90** (giro anti-horário): {', '.join(f"#{p['n']} {p['clipe']} ({tc(p['timeline_in_f'])})" for p in ccw)}
- [ ] Se algum plano vier com barras pretas/zoom errado: Scale = 66,67 (1080×1920 → 720×1280).
- [ ] Dica de qualidade: os originais em pé têm 1080×1920. Para exportar em resolução cheia, mude a sequência para
      1080×1920 (Sequence Settings) e Scale = 100. Mantive 720×1280 por ser a configuração da referência.

## 3. Transições
""" + "\n".join(f"- [ ] Cross Dissolve de {P['dissolve_f']} quadros centrado no corte {tc(p['timeline_in_f'])} (entrada do plano #{p['n']}, {p['nome_bloco']})." for p in diss) + f"""
- [ ] Fade para preto no fim: {tc(DUR - fv)} → {tc(DUR)} ({fv} quadros, Cross Dissolve/Dip to Black no fim do plano #{P['planos'][-1]['n']}).
- Demais cortes: seco, na batida (estilo da referência).

## 4. Música
- [ ] Trecho da música: começa em {M['in_s']:.3f}s da faixa (no XML: quadro {round(M['in_s'] * FPS)} = {round(M['in_s'] * FPS) / FPS:.3f}s; diferença de {abs(round(M['in_s'] * FPS) / FPS - M['in_s']) * 1000:.0f} ms, imperceptível).
      Se quiser exato, arraste a música {abs(round(M['in_s'] * FPS) / FPS - M['in_s']) * 1000:.0f} ms (slip) no áudio.
- [ ] Fade-out: Cross Fade de {M['fade_out_s']:.0f}s em {tc(DUR - fo)} → {tc(DUR)}. Se não vier no import, faça com keyframes de volume
      (0 dB em {tc(DUR - fo)} → −∞ em {tc(DUR)}).
- [ ] Não há locução (nenhum arquivo de locução no material) — nada a abaixar.

## 5. Velocidade
- Nenhuma alteração de velocidade aplicada (o roteiro não pede; a referência não usa câmera lenta perceptível).

## 6. Textos
- Sem texto na tela (decisão confirmada). Sem .srt.

## 7. Cor (não vai no XML)
O material é noturno, quente (laranja dos guarda-sóis) e alguns planos estão escuros. A referência é clara e saturada.
- [ ] Lumetri em ajuste (Adjustment Layer) na sequência toda: leve aumento de exposição/contraste e vibrance, balanço um pouco mais neutro.
- [ ] Planos mais escuros, pedir +exposição individual: #9 MVI_0697 ({tc(P['planos'][8]['timeline_in_f'])}), #12 MVI_0331 ({tc(P['planos'][11]['timeline_in_f'])}),
      #15 MVI_0339 ({tc(P['planos'][14]['timeline_in_f'])}), #23 MVI_0324 ({tc(P['planos'][22]['timeline_in_f'])}), #3 MVI_0668 ({tc(P['planos'][2]['timeline_in_f'])}).
- [ ] Planos mais claros (podem precisar baixar realces): #25 MVI_0547 ({tc(P['planos'][24]['timeline_in_f'])}), #27 MVI_0722 ({tc(P['planos'][26]['timeline_in_f'])}).

## 8. Estabilização (opcional)
- [ ] Planos com mais tremor: #18 MVI_0597 ({tc(P['planos'][17]['timeline_in_f'])}), #34 MVI_0579 ({tc(P['planos'][33]['timeline_in_f'])}), #7 MVI_0320 ({tc(P['planos'][6]['timeline_in_f'])}), #1 MVI_0718 ({tc(0)}, é uma panorâmica).
      Warp Stabilizer leve (Smoothness 10–20%) se incomodar.
"""
open(os.path.join(out, "checklist_premiere.md"), "w").write(C)
print("ok")
