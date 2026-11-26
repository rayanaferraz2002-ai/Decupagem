# Relatório — 1 ano T.T. Burger: desejos com velinha

## Material e como interpretei
O Drive não tinha as pastas `direcional/ referencia/ musica/ clipes/ locucao/`. Identifiquei assim:

| Origem no Drive | Arquivo | Interpretação |
|---|---|---|
| pasta de vídeos | 10 × `MVI_0340…0349.MP4` (1920×1080, 23,976 fps, com áudio) | **clipes/**: cada pessoa sentada com um burger com velinha, faz um desejo e sopra |
| pasta de trilha | `Like A Win (Instrumental).mp4` (só áudio, 3:24) | **musica/** |
| pasta de trilha | `snapinsta-1795715222564.mp4` (720×1280, **24 fps**, 47,2 s) | **referencia/** |
| — | — | **direcional/**: veio no texto do pedido |
| — | — | **locucao/**: não há; o áudio de fala é o dos próprios clipes (A1) |

- **Download:** baixei tudo direto do Drive e os originais ficaram somente leitura.
- **Orientação:** os clipes foram gravados em pé e salvos deitados. 0340–0343 giram 90° no sentido anti-horário e 0344–0349 no horário; conferi um a um.
- **0344 e 0345:** baixados, mas não usados (direcional).

## Passo 1 — Direcional
| Cena | Direção de imagem | Direção de edição | Duração | Áudio |
|---|---|---|---|---|
| 1 | close do hambúrguer com a velinha sendo soprada | abre o vídeo | até a vela apagar, fechando na batida | música (som da câmera mudo: alguém fala "Fala!" fora de quadro) |
| 2 | mulher de vermelho falando do ketchup | logo em seguida | até o fim da fala, na batida | fala + música baixa |
| 3+ | demais clipes, à minha escolha, **sem 0344 e 0345** | desejo + sopro quando existir (**confirmado**) | idem | fala + música baixa |

**Confirmado por você:** sem legenda; cada pessoa com desejo + sopro.

**Ordem que escolhi:** 0346 → 0340 → 0341 → 0347 → 0348 → 0349. Alternei homem e mulher e as roupas, para evitar planos parecidos em sequência. Fechei com o desejo da marca ("Eu desejo muito sucesso e muito T.T. trufado!"), o sopro e a comemoração com as mãos, no compasso mais forte da música.

## Passo 2 — Referência (só estilo)
- **Formato:** 47,2 s, **9:16, 720×1280, 24 fps**.
- **Planos:** 11 planos (`dados/referencia_cenas.csv`), média de 4,3 s.
- **Estrutura:** 3 desejos de 4,6–6,0 s ("Eu desejo…", com legenda) diante de um bolo com velas → b-roll do bolo cortado (2,9–3,1 s) → grupo comemorando (3,3–7,5 s) → logo no fim (1,7 s).
- **Transições:** cortes secos.
- **O que não reproduzi:**
  - a legenda, porque você pediu sem;
  - a cartela de logo e o b-roll, porque não há esse material.

## Passo 3 — Música (`dados/mapa_batidas_musica.json`)
- **Andamento:** ~87 BPM (batida a cada 0,69 s; o librosa estimou 86,1 no global). A 1ª batida é em 5,6 s.
- **Energia:** alta e estável de 0:13 a 2:14, vale em 2:20–2:31, de novo alta até 3:12. Compassos mais fortes em 0:29,7 e **1:47,0**.
- **Trecho usado:** 1:05,6 → 1:48,35. O **sopro final do 0349 cai em 1:46,8**, e a comemoração fica dentro do compasso mais forte (1:47,0).
- **Cortes:** todos caem numa batida (erro máximo de 21 ms, meio quadro a 24 fps).

## Passo 4 — Escolha dos trechos
**Como achei os trechos:**
- **Fala:** transcrição local com Whisper. Sem o vocabulário de apoio, porque com ele o modelo "inventava" texto nos clipes sem fala (0343, 0349).
- **Sopro:** localizado vendo os quadros (com tempo exato via ffmpeg −ss) e pela chama da vela.
- **Entradas:** no silêncio antes da 1ª palavra, medido em janelas de 10 ms.
- **Saídas:** na 1ª batida depois do conteúdo, sem invadir fala indesejada. Quando a batida não cabia, a entrada recua para um trecho parado antes da fala (`ini_min`).

**Conferência:** transcrevi a própria prévia plano a plano. As falas entram e saem inteiras.

**Casos particulares:**
- **0343:** começa em 0,85 s, com o close parado do burger, e vai até a vela apagar (~4,1 s). O som da câmera fica mudo, porque havia um "Fala!" fora de quadro e o plano precisava de 3,45 s para fechar na batida.
- **0342:** a mulher de vermelho sopra entre 1,25 e 2,0 s e só depois fala. Como o sopro dela já está no close da abertura, o plano começa logo depois do sopro, já no desejo: "Eu desejo um ano cheio de ketchup e de goiabada."
- **0340 e 0348:** a vela continua acesa até o fim desses clipes, então entram só com o desejo.
- **0348:** cortei o "É pra eu falar, tipo, eu desejo…" e o "Obrigada" do final.
- **0349:** o Whisper ouviu "Eu entendi", mas pelo contexto é "Eu desejo muito sucesso…", no mesmo padrão dos outros.
- **Palavras incertas na transcrição** (não afetam, porque não há legenda): "goiabada" (0342), "Sacode" (0341/0348) e "farta/festa" (0341).

## Cena → clipe escolhido
| # | Cena | Timeline | Dur. | Arquivo original | Entrada → saída no original | Rotação | Zoom | Áudio da câmera | Conteúdo | Motivo |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 1 | 00:00:00:00 | 3.46s | MVI_0343.MP4 | 0.85s → 4.31s (00:00:20 → 00:04:07) | 90° anti-horário | — | mudo | (sem fala: close do burger com a velinha sendo soprada) | direcional: abrir com o close do hambúrguer com a velinha sendo soprada |
| 2 | 2 | 00:00:03:11 | 4.17s | MVI_0342.MP4 | 2.27s → 6.44s (00:02:06 → 00:06:10) | 90° anti-horário | — | +6.4 dB | Eu desejo um ano cheio de ketchup e de goiabada. | direcional: mulher de vermelho falando do ketchup (o sopro dela já aparece no close da abertura) |
| 3 | 3 | 00:00:07:15 | 3.42s | MVI_0346.MP4 | 0.70s → 4.11s (00:00:17 → 00:04:03) | 90° horário | — | +5.8 dB | Eu desejo mais hambúrgueres novos. (sopra) | desejo curto + sopro; quebra com rosto masculino depois de duas cenas da mesma mulher |
| 4 | 4 | 00:00:11:01 | 4.12s | MVI_0340.MP4 | 3.37s → 7.50s (00:03:09 → 00:07:12) | 90° anti-horário | — | +12.0 dB | Eu desejo muito hambúrguer pra todo mundo. | desejo (não sopra no clipe) |
| 5 | 5 | 00:00:15:04 | 11.04s | MVI_0341.MP4 | 2.25s → 13.29s (00:02:06 → 00:13:07) | 90° anti-horário | — | +12.0 dB | (sopra) Seja mais um ano do T.T. Burger com muito Quintão, muita [farta/festa?] do Sacode, muitas idas e vindas aqui, aproveitando o máximo de todas essas delícias. | sopro + o desejo mais completo (cita T.T. e Quintão) |
| 6 | 6 | 00:00:26:05 | 6.21s | MVI_0347.MP4 | 1.01s → 7.22s (00:01:00 → 00:07:05) | 90° horário | — | +12.0 dB | Eu desejo muitos clientes e muita prosperidade, tá bom? (sopra) | desejo + sopro |
| 7 | 7 | 00:00:32:10 | 3.46s | MVI_0348.MP4 | 8.65s → 12.11s (00:08:15 → 00:12:02) | 90° horário | — | +0.8 dB | Eu desejo que tenham mais promoções de Sacode. | desejo (sem o 'é pra eu falar, tipo...'; não sopra no clipe) |
| 8 | 8 | 00:00:35:21 | 6.88s | MVI_0349.MP4 | 9.58s → 16.45s (00:09:14 → 00:16:11) | 90° horário | — | +6.5 dB | Eu desejo muito sucesso e muito T.T. trufado! (ri, sopra e comemora) | fechamento: desejo da marca + sopro + comemoração, no compasso mais forte da música |

(Entrada/saída em segundos do original; entre parênteses, mm:ss:qq a 23,976 fps.)

## Descartados
- **MVI_0344 e MVI_0345:** por instrução do direcional.
- **Trechos não usados:**
  - 0340: "Oi?" no fim;
  - 0346: "Tá bom, hambúrguer novo" e o aceno depois do sopro;
  - 0348: a hesitação inicial e o "Obrigada";
  - 0343: o "Fala!" do início.

## Premissas
1. **Duração:** 42.75 s, perto dos 47 s da referência. O direcional não define duração.
2. **Formato:** 720×1280 a **24 fps**, igual à referência. Os originais são 23,976.
3. **Áudio:**
   - A fala de cada clipe fica na A1, com ganho para igualar as vozes. 0340, 0341 e 0347 foram gravados baixo e ficaram no limite de +12 dB.
   - A música fica na A2: −24 dB durante a fala, −13 dB nos trechos sem fala (ducking) e fade-out de 1,5 s. O XML leva o nível de fala, e as subidas estão no checklist.
4. **Transições:** cortes secos e fade para preto no fim, sem zoom (o direcional não pede).

## Validação do XML
- **Checagem estrutural** (`scripts/validar_xml.py`): XML bem formado (xmllint), 720×1280@24, V1 contígua, A1 sincronizada com a V1 (exceto o plano 1, que é mudo), in/out dentro de cada mídia, originais existem pelo nome e música cobre a sequência.
- **Leitura independente** (OpenTimelineIO): 3 trilhas, 8 clipes de vídeo, 8 de áudio (7 falas + música), 1026 quadros @ 24.
- **Não testei no Premiere.** O ponto sensível é o sinal da rotação (ver checklist).
