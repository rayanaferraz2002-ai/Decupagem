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

## Versão 2 — alteração pedida
Pedido: abrir com a placa do T.T. Burger, em seguida um **mosaico como o da referência** com um preview de tudo o que aconteceu,
e depois pessoas comendo → chopp → comida → cerveja → pessoas rindo. A música, a duração (43,97 s), o formato e os cortes na batida continuam os mesmos.

## Passo 1 — Roteiro (estrutura atual)
| Bloco | Direção de imagem | Direção de edição | Tempo (batidas) | Áudio |
|---|---|---|---|---|
| 1. Placa T.T. Burger | placa redonda T.T.BURGER acesa sobre a multidão (MVI_0713) | plano único no build | 0:00–0:01,97 (4) | música, antes do drop |
| 2. Mosaico (preview) | casa cheia, fachada, DJ, equipe, roleta, máquina de garra, brinde "1 ano", telas, público | entra no drop em tela cheia; na batida seguinte vira 3 faixas; depois troca 1 faixa por batida (topo → base → meio); 17 painéis | 0:01,97–0:09,96 (16) | clímax |
| 3. Pessoas comendo | clientes mordendo e segurando o burger | corte a cada 2 batidas | 0:09,96–0:17,97 (16) | clímax |
| 4. Chopp | chopp sendo tirado na chopeira | entra com fusão; 4 batidas por plano | 0:17,97–0:21,97 (8) | respiro |
| 5. Comida | cozinha, bandeja com burger e fritas | 4 batidas | 0:21,97–0:27,98 (12) | respiro |
| 6. Cerveja | mesas com copos, cliente bebendo | 4 + 4 + 2 + 2 batidas | 0:27,98–0:33,97 (12) | respiro → subida |
| 7. Risadas | clientes e equipe rindo, amigas dançando | 2 batidas, drop final em 0:35,97, último plano com 4 e fade | 0:33,97–0:43,96 (20) | subida → clímax → fade-out |

**Como o mosaico funciona:** são 3 faixas iguais (topo/meio/base, 1/3 da altura cada). Cada painel mostra **o terço do próprio clipe** em que
o assunto já está (escolhi os clipes por isso): a placa no alto, o público embaixo etc. Assim não é preciso reposicionar nada.
No Premiere isso é só **Crop**, porque o parâmetro de posição (Center) do XML do FCP7 não tem a escala bem documentada
e poderia deslocar os painéis. Faixa do meio = V1, topo = V2, base = V3.

## Passo 2 — Referência (só estilo)
- 43,8 s, **9:16, 720×1280, 30 fps**.
- 48 planos, **média de 0,91 s** (mín. 0,60 s, máx. 1,90 s). Cortes detectados com PySceneDetect (`dados/referencia_cenas.csv`).
- Áudio da referência a ~92 BPM (batida de 0,65 s): a maioria dos cortes cai **a cada 1 batida**, alguns a cada 2.
- Ritmo: abre com 2 planos de ~1,3 s, faz uma sequência rápida (~0,65 s) até ~19 s, alonga no meio (1–1,8 s, 20–35 s), acelera de novo e fecha num plano longo.
- Por volta de 2,7–5,3 s a referência faz um **mosaico de 3 faixas horizontais**: a cada batida entra um vídeo novo numa faixa, como um resumo rápido do evento.
- Transições: cortes secos. Estilo: câmera na mão, gente sorrindo, detalhes da festa, legendas palavra por palavra (não usadas: você pediu sem texto).

## Passo 3 — Música (`dados/mapa_batidas_musica.json`)
- Duração 3:16. **Andamento ~120 BPM**: o intervalo médio entre batidas é 0,500 s (o librosa estimou 117,45 BPM no global, mas as batidas detectadas estão a 0,500 s ± 0,012).
- Frases de 8 compassos (~16 s). Seções de energia:
  intro baixa 0:01–0:17 · subida 0:17–0:21 · **clímax 0:21–0:29** · alto 0:29–0:33 · baixo 0:33–0:49 · subida 0:49–0:53 · **clímax 0:53–1:01** · alto 1:01–1:15 · clímax 1:15–1:19 · baixo 1:23–1:35 · **clímax 1:41–2:05** · baixo 2:09–2:25 · clímax 2:29–2:37 · clímax 2:51–2:57 · final baixo 3:01–3:09.
