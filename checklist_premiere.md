# Checklist — o que conferir/aplicar no Premiere

Sequência: **720×1280, 30 fps, 43.967 s (1319 quadros)**. Timecodes abaixo = timeline da sequência.

## 1. Ao importar
- [ ] File → Import → `sequencia.xml`. Vai aparecer "Link Media": aponte a pasta com os originais
      (MVI_xxxx.MP4) e marque *Align by: File Name*. A música é `Bring It (Instrumental).mp4`.
      (Ou gere o XML com o caminho certo: `python3 -I scripts/gerar_xml.py ... --base "/sua/pasta"`.)
- [ ] O áudio de câmera dos clipes **não** foi incluído (só música na A1). Se quiser ambiente, adicione manualmente.

## 2. Rotação (o XML leva, mas confira) — o que o XML pode não carregar bem
Os originais foram gravados com a câmera em pé e estão salvos deitados (1920×1080). Cada clipe tem
Motion → Rotation ±90 e Scale 66,67% no XML.
- [ ] Rode a timeline e veja se algum plano aparece **de cabeça para baixo**. Se acontecer com todos de um
      grupo, inverta o sinal da rotação desse grupo (90 ↔ −90): o sinal de rotação do FCP7 XML pode ser
      interpretado ao contrário em algumas versões.
  - Rotation **90** (giro horário): #2 MVI_0549 (V1, 00:00:01:29), #3 MVI_0549 (V1, 00:00:02:14), #4 MVI_0719 (V2, 00:00:02:14), #6 MVI_0718 (V2, 00:00:02:29), #7 MVI_0722 (V3, 00:00:03:14), #9 MVI_0578 (V2, 00:00:04:14), #10 MVI_0333 (V3, 00:00:04:29), #11 MVI_0553 (V1, 00:00:05:14), #12 MVI_0723 (V2, 00:00:05:29), #13 MVI_0339 (V3, 00:00:06:14), #15 MVI_0328 (V2, 00:00:07:14), #16 MVI_0320 (V3, 00:00:07:29), #17 MVI_0668 (V1, 00:00:08:14), #18 MVI_0325 (V2, 00:00:08:29), #19 MVI_0696 (V3, 00:00:09:14), #20 MVI_0711 (V1, 00:00:09:29), #21 MVI_0610 (V1, 00:00:10:29), #22 MVI_0324 (V1, 00:00:11:29), #23 MVI_0332 (V1, 00:00:12:29), #31 MVI_0710 (V1, 00:00:23:29), #35 MVI_0331 (V1, 00:00:31:28), #36 MVI_0551 (V1, 00:00:32:29), #38 MVI_0323 (V1, 00:00:34:29), #40 MVI_0723 (V1, 00:00:36:29), #42 MVI_0555 (V1, 00:00:38:29), #44 MVI_0697 (V1, 00:00:40:29)
  - Rotation **−90** (giro anti-horário): #1 MVI_0713 (V1, 00:00:00:00), #5 MVI_0321 (V3, 00:00:02:14), #8 MVI_0547 (V1, 00:00:03:29), #14 MVI_0557 (V1, 00:00:06:29), #24 MVI_0717 (V1, 00:00:13:29), #25 MVI_0709 (V1, 00:00:14:29), #26 MVI_0656 (V1, 00:00:15:29), #27 MVI_0704 (V1, 00:00:16:29), #28 MVI_0541 (V1, 00:00:17:29), #29 MVI_0542 (V1, 00:00:20:00), #30 MVI_0597 (V1, 00:00:21:29), #32 MVI_0596 (V1, 00:00:25:29), #33 MVI_0543 (V1, 00:00:27:29), #34 MVI_0705 (V1, 00:00:29:29), #37 MVI_0582 (V1, 00:00:33:29), #39 MVI_0571 (V1, 00:00:35:29), #41 MVI_0581 (V1, 00:00:37:29), #43 MVI_0580 (V1, 00:00:39:29), #45 MVI_0544 (V1, 00:00:41:29)
- [ ] Se algum plano vier com barras pretas/zoom errado: Scale = 66,67 (1080×1920 → 720×1280).
- [ ] Dica de qualidade: os originais em pé têm 1080×1920. Para exportar em resolução cheia, mude a sequência para
      1080×1920 (Sequence Settings) e Scale = 100. Mantive 720×1280 por ser a configuração da referência.

## 3. Mosaico (preview do evento) — confira o Crop
00:00:02:14 → 00:00:09:29: 3 faixas horizontais iguais (como na referência).
Faixa do **meio = V1**, **topo = V2**, **base = V3**. Cada painel mostra o próprio terço do clipe (sem mudar Position),
só com o efeito **Crop** (Left/Right, em % do original deitado). Se o Crop não vier no import, aplique Effects → Transform → Crop com estes valores:

| # | Trilha | Faixa | Entra em | Clipe | Crop Left | Crop Right |
|---|---|---|---|---|---|---|
| 3 | V1 | meio | 00:00:02:14 | MVI_0549.MP4 | 33.33% | 33.33% |
| 4 | V2 | topo | 00:00:02:14 | MVI_0719.MP4 | 0.00% | 66.67% |
| 5 | V3 | base | 00:00:02:14 | MVI_0321.MP4 | 0.00% | 66.67% |
| 6 | V2 | topo | 00:00:02:29 | MVI_0718.MP4 | 0.00% | 66.67% |
| 7 | V3 | base | 00:00:03:14 | MVI_0722.MP4 | 66.67% | 0.00% |
| 8 | V1 | meio | 00:00:03:29 | MVI_0547.MP4 | 33.33% | 33.33% |
| 9 | V2 | topo | 00:00:04:14 | MVI_0578.MP4 | 0.00% | 66.67% |
| 10 | V3 | base | 00:00:04:29 | MVI_0333.MP4 | 66.67% | 0.00% |
| 11 | V1 | meio | 00:00:05:14 | MVI_0553.MP4 | 33.33% | 33.33% |
| 12 | V2 | topo | 00:00:05:29 | MVI_0723.MP4 | 0.00% | 66.67% |
| 13 | V3 | base | 00:00:06:14 | MVI_0339.MP4 | 66.67% | 0.00% |
| 14 | V1 | meio | 00:00:06:29 | MVI_0557.MP4 | 33.33% | 33.33% |
| 15 | V2 | topo | 00:00:07:14 | MVI_0328.MP4 | 0.00% | 66.67% |
| 16 | V3 | base | 00:00:07:29 | MVI_0320.MP4 | 66.67% | 0.00% |
| 17 | V1 | meio | 00:00:08:14 | MVI_0668.MP4 | 33.33% | 33.33% |
| 18 | V2 | topo | 00:00:08:29 | MVI_0325.MP4 | 0.00% | 66.67% |
| 19 | V3 | base | 00:00:09:14 | MVI_0696.MP4 | 66.67% | 0.00% |

- [ ] Se um painel mostrar o terço errado do clipe (ex.: o topo aparece embaixo), é porque a rotação veio invertida:
      corrija a rotação (item 2). O Crop está nas coordenadas do original e continua certo.
- [ ] Opcional: um contorno fino entre as faixas (ex.: Stroke/linha de 4 px) se quiser separar mais, como na referência.

## 4. Transições
- [ ] Cross Dissolve de 8 quadros centrado no corte 00:00:17:29 (entrada do plano #28, Chopp).
- [ ] Fade para preto no fim: 00:00:43:05 → 00:00:43:29 (24 quadros, Cross Dissolve/Dip to Black no fim do plano #45).
- Demais cortes: seco, na batida (estilo da referência).

## 5. Música
- [ ] Trecho da música: começa em 15.116s da faixa (no XML: quadro 453 = 15.100s; diferença de 16 ms, imperceptível).
      Se quiser exato, arraste a música 16 ms (slip) no áudio.
- [ ] Fade-out: Cross Fade de 2s em 00:00:41:29 → 00:00:43:29. Se não vier no import, faça com keyframes de volume
      (0 dB em 00:00:41:29 → −∞ em 00:00:43:29).
- [ ] Não há locução (nenhum arquivo de locução no material) — nada a abaixar.

## 6. Velocidade
- Nenhuma alteração de velocidade aplicada (o roteiro não pede; a referência não usa câmera lenta perceptível).

## 7. Textos
- Sem texto na tela (decisão confirmada). Sem .srt.

## 8. Cor (não vai no XML)
O material é noturno, quente (laranja dos guarda-sóis) e alguns planos estão escuros. A referência é clara e saturada.
- [ ] Lumetri em ajuste (Adjustment Layer) na sequência toda: leve aumento de exposição/contraste e vibrance, balanço um pouco mais neutro.
- [ ] Planos mais escuros (pedir +exposição individual): #13 MVI_0339 (V3, 00:00:06:14), #17 MVI_0668 (V1, 00:00:08:14), #22 MVI_0324 (V1, 00:00:11:29), #29 MVI_0542 (V1, 00:00:20:00), #35 MVI_0331 (V1, 00:00:31:28), #44 MVI_0697 (V1, 00:00:40:29).
- [ ] Planos mais claros (podem precisar baixar realces): #7 MVI_0722 (V3, 00:00:03:14), #8 MVI_0547 (V1, 00:00:03:29), #12 MVI_0723 (V2, 00:00:05:29).

## 9. Estabilização (opcional)
- [ ] Planos com mais tremor: #16 MVI_0320 (V3, 00:00:07:29), #17 MVI_0668 (V1, 00:00:08:14), #30 MVI_0597 (V1, 00:00:21:29), #38 MVI_0323 (V1, 00:00:34:29), #42 MVI_0555 (V1, 00:00:38:29).
      Warp Stabilizer leve (Smoothness 10–20%) se incomodar.
