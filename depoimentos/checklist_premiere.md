# Checklist — o que conferir/aplicar no Premiere

Sequência **720×1280, 30 fps, 43.3 s (1299 quadros)**. Timecodes = timeline.
Trilhas: **V1** depoimentos · **A1** fala dos próprios clipes · **A2** música.

## 1. Importar
- [ ] File → Import → `sequencia.xml`. Em "Link Media", aponte a pasta dos originais (`MVI_0585…0598.MP4`) e a música
      `Feels Good (Instrumental).mp4`, com *Align by: File Name*. (Ou gere com `--base "/sua/pasta"` para já sair com o caminho.)

## 2. Rotação e escala (os originais estão deitados)
- [ ] Rotation **90**: #3 MVI_0587 (00:00:18:08), #4 MVI_0598 (00:00:22:28), #5 MVI_0586 (00:00:31:24)
- [ ] Rotation **−90**: #1 MVI_0585 (00:00:00:00), #2 MVI_0588 (00:00:13:17), #6 MVI_0589 (00:00:37:01), #7 MVI_0590 (00:00:40:05)
- [ ] Se um grupo vier de cabeça para baixo, inverta o sinal (90 ↔ −90) desse grupo. Scale base = 66.67%.
- [ ] Dica: os originais em pé têm 1080×1920; para exportar em resolução cheia, mude a sequência para 1080×1920 e Scale = 100 (zoom: 100 → 112).

## 3. Zoom-in (keyframes de Scale — confira se vieram)
- [ ] #3 MVI_0587: Scale 66.67% em 00:00:18:08 → 74.67% em 00:00:22:27 (linear).
- [ ] #4 MVI_0598: Scale 66.67% em 00:00:22:28 → 74.67% em 00:00:31:23 (linear).
- [ ] #6 MVI_0589: Scale 66.67% em 00:00:37:01 → 74.67% em 00:00:40:04 (linear).
- Se os keyframes não vierem no import, crie os dois keyframes de Scale à mão com esses valores (Effect Controls → Motion → Scale).

## 4. Áudio
- [ ] A1 (fala): ganho por clipe já no XML (Audio Levels/Clip Volume) para igualar as vozes:
      #1 +0.8 dB, #2 +0.8 dB, #3 +10.8 dB, #4 +3.7 dB, #5 -0.4 dB, #6 -3.6 dB, #7 +2.4 dB. O #3 (MVI_0587) foi gravado baixo: confira se não ficou com ruído.
- [ ] A2 (música): no XML está fixa em **-26 dB** (nível sob a fala). Suba para **-16 dB** nas pausas sem fala
      (com rampas de ~0,15 s), como na prévia:
      - 00:00:12:28 → 00:00:13:17
      - 00:00:18:00 → 00:00:18:08
      - 00:00:31:12 → 00:00:31:24
      - 00:00:36:12 → 00:00:37:01
      - 00:00:42:10 → 00:00:43:09
      (Alternativa: Essential Sound → música como *Music* com **Ducking** ativado em relação ao *Dialogue*.)
- [ ] Fade-out da música: Cross Fade de 1.5 s em 00:00:41:24 → 00:00:43:09. Se não vier, faça com keyframes de volume.
- [ ] Música começa em 49.667 s da faixa (XML: quadro 1490 = 49.667 s, diferença de 0 ms).

## 5. Transições e fim
- Cortes secos na batida entre os depoimentos (como na referência, que corta a cada troca de pessoa).
- [ ] Fade para preto no fim: 00:00:42:24 → 00:00:43:09.

## 6. Velocidade / textos
- Nenhuma alteração de velocidade. Sem texto na tela e sem legenda (decisão confirmada), por isso não há .srt.

## 7. Cor (não vai no XML)
- [ ] Material noturno e quente. Lumetri leve na sequência toda (exposição/contraste e tons de pele); os mais escuros são o #3 (MVI_0587, brilho médio 42/255) e o #6 (MVI_0589, 43/255); o mais claro é o #5 (MVI_0586, 76/255). Iguale a exposição entre eles.