- **Trecho usado: 0:15,116 → 0:59,08 (88 batidas = 22 compassos = 43,97 s).** Edição: placa no build 0–1,97 s → **drop 1,97 s = mosaico** → comendo → respiro 17,97–31,93 s (chopp, comida, cerveja) → subida → **drop 35,97 s = risadas** → fade.
- Na edição, a batida vem a cada 15 quadros (30 fps). Erro máximo entre corte e batida: **16 ms** (meio quadro).

## Passo 4 — Escolha dos trechos
Mesmo método: métricas de nitidez, tremor e brilho nos proxies, folhas de contato já giradas, janela escolhida à mão e
melhor trecho dentro dela escolhido pelo script. No mosaico, conferi quadro a quadro com linhas dos terços e troquei 4 painéis:
MVI_0330 (só guarda-sol no terço de cima) → MVI_0718 (letreiro), MVI_0558 (borrado no terço de baixo) → MVI_0333,
MVI_0576 (1,08 s, curto demais para o painel de 1,5 s) → MVI_0339, e o último painel de baixo → MVI_0696.
Também conferi automaticamente que nenhuma faixa fica preta em nenhum quadro do mosaico.

**Repetições:** MVI_0549 aparece em tela cheia e segue na faixa do meio (é o mesmo trecho contínuo). MVI_0723 aparece no mosaico
(topo da máquina de garra, 3,4 s) e de novo nas risadas (cliente rindo, 15,5 s): são momentos diferentes, e não havia outro plano de risada tão bom.

