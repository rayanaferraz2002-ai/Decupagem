# Relatório — Recap evento 19/11 (1 ano T.T. Macaé)

## Material recebido e como interpretei
O Drive não tinha a estrutura `roteiro/ referencia/ musica/ clipes/ locucao/`. Identifiquei assim:

| Origem no Drive | Arquivo | Interpretação |
|---|---|---|
| Recap Evento 19/11 | 78 × `MVI_xxxx.MP4` (1920×1080, 23,976 fps, H.264, ~2,2 GB) | **clipes/** (brutos) |
| Recap Niver T.T | `Bring It (Instrumental).mp4` (só áudio AAC, 3:16) | **musica/** |
| Recap Niver T.T | `helloweddingpro_pindown.io_1795696906.mp4` (720×1280, 30 fps, 43,8 s) | **referencia/** |
| — | (nenhum) | **roteiro/**: veio só no texto do pedido, sem decupagem cena a cena |
| — | (nenhum) | **locucao/**: não há, então a edição não tem trilha de locução |

Acesso: o `gdown` foi bloqueado pelo proxy do ambiente. Liberei `drive.google.com`, `drive.usercontent.google.com` e `docs.google.com`
no ambiente e baixei por `drive.usercontent.google.com` (o gdown redireciona para hosts dinâmicos `*.googleusercontent.com`, que não são liberáveis). Todos os 78 clipes foram conferidos por tamanho.
Os originais ficaram somente leitura. Todo o trabalho foi feito em cópias (proxies 720p).

**Achado importante:** os clipes foram gravados com a câmera em pé, mas estão salvos deitados (1920×1080, sem metadado de rotação),
uns girados para um lado e outros para o outro. Classifiquei os 78 clipes um a um (`dados/orientacao.json`): 32 giram 90° no sentido horário, 45 giram 90° no anti-horário e 1 foi descartado.

## Passo 1 — Roteiro
O roteiro traz objetivo, direção e mensagem, mas não traz cenas, durações, efeitos nem texto. **Perguntei e você confirmou:**
estrutura derivada da direção, **sem texto na tela** e **~44 s com a música a partir de 0:15**.

| Cena/bloco | Direção de imagem | Direção de edição | Duração | Áudio |
|---|---|---|---|---|
| 1. Abertura – casa cheia | fachada T.T. Burger, varanda e salão lotados | 1º plano no build (4 batidas), depois cortes a cada 2 batidas a partir do drop | 0:00–0:07,96 (16 batidas) | música (drop em 0:01,97) |
| 2. Gente e clima | rostos, sorrisos, amigos, equipe, atendimento | cortes a cada 2 batidas, sem repetir clipe | 0:07,96–0:17,97 (20 batidas) | música (alta energia) |
| 3. Burger | cozinha, bandeja, gente comendo | entra com fusão; planos mais longos (4 batidas) no respiro da música | 0:17,97–0:31,93 (28 batidas) | música (parte baixa) |
| 4. Comemoração | roleta de prêmios, brinde "1 ano de T.T.", máquina de garra, risadas | fusão na entrada; 2 batidas, 2 cortes de 1 batida antes do drop final | 0:31,93–0:39,96 (16 batidas) | música (subida + drop em 0:35,97) |
| 5. Fechamento | letreiro T.T.BURGER sobre a multidão | 4 batidas cada, fade para preto | 0:39,96–0:43,96 (8 batidas) | fade-out de 2 s |

Mensagem central ("1 ano de T.T. Macaé em uma noite / obrigado") é passada só por imagem: abre e fecha no letreiro, e a sacola "1 ano de T.T." aparece no bloco 4.

## Passo 2 — Referência (só estilo)
- 43,8 s, **9:16, 720×1280, 30 fps**.
- 48 planos, **média de 0,91 s** (mín. 0,60 s, máx. 1,90 s). Cortes detectados com PySceneDetect (`dados/referencia_cenas.csv`).
- Áudio da referência a ~92 BPM (batida de 0,65 s): a maioria dos cortes cai **a cada 1 batida**, alguns a cada 2.
- Ritmo: abre com 2 planos de ~1,3 s, faz uma sequência rápida (~0,65 s) até ~19 s, alonga no meio (1–1,8 s, 20–35 s), acelera de novo e fecha num plano longo.
- Transições: cortes secos. Estilo: câmera na mão, gente sorrindo, detalhes da festa, legendas palavra por palavra (não usadas: você pediu sem texto).

## Passo 3 — Música (`dados/mapa_batidas_musica.json`)
- Duração 3:16. **Andamento ~120 BPM**: o intervalo médio entre batidas é 0,500 s (o librosa estimou 117,45 BPM no global, mas as batidas detectadas estão a 0,500 s ± 0,012).
- Frases de 8 compassos (~16 s). Seções de energia:
  intro baixa 0:01–0:17 · subida 0:17–0:21 · **clímax 0:21–0:29** · alto 0:29–0:33 · baixo 0:33–0:49 · subida 0:49–0:53 · **clímax 0:53–1:01** · alto 1:01–1:15 · clímax 1:15–1:19 · baixo 1:23–1:35 · **clímax 1:41–2:05** · baixo 2:09–2:25 · clímax 2:29–2:37 · clímax 2:51–2:57 · final baixo 3:01–3:09.
- **Trecho usado: 0:15,116 → 0:59,08 (88 batidas = 22 compassos = 43,97 s).** Edição: build 0–1,97 s → **drop 1,97 s** → respiro 17,97–31,93 s → subida → **drop 35,97 s** → fade.
- Na edição, a batida vem a cada 15 quadros (30 fps). Erro máximo entre corte e batida: **16 ms** (meio quadro).

## Passo 4 — Escolha dos trechos
Proxies 720p → métricas a 8 quadros/s (nitidez pela variância do Laplaciano, tremor por phaseCorrelate, brilho) + folhas de contato já giradas.
Escolhi o clipe e a janela de cada plano olhando as imagens (`dados/escolhas.json`). Dentro da janela, o script pega o trecho mais nítido, com menos tremor e boa exposição.
Revisei os quadros escolhidos e troquei 2: #8 MVI_0323 (estava tremido, movi a janela) e #33 MVI_0720 (desfocado, troquei por MVI_0581).
Nenhum clipe se repete. Em todas as cenas havia material adequado.

## Cena → clipe escolhido
| # | Bloco | Timeline (entrada) | Dur. | Batidas | Arquivo original | Entrada → saída no original | Rotação | Transição | Motivo |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 1. Abertura - casa cheia | 00:00:00:00 | 1.97s | 4 | MVI_0718.MP4 | 15.25s → 17.22s (00:15:06 → 00:17:05) | 90° horário | corte | fachada com letreiro T.T.BURGER e varanda lotada; abre no build antes do drop |
| 2 | 1. Abertura - casa cheia | 00:00:01:29 | 1.00s | 2 | MVI_0549.MP4 | 3.00s → 4.00s (00:03:00 → 00:04:00) | 90° horário | corte | letreiro T.T BURGER + salão externo lotado, plano mais nítido do lote (cai no drop) |
| 3 | 1. Abertura - casa cheia | 00:00:02:29 | 1.00s | 2 | MVI_0668.MP4 | 0.20s → 1.20s (00:00:05 → 00:01:05) | 90° horário | corte | multidão em pé na área externa |
| 4 | 1. Abertura - casa cheia | 00:00:03:29 | 1.00s | 2 | MVI_0719.MP4 | 1.50s → 2.50s (00:01:12 → 00:02:12) | 90° horário | corte | fachada frontal com mesas cheias, estável |
| 5 | 1. Abertura - casa cheia | 00:00:04:29 | 1.00s | 2 | MVI_0578.MP4 | 0.20s → 1.20s (00:00:05 → 00:01:05) | 90° horário | corte | público sentado entre balões |
| 6 | 1. Abertura - casa cheia | 00:00:05:29 | 1.00s | 2 | MVI_0696.MP4 | 0.20s → 1.20s (00:00:05 → 00:01:05) | 90° horário | corte | salão interno cheio, gente conversando |
| 7 | 1. Abertura - casa cheia | 00:00:06:29 | 1.00s | 2 | MVI_0320.MP4 | 3.00s → 4.00s (00:03:00 → 00:04:00) | 90° horário | corte | mesas externas ocupadas, nítido |
| 8 | 2. Gente e clima | 00:00:07:29 | 1.00s | 2 | MVI_0323.MP4 | 5.00s → 6.00s (00:05:00 → 00:06:00) | 90° horário | corte | cliente sorrindo para a câmera |
| 9 | 2. Gente e clima | 00:00:08:29 | 1.00s | 2 | MVI_0697.MP4 | 0.00s → 1.00s (00:00:00 → 00:01:00) | 90° horário | corte | amigas na festa, rosto em foco |
| 10 | 2. Gente e clima | 00:00:09:29 | 1.00s | 2 | MVI_0333.MP4 | 0.20s → 1.20s (00:00:05 → 00:01:05) | 90° horário | corte | amigas conversando com o salão cheio ao fundo |
| 11 | 2. Gente e clima | 00:00:10:29 | 1.00s | 2 | MVI_0552.MP4 | 4.95s → 5.95s (00:04:23 → 00:05:23) | 90° horário | corte | equipe 'Sorrisos são virais' com a roleta |
| 12 | 2. Gente e clima | 00:00:11:29 | 1.00s | 2 | MVI_0331.MP4 | 0.95s → 1.95s (00:00:23 → 00:01:23) | 90° horário | corte | atendimento na mesa |
| 13 | 2. Gente e clima | 00:00:12:29 | 1.00s | 2 | MVI_0554.MP4 | 1.50s → 2.50s (00:01:12 → 00:02:12) | 90° horário | corte | família/criança na mesa |
| 14 | 2. Gente e clima | 00:00:13:29 | 1.00s | 2 | MVI_0326.MP4 | 4.12s → 5.12s (00:04:03 → 00:05:03) | 90° horário | corte | mesa com mural da marca ao fundo |
| 15 | 2. Gente e clima | 00:00:14:29 | 1.00s | 2 | MVI_0339.MP4 | 0.20s → 1.20s (00:00:05 → 00:01:05) | 90° horário | corte | grupo conversando na área externa |
| 16 | 2. Gente e clima | 00:00:15:29 | 1.00s | 2 | MVI_0582.MP4 | 1.57s → 2.58s (00:01:14 → 00:02:14) | 90° anti-horário | corte | cliente sorrindo |
| 17 | 2. Gente e clima | 00:00:16:29 | 1.00s | 2 | MVI_0544.MP4 | 14.12s → 15.12s (00:14:03 → 00:15:03) | 90° anti-horário | corte | amigas dançando - energia antes de baixar o ritmo |
| 18 | 3. Burger | 00:00:17:29 | 2.03s | 4 | MVI_0597.MP4 | 2.40s → 4.43s (00:02:10 → 00:04:10) | 90° anti-horário | dissolve | cozinha montando o burger |
| 19 | 3. Burger | 00:00:20:00 | 1.97s | 4 | MVI_0710.MP4 | 0.20s → 2.17s (00:00:05 → 00:02:04) | 90° horário | corte | close da bandeja com burger e fritas |
| 20 | 3. Burger | 00:00:21:29 | 2.00s | 4 | MVI_0711.MP4 | 7.25s → 9.25s (00:07:06 → 00:09:06) | 90° horário | corte | cliente mordendo o burger |
| 21 | 3. Burger | 00:00:23:29 | 2.00s | 4 | MVI_0610.MP4 | 0.20s → 2.20s (00:00:05 → 00:02:05) | 90° horário | corte | cliente sorrindo com o burger na mão |
| 22 | 3. Burger | 00:00:25:29 | 2.00s | 4 | MVI_0656.MP4 | 0.20s → 2.20s (00:00:05 → 00:02:05) | 90° anti-horário | corte | cliente comendo, mesa com bandejas e latas |
| 23 | 3. Burger | 00:00:27:29 | 2.00s | 4 | MVI_0324.MP4 | 0.20s → 2.20s (00:00:05 → 00:02:05) | 90° horário | corte | cliente comendo burger na área externa |
| 24 | 3. Burger | 00:00:29:29 | 1.97s | 4 | MVI_0551.MP4 | 3.58s → 5.54s (00:03:14 → 00:05:13) | 90° horário | corte | salão interno cheio, mesas comendo (fecha o bloco ligando burger e casa cheia) |
| 25 | 4. Comemoração | 00:00:31:28 | 1.03s | 2 | MVI_0547.MP4 | 9.82s → 10.86s (00:09:20 → 00:10:20) | 90° anti-horário | dissolve | roleta de prêmios girando |
| 26 | 4. Comemoração | 00:00:32:29 | 1.00s | 2 | MVI_0553.MP4 | 0.00s → 1.00s (00:00:00 → 00:01:00) | 90° horário | corte | brinde com sacola '1 ano de T.T.' |
| 27 | 4. Comemoração | 00:00:33:29 | 1.00s | 2 | MVI_0722.MP4 | 1.57s → 2.58s (00:01:14 → 00:02:14) | 90° horário | corte | máquina de garra com ketchups |
| 28 | 4. Comemoração | 00:00:34:29 | 0.50s | 1 | MVI_0557.MP4 | 14.50s → 15.00s (00:14:12 → 00:15:00) | 90° anti-horário | corte | roleta girando (close, corte rápido antes do drop) |
| 29 | 4. Comemoração | 00:00:35:14 | 0.50s | 1 | MVI_0558.MP4 | 1.45s → 1.95s (00:01:11 → 00:01:23) | 90° horário | corte | placa de premiações |
| 30 | 4. Comemoração | 00:00:35:29 | 1.00s | 2 | MVI_0571.MP4 | 24.00s → 25.00s (00:23:23 → 00:24:23) | 90° anti-horário | corte | cliente rindo/comemorando (no drop final) |
| 31 | 4. Comemoração | 00:00:36:29 | 1.00s | 2 | MVI_0723.MP4 | 15.50s → 16.50s (00:15:12 → 00:16:12) | 90° horário | corte | cliente rindo na máquina de garra |
| 32 | 4. Comemoração | 00:00:37:29 | 1.00s | 2 | MVI_0580.MP4 | 0.82s → 1.82s (00:00:20 → 00:01:20) | 90° anti-horário | corte | amigas juntas sorrindo |
| 33 | 4. Comemoração | 00:00:38:29 | 1.00s | 2 | MVI_0581.MP4 | 25.75s → 26.75s (00:25:17 → 00:26:17) | 90° anti-horário | corte | cliente sorrindo/rindo, rosto nítido (substitui MVI_0720, desfocado) |
| 34 | 5. Fechamento | 00:00:39:29 | 2.00s | 4 | MVI_0579.MP4 | 2.88s → 4.88s (00:02:21 → 00:04:21) | 90° horário | corte | rua/fila com letreiro T.T.BURGER |
| 35 | 5. Fechamento | 00:00:41:29 | 2.00s | 4 | MVI_0713.MP4 | 0.20s → 2.20s (00:00:05 → 00:02:05) | 90° anti-horário | corte + fade p/ preto | letreiro T.T.BURGER sobre a multidão - assinatura final com fade |

(Entrada/saída em segundos do original; entre parênteses, mm:ss:qq a 23,976 fps.)

## Descartados (motivo)
- **Inutilizável:** MVI_0577 (parede desfocada, sem assunto).
- **Desfocado/tremido:** 0322, 0329, 0337, 0542, 0543, 0546, 0583, 0708, 0717, 0720, 0721.
- **Escuro ou contraluz:** 0338, 0611, 0699, 0700, 0701, 0715.
- **Rosto encoberto ou enquadramento confuso:** 0321 (rosto cortado em 1º plano), 0596 (bancada com roleta, leitura confusa), 0704, 0705, 0706, 0707 (mão na frente), 0709, 0712, 0714 (vista de cima).
- **Redundante com plano melhor já usado:** 0325 e 0330 (funcionário no balcão), 0328 (cliente de costas no totem), 0545 (≈0544), 0548 (≈0547/0552), 0550 (salão visto de fora, mesma ideia de 0551), 0555 (≈0553, mesma pessoa), 0556 (≈0557), 0576 (≈0578, mesmo rapaz), 0584 (≈0713 letreiro), 0716.
- **Destaque de outra marca vizinha (Mabros) como assunto principal:** 0591, 0698 (evitei dar protagonismo).
- **Boas alternativas para trocas:** MVI_0332 (casal comendo, nítido) e MVI_0327 (detalhe do ketchup) para o bloco Burger; MVI_0541 (chope sendo tirado) para detalhe; MVI_0555 (brinde) para Comemoração; MVI_0576 para casa cheia.

## Premissas e decisões
1. Sem decupagem no roteiro: estrutura em 5 blocos derivada da direção (**confirmado por você**).
2. Sem texto na tela (**confirmado**), por isso não há .srt.
3. 43,97 s, 720×1280, 30 fps, igual à referência; música a partir de 0:15,116 (**confirmado**).
4. Cortes: 2 batidas (1,0 s) nos trechos de energia, 4 batidas (2,0 s) no respiro e no começo/fim, 1 batida em dois cortes antes do drop final. É um pouco mais lento que a referência (média 1,26 s × 0,91 s): a música é mais rápida (120 × 92 BPM), e 1 batida aqui (0,5 s) ficaria picotado demais para material noturno.
5. Clímax da música alinhado com o maior impacto: casa cheia no 1º drop; risadas e comemoração no 2º.
6. Fusões curtas (8 quadros) só nas viradas de bloco que coincidem com mudança de energia da música (entrada do Burger e da Comemoração). O resto é corte seco, como na referência.
7. Áudio de câmera não usado. Não há locução.
8. A sequência é 720×1280 (referência). Os originais em pé têm 1080×1920: veja a dica no checklist para exportar em resolução cheia.
9. A prévia foi renderizada a partir dos proxies 720p (por isso é leve). O XML aponta para os **originais** pelo nome.
10. No XML a música começa no quadro 453 (15,100 s) em vez de 15,116 s, por arredondamento de quadro (16 ms).

## Validação do XML
`scripts/validar_xml.py`: XML bem formado (xmllint), sequência 720×1280@30, 35 clipes contíguos sem buracos nem sobreposição, in/out dentro de cada mídia, arquivos originais existem pelo nome, música cobre a sequência.
Leitura independente com OpenTimelineIO (adapter FCP XML): 2 trilhas, 35 clipes, 1319 quadros @ 30. **Não testei dentro do Premiere** (não está disponível aqui). O ponto mais sensível é o sinal da rotação: veja o checklist.
