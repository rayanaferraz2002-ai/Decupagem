"""Gera checklist_premiere.md e a tabela cena->clipe (tabela_planos.md) a partir do plano.json.

Uso: python3 -I gerar_docs.py plano.json pasta_saida [metricas.json]
"""
import json, sys, os

P = json.load(open(sys.argv[1])); out = sys.argv[2]; FPS = P["sequencia"]["fps"]; DUR = P["sequencia"]["duracao_f"]


def tc(f, fps=FPS):
    s = int(f // fps); return f"00:{s // 60:02d}:{s % 60:02d}:{int(f % fps):02d}"


def src_tc(sec):  # timecode do original (23,976 fps -> exibido em 24 quadros/s)
    f = round(sec * 24000 / 1001); s = f // 24; return f"{s // 60:02d}:{s % 60:02d}:{f % 24:02d}"


# tabela de planos
L = ["| # | Bloco | Timeline (entrada) | Dur. | Trilha / faixa | Arquivo original | Entrada → saída no original | Rotação | Transição | Motivo |",
     "|---|---|---|---|---|---|---|---|---|---|"]
for p in P["planos"]:
    d = (p["timeline_out_f"] - p["timeline_in_f"]) / FPS
    L.append(f"| {p['n']} | {p['bloco']}. {p['nome_bloco']} | {tc(p['timeline_in_f'])} | {d:.2f}s | {p.get('camada', 'V1')} {p.get('faixa') or 'tela cheia'} | {p['arquivo']} | "
             f"{p['in_s']:.2f}s → {p['out_s']:.2f}s ({src_tc(p['in_s'])} → {src_tc(p['out_s'])}) | "
             f"{'90° horário' if p['rotacao'] == 'cw' else '90° anti-horário'} | {p['transicao_entrada']}{' + fade p/ preto' if p['fade_out'] else ''} | {p['motivo']} |")
open(os.path.join(out, "tabela_planos.md"), "w").write("\n".join(L) + "\n")

def crop_pct(p):
    y0, y1 = p["recorte_y"]
    if p["rotacao"] == "cw": return 100 * y0, 100 * (1 - y1)
    return 100 * (1 - y1), 100 * y0


def ref(p): return f"#{p['n']} {p['clipe']} ({p.get('camada', 'V1')}, {tc(p['timeline_in_f'])})"


MOS = [p for p in P["planos"] if p.get("faixa")]
MET = json.load(open(sys.argv[3])) if len(sys.argv) > 3 else {}


def med(p, k):
    s = [x[k] for x in MET.get(p["clipe"], {}).get("segundos", []) if p["in_s"] - 0.5 <= x["t"] <= p["out_s"]]
    return sum(s) / len(s) if s else None


escuros = [p for p in P["planos"] if (med(p, "bright") or 99) < 42]
claros = [p for p in P["planos"] if (med(p, "bright") or 0) > 95]
tremidos = [p for p in P["planos"] if (med(p, "shake") or 0) > 1.8]
cw = [p for p in P["planos"] if p["rotacao"] == "cw"]
ccw = [p for p in P["planos"] if p["rotacao"] == "ccw"]
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
  - Rotation **90** (giro horário): {', '.join(ref(p) for p in cw)}
  - Rotation **−90** (giro anti-horário): {', '.join(ref(p) for p in ccw)}
- [ ] Se algum plano vier com barras pretas/zoom errado: Scale = 66,67 (1080×1920 → 720×1280).
- [ ] Dica de qualidade: os originais em pé têm 1080×1920. Para exportar em resolução cheia, mude a sequência para
      1080×1920 (Sequence Settings) e Scale = 100. Mantive 720×1280 por ser a configuração da referência.

## 3. Mosaico (preview do evento) — confira o Crop
{tc(MOS[0]['timeline_in_f']) if MOS else ''} → {tc(max(p['timeline_out_f'] for p in MOS)) if MOS else ''}: 3 faixas horizontais iguais (como na referência).
Faixa do **meio = V1**, **topo = V2**, **base = V3**. Cada painel mostra o próprio terço do clipe (sem mudar Position),
só com o efeito **Crop** (Left/Right, em % do original deitado). Se o Crop não vier no import, aplique Effects → Transform → Crop com estes valores:

| # | Trilha | Faixa | Entra em | Clipe | Crop Left | Crop Right |
|---|---|---|---|---|---|---|
""" + "\n".join(f"| {p['n']} | {p['camada']} | {p['faixa']} | {tc(p['timeline_in_f'])} | {p['arquivo']} | {crop_pct(p)[0]:.2f}% | {crop_pct(p)[1]:.2f}% |" for p in MOS) + f"""

- [ ] Se um painel mostrar o terço errado do clipe (ex.: o topo aparece embaixo), é porque a rotação veio invertida:
      corrija a rotação (item 2). O Crop está nas coordenadas do original e continua certo.
- [ ] Opcional: um contorno fino entre as faixas (ex.: Stroke/linha de 4 px) se quiser separar mais, como na referência.

## 4. Transições
""" + "\n".join(f"- [ ] Cross Dissolve de {P['dissolve_f']} quadros centrado no corte {tc(p['timeline_in_f'])} (entrada do plano #{p['n']}, {p['nome_bloco']})." for p in diss) + f"""
- [ ] Fade para preto no fim: {tc(DUR - fv)} → {tc(DUR)} ({fv} quadros, Cross Dissolve/Dip to Black no fim do plano #{[p for p in P['planos'] if p.get('fade_out')][-1]['n']}).
- Demais cortes: seco, na batida (estilo da referência).

## 5. Música
- [ ] Trecho da música: começa em {M['in_s']:.3f}s da faixa (no XML: quadro {round(M['in_s'] * FPS)} = {round(M['in_s'] * FPS) / FPS:.3f}s; diferença de {abs(round(M['in_s'] * FPS) / FPS - M['in_s']) * 1000:.0f} ms, imperceptível).
      Se quiser exato, arraste a música {abs(round(M['in_s'] * FPS) / FPS - M['in_s']) * 1000:.0f} ms (slip) no áudio.
- [ ] Fade-out: Cross Fade de {M['fade_out_s']:.0f}s em {tc(DUR - fo)} → {tc(DUR)}. Se não vier no import, faça com keyframes de volume
      (0 dB em {tc(DUR - fo)} → −∞ em {tc(DUR)}).
- [ ] Não há locução (nenhum arquivo de locução no material) — nada a abaixar.

## 6. Velocidade
- Nenhuma alteração de velocidade aplicada (o roteiro não pede; a referência não usa câmera lenta perceptível).

## 7. Textos
- Sem texto na tela (decisão confirmada). Sem .srt.

## 8. Cor (não vai no XML)
O material é noturno, quente (laranja dos guarda-sóis) e alguns planos estão escuros. A referência é clara e saturada.
- [ ] Lumetri em ajuste (Adjustment Layer) na sequência toda: leve aumento de exposição/contraste e vibrance, balanço um pouco mais neutro.
- [ ] Planos mais escuros (pedir +exposição individual): {', '.join(ref(p) for p in escuros) or 'nenhum'}.
- [ ] Planos mais claros (podem precisar baixar realces): {', '.join(ref(p) for p in claros) or 'nenhum'}.

## 9. Estabilização (opcional)
- [ ] Planos com mais tremor: {', '.join(ref(p) for p in tremidos) or 'nenhum'}.
      Warp Stabilizer leve (Smoothness 10–20%) se incomodar.
"""
open(os.path.join(out, "checklist_premiere.md"), "w").write(C)
print("ok")