## Cena → clipe escolhido
| # | Bloco | Timeline (entrada) | Dur. | Trilha / faixa | Arquivo original | Entrada → saída no original | Rotação | Transição | Motivo |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 1. Placa T.T. Burger | 00:00:00:00 | 1.97s | V1 tela cheia | MVI_0713.MP4 | 0.20s → 2.17s (00:00:05 → 00:02:04) | 90° anti-horário | corte | placa redonda T.T.BURGER acesa sobre a multidão; abre no build antes do drop |
| 2 | 2. Mosaico - preview do evento | 00:00:01:29 | 0.50s | V1 tela cheia | MVI_0549.MP4 | 3.00s → 3.50s (00:03:00 → 00:03:12) | 90° horário | corte | casa cheia com letreiro (tela cheia no drop, depois segue na faixa do meio) [tela cheia] |
| 3 | 2. Mosaico - preview do evento | 00:00:02:14 | 1.50s | V1 meio | MVI_0549.MP4 | 3.50s → 5.00s (00:03:12 → 00:05:00) | 90° horário | corte | casa cheia com letreiro (tela cheia no drop, depois segue na faixa do meio) [faixa do meio] |
| 4 | 2. Mosaico - preview do evento | 00:00:02:14 | 0.50s | V2 topo | MVI_0719.MP4 | 1.50s → 2.00s (00:01:12 → 00:02:00) | 90° horário | corte | letreiro BURGER da fachada |
| 5 | 2. Mosaico - preview do evento | 00:00:02:14 | 1.00s | V3 base | MVI_0321.MP4 | 2.80s → 3.80s (00:02:19 → 00:03:19) | 90° anti-horário | corte | DJ / pick-ups |
| 6 | 2. Mosaico - preview do evento | 00:00:02:29 | 1.50s | V2 topo | MVI_0718.MP4 | 15.75s → 17.25s (00:15:18 → 00:17:06) | 90° horário | corte | letreiro T.T.BURGER da fachada |
| 7 | 2. Mosaico - preview do evento | 00:00:03:14 | 1.50s | V3 base | MVI_0722.MP4 | 1.43s → 2.92s (00:01:10 → 00:02:22) | 90° horário | corte | máquina de garra cheia de ketchups |
| 8 | 2. Mosaico - preview do evento | 00:00:03:29 | 1.50s | V1 meio | MVI_0547.MP4 | 9.00s → 10.50s (00:09:00 → 00:10:12) | 90° anti-horário | corte | roleta de prêmios com a equipe |
| 9 | 2. Mosaico - preview do evento | 00:00:04:14 | 1.50s | V2 topo | MVI_0578.MP4 | 8.00s → 9.50s (00:08:00 → 00:09:12) | 90° horário | corte | placa T.T.BURGER no alto da rua lotada |
| 10 | 2. Mosaico - preview do evento | 00:00:04:29 | 1.50s | V3 base | MVI_0333.MP4 | 0.20s → 1.70s (00:00:05 → 00:01:17) | 90° horário | corte | mesas e público no salão |
| 11 | 2. Mosaico - preview do evento | 00:00:05:14 | 1.50s | V1 meio | MVI_0553.MP4 | 0.20s → 1.70s (00:00:05 → 00:01:17) | 90° horário | corte | brinde com a sacola '1 ano de T.T.' |
| 12 | 2. Mosaico - preview do evento | 00:00:05:29 | 1.50s | V2 topo | MVI_0723.MP4 | 3.38s → 4.88s (00:03:09 → 00:04:21) | 90° horário | corte | topo da máquina de garra |
| 13 | 2. Mosaico - preview do evento | 00:00:06:14 | 1.50s | V3 base | MVI_0339.MP4 | 0.20s → 1.70s (00:00:05 → 00:01:17) | 90° horário | corte | grupo conversando (substitui MVI_0576, curto demais) |
| 14 | 2. Mosaico - preview do evento | 00:00:06:29 | 1.50s | V1 meio | MVI_0557.MP4 | 10.50s → 12.00s (00:10:12 → 00:12:00) | 90° anti-horário | corte | roleta girando |
| 15 | 2. Mosaico - preview do evento | 00:00:07:14 | 1.50s | V2 topo | MVI_0328.MP4 | 1.07s → 2.58s (00:01:02 → 00:02:14) | 90° horário | corte | telas e totem de pedido |
| 16 | 2. Mosaico - preview do evento | 00:00:07:29 | 1.50s | V3 base | MVI_0320.MP4 | 3.00s → 4.50s (00:03:00 → 00:04:12) | 90° horário | corte | mesas externas ocupadas |
| 17 | 2. Mosaico - preview do evento | 00:00:08:14 | 1.50s | V1 meio | MVI_0668.MP4 | 1.00s → 2.50s (00:01:00 → 00:02:12) | 90° horário | corte | multidão em pé |
| 18 | 2. Mosaico - preview do evento | 00:00:08:29 | 1.00s | V2 topo | MVI_0325.MP4 | 0.45s → 1.45s (00:00:11 → 00:01:11) | 90° horário | corte | atendente sob o guarda-sol |
| 19 | 2. Mosaico - preview do evento | 00:00:09:14 | 0.50s | V3 base | MVI_0696.MP4 | 0.50s → 1.00s (00:00:12 → 00:01:00) | 90° horário | corte | gente conversando no salão |
| 20 | 3. Pessoas comendo | 00:00:09:29 | 1.00s | V1 tela cheia | MVI_0711.MP4 | 7.25s → 8.25s (00:07:06 → 00:08:06) | 90° horário | corte | cliente mordendo o burger |
| 21 | 3. Pessoas comendo | 00:00:10:29 | 1.00s | V1 tela cheia | MVI_0610.MP4 | 1.20s → 2.20s (00:01:05 → 00:02:05) | 90° horário | corte | cliente sorrindo com o burger na mão |
| 22 | 3. Pessoas comendo | 00:00:11:29 | 1.00s | V1 tela cheia | MVI_0324.MP4 | 0.20s → 1.20s (00:00:05 → 00:01:05) | 90° horário | corte | cliente comendo na área externa |
| 23 | 3. Pessoas comendo | 00:00:12:29 | 1.00s | V1 tela cheia | MVI_0332.MP4 | 0.20s → 1.20s (00:00:05 → 00:01:05) | 90° horário | corte | casal comendo |
| 24 | 3. Pessoas comendo | 00:00:13:29 | 1.00s | V1 tela cheia | MVI_0717.MP4 | 2.45s → 3.45s (00:02:11 → 00:03:11) | 90° anti-horário | corte | cliente comendo, mesa com ketchup e latas |
| 25 | 3. Pessoas comendo | 00:00:14:29 | 1.00s | V1 tela cheia | MVI_0709.MP4 | 1.05s → 2.05s (00:01:01 → 00:02:01) | 90° anti-horário | corte | grupo comendo |
| 26 | 3. Pessoas comendo | 00:00:15:29 | 1.00s | V1 tela cheia | MVI_0656.MP4 | 0.20s → 1.20s (00:00:05 → 00:01:05) | 90° anti-horário | corte | cliente comendo, bandejas na mesa |
| 27 | 3. Pessoas comendo | 00:00:16:29 | 1.00s | V1 tela cheia | MVI_0704.MP4 | 4.17s → 5.17s (00:04:04 → 00:05:04) | 90° anti-horário | corte | cliente comendo com chopp na mesa |
| 28 | 4. Chopp | 00:00:17:29 | 2.03s | V1 tela cheia | MVI_0541.MP4 | 0.45s → 2.48s (00:00:11 → 00:02:12) | 90° anti-horário | dissolve | chopp sendo tirado na torneira |
| 29 | 4. Chopp | 00:00:20:00 | 1.97s | V1 tela cheia | MVI_0542.MP4 | 0.30s → 2.27s (00:00:07 → 00:02:06) | 90° anti-horário | corte | copo enchendo na chopeira |
| 30 | 5. Comida | 00:00:21:29 | 2.00s | V1 tela cheia | MVI_0597.MP4 | 2.40s → 4.40s (00:02:10 → 00:04:09) | 90° anti-horário | corte | cozinha montando o burger |
| 31 | 5. Comida | 00:00:23:29 | 2.00s | V1 tela cheia | MVI_0710.MP4 | 0.20s → 2.20s (00:00:05 → 00:02:05) | 90° horário | corte | close da bandeja com burger e fritas |
| 32 | 5. Comida | 00:00:25:29 | 2.00s | V1 tela cheia | MVI_0596.MP4 | 16.50s → 18.50s (00:16:12 → 00:18:12) | 90° anti-horário | corte | bandeja com fritas, ketchup e lata |
| 33 | 6. Cerveja | 00:00:27:29 | 2.00s | V1 tela cheia | MVI_0543.MP4 | 5.25s → 7.25s (00:05:06 → 00:07:06) | 90° anti-horário | corte | mesa com copos de chopp, amigos conversando |
| 34 | 6. Cerveja | 00:00:29:29 | 1.97s | V1 tela cheia | MVI_0705.MP4 | 1.62s → 3.59s (00:01:15 → 00:03:14) | 90° anti-horário | corte | cliente bebendo |
| 35 | 6. Cerveja | 00:00:31:28 | 1.03s | V1 tela cheia | MVI_0331.MP4 | 0.95s → 1.98s (00:00:23 → 00:02:00) | 90° horário | corte | mesa com copos de cerveja sendo servida |
| 36 | 6. Cerveja | 00:00:32:29 | 1.00s | V1 tela cheia | MVI_0551.MP4 | 3.58s → 4.58s (00:03:14 → 00:04:14) | 90° horário | corte | salão interno cheio, mesas com bebida |
| 37 | 7. Risadas | 00:00:33:29 | 1.00s | V1 tela cheia | MVI_0582.MP4 | 1.57s → 2.58s (00:01:14 → 00:02:14) | 90° anti-horário | corte | cliente sorrindo |
| 38 | 7. Risadas | 00:00:34:29 | 1.00s | V1 tela cheia | MVI_0323.MP4 | 5.00s → 6.00s (00:05:00 → 00:06:00) | 90° horário | corte | cliente sorrindo para a câmera |
| 39 | 7. Risadas | 00:00:35:29 | 1.00s | V1 tela cheia | MVI_0571.MP4 | 24.00s → 25.00s (00:23:23 → 00:24:23) | 90° anti-horário | corte | cliente rindo (no drop final) |
| 40 | 7. Risadas | 00:00:36:29 | 1.00s | V1 tela cheia | MVI_0723.MP4 | 15.50s → 16.50s (00:15:12 → 00:16:12) | 90° horário | corte | cliente rindo na máquina de garra |
| 41 | 7. Risadas | 00:00:37:29 | 1.00s | V1 tela cheia | MVI_0581.MP4 | 25.75s → 26.75s (00:25:17 → 00:26:17) | 90° anti-horário | corte | cliente rindo |
| 42 | 7. Risadas | 00:00:38:29 | 1.00s | V1 tela cheia | MVI_0555.MP4 | 3.00s → 4.00s (00:03:00 → 00:04:00) | 90° horário | corte | equipe rindo |
| 43 | 7. Risadas | 00:00:39:29 | 1.00s | V1 tela cheia | MVI_0580.MP4 | 0.82s → 1.82s (00:00:20 → 00:01:20) | 90° anti-horário | corte | amigas juntas sorrindo |
| 44 | 7. Risadas | 00:00:40:29 | 1.00s | V1 tela cheia | MVI_0697.MP4 | 0.00s → 1.00s (00:00:00 → 00:01:00) | 90° horário | corte | amigas na festa |
| 45 | 7. Risadas | 00:00:41:29 | 2.00s | V1 tela cheia | MVI_0544.MP4 | 13.62s → 15.62s (00:13:15 → 00:15:15) | 90° anti-horário | corte + fade p/ preto | amigas dançando e rindo - fecha com fade |

