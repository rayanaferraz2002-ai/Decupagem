# Checklist — o que conferir/aplicar no Premiere

Sequência **720×1280, 24 fps, 42.75 s (1026 quadros)**. Timecodes = timeline.
Trilhas: **V1** vídeo · **A1** áudio dos próprios clipes (falas/sopros) · **A2** música.

## 1. Importar
- [ ] File → Import → `sequencia.xml`. Em "Link Media", aponte a pasta dos originais (MVI_0340.MP4, MVI_0341.MP4, MVI_0342.MP4, MVI_0343.MP4, MVI_0346.MP4, MVI_0347.MP4, MVI_0348.MP4, MVI_0349.MP4) e a música
      `Like A Win (Instrumental).mp4`, com *Align by: File Name*. (Ou gere com `--base "/sua/pasta"` para já sair com o caminho.)

## 2. Rotação e escala (os originais estão deitados)
- [ ] Rotation **90**: #3 MVI_0346 (00:00:07:15), #6 MVI_0347 (00:00:26:05), #7 MVI_0348 (00:00:32:10), #8 MVI_0349 (00:00:35:21)
- [ ] Rotation **−90**: #1 MVI_0343 (00:00:00:00), #2 MVI_0342 (00:00:03:11), #4 MVI_0340 (00:00:11:01), #5 MVI_0341 (00:00:15:04)
- [ ] Se um grupo vier de cabeça para baixo, inverta o sinal (90 ↔ −90) desse grupo. Scale base = 66.67%.
- [ ] Dica: os originais em pé têm 1080×1920; para exportar em resolução cheia, mude a sequência para 1080×1920 e Scale = 100.

## 3. Zoom
- Nenhum zoom nesta edição.

## 4. Áudio
- [ ] A1: ganho por clipe já no XML (Audio Levels) para igualar as vozes: #2 +6.4 dB, #3 +5.8 dB, #4 +12.0 dB, #5 +12.0 dB, #6 +12.0 dB, #7 +0.8 dB, #8 +6.5 dB.
      Gravados baixo (ganho ≥ +10 dB, limite +12): #4 MVI_0340, #5 MVI_0341, #6 MVI_0347. Confira ruído de fundo; se precisar, use DeNoise.
- [ ] Sem áudio da câmera (só música): #1 MVI_0343 (00:00:00:00). Não há clipe de áudio na A1 nesses trechos.
- [ ] A2 (música): no XML está fixa em **-24 dB** (nível sob a fala). Suba para **-13 dB** nos trechos sem fala
      (rampas de ~0,15 s), como na prévia:
      - 00:00:00:00 → 00:00:03:17
      - 00:00:06:21 → 00:00:07:23
      - 00:00:09:14 → 00:00:11:03
      - 00:00:14:10 → 00:00:17:12
      - 00:00:25:16 → 00:00:26:10
      - 00:00:29:16 → 00:00:32:11
      - 00:00:35:06 → 00:00:35:21
      - 00:00:39:19 → 00:00:42:18
      (Alternativa: Essential Sound → música como *Music* com **Ducking** em relação ao *Dialogue*.)
- [ ] Fade-out da música: Cross Fade de 1.5 s em 00:00:41:06 → 00:00:42:18. Se não vier, faça com keyframes de volume.
- [ ] Música começa em 65.600 s da faixa (XML: quadro 1574 = 65.583 s, diferença de 17 ms).

## 5. Transições e fim
- Cortes secos, todos na batida.
- [ ] Fade para preto no fim: 00:00:42:03 → 00:00:42:18.

## 6. Velocidade / textos
- Nenhuma alteração de velocidade. Sem texto na tela e sem legenda (decisão confirmada), por isso não há .srt.

## 7. Cor (não vai no XML)
- [ ] Lumetri leve na sequência toda (exposição/contraste e tons de pele).
- [ ] Brilho médio por plano (0–255): #1 97, #2 95, #3 75, #4 89, #5 100, #6 84, #7 70, #8 89. Mais escuros: #7, #3; mais claros: #1, #5. Iguale a exposição entre eles.
