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
  - Rotation **90** (giro horário): #1 MVI_0718 (00:00:00:00), #2 MVI_0549 (00:00:01:29), #3 MVI_0668 (00:00:02:29), #4 MVI_0719 (00:00:03:29), #5 MVI_0578 (00:00:04:29), #6 MVI_0696 (00:00:05:29), #7 MVI_0320 (00:00:06:29), #8 MVI_0323 (00:00:07:29), #9 MVI_0697 (00:00:08:29), #10 MVI_0333 (00:00:09:29), #11 MVI_0552 (00:00:10:29), #12 MVI_0331 (00:00:11:29), #13 MVI_0554 (00:00:12:29), #14 MVI_0326 (00:00:13:29), #15 MVI_0339 (00:00:14:29), #19 MVI_0710 (00:00:20:00), #20 MVI_0711 (00:00:21:29), #21 MVI_0610 (00:00:23:29), #23 MVI_0324 (00:00:27:29), #24 MVI_0551 (00:00:29:29), #26 MVI_0553 (00:00:32:29), #27 MVI_0722 (00:00:33:29), #29 MVI_0558 (00:00:35:14), #31 MVI_0723 (00:00:36:29), #34 MVI_0579 (00:00:39:29)
  - Rotation **−90** (giro anti-horário): #16 MVI_0582 (00:00:15:29), #17 MVI_0544 (00:00:16:29), #18 MVI_0597 (00:00:17:29), #22 MVI_0656 (00:00:25:29), #25 MVI_0547 (00:00:31:28), #28 MVI_0557 (00:00:34:29), #30 MVI_0571 (00:00:35:29), #32 MVI_0580 (00:00:37:29), #33 MVI_0581 (00:00:38:29), #35 MVI_0713 (00:00:41:29)
- [ ] Se algum plano vier com barras pretas/zoom errado: Scale = 66,67 (1080×1920 → 720×1280).
- [ ] Dica de qualidade: os originais em pé têm 1080×1920. Para exportar em resolução cheia, mude a sequência para
      1080×1920 (Sequence Settings) e Scale = 100. Mantive 720×1280 por ser a configuração da referência.

## 3. Transições
- [ ] Cross Dissolve de 8 quadros centrado no corte 00:00:17:29 (entrada do plano #18, Burger).
- [ ] Cross Dissolve de 8 quadros centrado no corte 00:00:31:28 (entrada do plano #25, Comemoração).
- [ ] Fade para preto no fim: 00:00:43:05 → 00:00:43:29 (24 quadros, Cross Dissolve/Dip to Black no fim do plano #35).
- Demais cortes: seco, na batida (estilo da referência).

## 4. Música
- [ ] Trecho da música: começa em 15.116s da faixa (no XML: quadro 453 = 15.100s; diferença de 16 ms, imperceptível).
      Se quiser exato, arraste a música 16 ms (slip) no áudio.
- [ ] Fade-out: Cross Fade de 2s em 00:00:41:29 → 00:00:43:29. Se não vier no import, faça com keyframes de volume
      (0 dB em 00:00:41:29 → −∞ em 00:00:43:29).
- [ ] Não há locução (nenhum arquivo de locução no material) — nada a abaixar.

## 5. Velocidade
- Nenhuma alteração de velocidade aplicada (o roteiro não pede; a referência não usa câmera lenta perceptível).

## 6. Textos
- Sem texto na tela (decisão confirmada). Sem .srt.

## 7. Cor (não vai no XML)
O material é noturno, quente (laranja dos guarda-sóis) e alguns planos estão escuros. A referência é clara e saturada.
- [ ] Lumetri em ajuste (Adjustment Layer) na sequência toda: leve aumento de exposição/contraste e vibrance, balanço um pouco mais neutro.
- [ ] Planos mais escuros, pedir +exposição individual: #9 MVI_0697 (00:00:08:29), #12 MVI_0331 (00:00:11:29),
      #15 MVI_0339 (00:00:14:29), #23 MVI_0324 (00:00:27:29), #3 MVI_0668 (00:00:02:29).
- [ ] Planos mais claros (podem precisar baixar realces): #25 MVI_0547 (00:00:31:28), #27 MVI_0722 (00:00:33:29).

## 8. Estabilização (opcional)
- [ ] Planos com mais tremor: #18 MVI_0597 (00:00:17:29), #34 MVI_0579 (00:00:39:29), #7 MVI_0320 (00:00:06:29), #1 MVI_0718 (00:00:00:00, é uma panorâmica).
      Warp Stabilizer leve (Smoothness 10–20%) se incomodar.