(Entrada/saída em segundos do original; entre parênteses, mm:ss:qq a 23,976 fps.)

## Descartados (motivo)
- **Inutilizável:** MVI_0577 (parede desfocada).
- **Desfocado/tremido:** 0322, 0329, 0337, 0546, 0583, 0708, 0720, 0721.
- **Escuro ou contraluz:** 0338, 0611, 0699, 0700, 0701, 0715.
- **Rosto encoberto ou enquadramento confuso:** 0706, 0707 (mão na frente), 0712, 0714 (vista de cima).
- **Curto demais para o mosaico:** 0576 (1,08 s).
- **Redundante com plano melhor já usado:** 0326, 0330, 0545 (≈0544), 0548 e 0552 (equipe com a roleta, ≈0547), 0550, 0554, 0556 (≈0557), 0558 (≈0547/0557), 0579, 0584 (placa, ≈0713), 0716, 0327 (ketchup; a comida já tem 3 planos).
- **Outra marca vizinha (Mabros) como assunto principal:** 0591, 0698.

## Premissas e decisões
1. "Placa do TT Burger" = a placa redonda iluminada (MVI_0713). Se você quis dizer o letreiro grande da fachada, troco pelo MVI_0718 ou MVI_0719.
2. O mosaico dura 16 batidas (8 s), mais que o da referência (~2,7 s), porque você pediu um preview de **tudo** o que aconteceu. Dá para encurtar.
3. Ordem dos blocos exatamente como no pedido. O fim agora são as risadas com fade, e não a placa, que foi para a abertura.
4. Chopp, comida e cerveja ficaram no trecho calmo da música (planos de 2 s). As risadas ficaram no drop final.
5. Sem texto na tela, 43,97 s, 720×1280, 30 fps, música a partir de 0:15,116 (confirmado antes).
6. Fusão de 8 quadros só na entrada do chopp (mudança de energia da música). O resto é corte seco na batida.
7. Áudio de câmera não usado. Não há locução.
8. Prévia renderizada a partir dos proxies. O XML aponta para os originais pelo nome.

## Validação do XML
`scripts/validar_xml.py`: XML bem formado (xmllint), sequência 720×1280@30, V1 contígua sem buracos, V2/V3 sem sobreposição,
tempos iguais ao plano, in/out dentro de cada mídia, Crop presente e coerente em cada painel do mosaico, arquivos originais existem pelo nome, música cobre a sequência.
Leitura independente com OpenTimelineIO: 4 trilhas (3 de vídeo + música), 45 clipes de vídeo, 1319 quadros @ 30.
Conferi também que o Crop em coordenadas do original pega o mesmo terço que a prévia (giros horário e anti-horário).
**Não testei dentro do Premiere.** Os pontos sensíveis são o sinal da rotação e a importação do Crop: o checklist traz os valores para aplicar à mão, se precisar.
