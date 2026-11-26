# Relatório — Depoimentos "Minha parte favorita do Quintão" (T.T. Burger)

## Material e como interpretei
O Drive não tinha as pastas `direcional/ referencia/ musica/ clipes/ locucao/`. Identifiquei assim:

| Origem no Drive | Arquivo | Interpretação |
|---|---|---|
| pasta de vídeos | 7 × `MVI_0585…0598.MP4` (1920×1080, 23,976 fps, com áudio) | **clipes/**: depoimentos (a fala de cada clipe é o áudio principal) |
| pasta de trilha | `Feels Good (Instrumental).mp4` (só áudio, 2:15) | **musica/** |
| pasta de trilha | `snapinsta-1795708988972.mp4` (720×1280, 30 fps, 1:35) | **referencia/** |
| — | — | **direcional/**: veio só no texto do pedido |
| — | — | **locucao/**: não há; a "voz" são as falas dos próprios clipes (trilha A1) |

- **Download:** o Drive baixou direto. Para transcrever as falas, liberei no ambiente os hosts do Hugging Face (modelo Whisper "medium", rodando localmente).
- **Originais:** ficaram somente leitura.
- **Orientação:** os 7 clipes foram gravados em pé e salvos deitados. Conferi um a um: 0586, 0587 e 0598 giram 90° no sentido horário; 0585, 0588, 0589 e 0590 giram 90° no anti-horário.

## Passo 1 — Direcional
| Cena | Direção de imagem | Direção de edição | Duração | Áudio |
|---|---|---|---|---|
| 1 | o depoimento com **mais empolgação** | resposta **inteira**, com "minha parte favorita…" | o tempo da resposta, fechando na batida | fala + música baixa |
| 2 a 7 | os outros depoimentos | começam **direto na resposta** (sem "minha parte favorita do Quintão é"); **zoom-in em alguns** para dar movimento | o tempo de cada resposta, fechando na batida | fala + música baixa |

**Perguntei e você confirmou:**
- abrir com MVI_0585;
- sem legenda;
- ~45 s, só respostas;
- manter MVI_0589 sem legenda no trecho incerto.

**Decidi sozinho (o direcional não diz):**
- **Ordem dos planos 2–7:** alternei roupas e ambientes e fechei com a resposta mais curta e enfática ("Comer, gente. Sem dúvida!").
- **Zoom-in:** apliquei nos 3 planos com menos movimento de câmera/pessoa (0587, 0598, 0589), de 100% a 112%, linear.

### Como escolhi o mais empolgado (só no trecho da resposta)
Escore = média dos z-scores de volume da voz, variação de tom (semitons), palavras por segundo e movimento da imagem.

| Clipe | Escore | Volume (dB) | Variação de tom (st) | Palavras/s | Movimento |
|---|---|---|---|---|---|
| MVI_0585 | +0.67 | -16.8 | 9.42 | 3.03 | 15.81 |
| MVI_0588 | +0.60 | -16.8 | 6.04 | 3.32 | 18.6 |
| MVI_0589 | +0.25 | -12.4 | 6.29 | 3.12 | 13.29 |
| MVI_0586 | -0.06 | -15.6 | 5.37 | 2.23 | 17.27 |
| MVI_0590 | -0.15 | -18.4 | 7.81 | 1.59 | 17.29 |
| MVI_0598 | -0.59 | -19.7 | 4.67 | 2.47 | 14.58 |
| MVI_0587 | -0.72 | -26.8 | 9.1 | 2.43 | 11.43 |

O MVI_0585 tem o maior escore e a maior variação de tom. Na imagem ela mostra o burger ("gente, olha só isso, a carne mal passada").

## Passo 2 — Referência (só estilo)
- **Formato:** 95,6 s, **9:16, 720×1280, 30 fps**.
- **Planos:** 7 planos detectados (média de 13,6 s), sem ritmo de clipe musical. Corta a cada troca de pessoa, e cada pessoa fala a resposta inteira, repetindo a pergunta ("O que eu vou sentir mais saudade…").
- **Estilo:** cortes secos, legenda pequena da fala, música instrumental baixa sob a voz, cartela da marca e logos no fim (a cartela não existe neste material, então não entrou).

## Passo 3 — Música (`dados/mapa_batidas_musica.json`)
- **Andamento:** ~115 BPM (batida a cada 0,522 s; o librosa estimou 117,45 no global).
- **Seções:** intro baixa 0:01–0:16 · alta 0:16–1:19 · vale 1:19–1:21 · subida 1:21–1:29 · **clímax 1:29–1:33** · alta 1:33–2:11.
- **Trecho usado:** 0:49,667 → 1:32,97 (começa num compasso). Abre já com energia junto do depoimento mais empolgado, e o **clímax (1:29) cai no último depoimento** ("Comer, gente. Sem dúvida!") e no fade.
- **Cortes:** todos caem numa batida (erro máximo de 17 ms, meio quadro).

## Passo 4 — Escolha dos trechos
- **Método:** transcrição com tempo por palavra. O início de cada resposta foi ajustado ao silêncio mais próximo antes da 1ª palavra, medido em janelas de 10 ms. A saída é a 1ª batida depois do fim da fala, sem invadir fala indesejada.
- **Conferência:** transcrevi a própria prévia plano a plano. Todos começam e terminam onde deviam e nenhuma palavra foi cortada (`scripts/verificar_falas.py`).
- **MVI_0598:** tem 3 tomadas. Usei a 3ª ("…**poder sair do trabalho numa quinta-feira ali, pré-final de semana, comer um hambúrguer, que o do T.T. é o melhor que tem, tomar um chopp, dar uma relaxada**"), que é a mais fluida e cita o T.T.
- **MVI_0588:** o "é" está colado no "poder". Achei o silêncio de 60 ms entre os dois (17,17–17,23 s) e cortei em 17,21 s.
- **MVI_0589:** começa em "é o dia oficial…" (cortei o "porque"). O "é" e o "o" saem colados na fala dela. O final ("…renovar meu kit…?") ficou incerto na transcrição, mas não afeta porque não há legenda.

## Cena → clipe escolhido
| # | Timeline | Dur. | Arquivo original | Entrada → saída no original | Rotação | Zoom | Ganho fala | Fala | Motivo |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 00:00:00:00 | 13.57s | MVI_0585.MP4 | 1.75s → 15.32s (00:01:18 → 00:15:07) | 90° anti-horário | — | +0.8 dB | “A minha parte favorita do Quintão definitivamente é o T.T. Trufado, que é esse hambúrguer que eu pedi, e ainda mais para completar esse ponto. Gente, olha só isso, a carne mal passada do jeitinho que eu gosto.” | abertura: depoimento mais empolgado (maior escore de volume/tom/gestos) e mostra o burger; única resposta inteira, com 'minha parte favorita...' |
| 2 | 00:00:13:17 | 4.70s | MVI_0588.MP4 | 17.21s → 21.91s (00:17:05 → 00:21:21) | 90° anti-horário | — | +0.8 dB | “Poder provar à vontade o chopp da Mabros e comer aquele hambúrguer gostoso de verdade.” | 2º mais empolgado; entra direto na resposta |
| 3 | 00:00:18:08 | 4.67s | MVI_0587.MP4 | 4.90s → 9.57s (00:04:21 → 00:09:13) | 90° horário | sim, 100→112% | +10.8 dB | “Toda semana provar um hambúrguer diferente para saber qual combina com meu paladar.” | resposta direta; pouco movimento de câmera -> zoom-in |
| 4 | 00:00:22:28 | 8.87s | MVI_0598.MP4 | 18.83s → 27.70s (00:18:19 → 00:27:16) | 90° horário | sim, 100→112% | +3.7 dB | “Poder sair do trabalho numa quinta-feira ali, pré-final de semana, comer um hambúrguer, que o do T.T. é o melhor que tem, tomar um chopp, dar uma relaxada.” | 3ª tomada (a mais fluida), cita o T.T.; plano longo e parado -> zoom-in |
| 5 | 00:00:31:24 | 5.23s | MVI_0586.MP4 | 3.85s → 9.08s (00:03:20 → 00:09:02) | 90° horário | — | -0.4 dB | “Poder juntar os meus favoritos, hambúrguer e uma cervejinha.” | resposta direta, hambúrguer + cerveja |
| 6 | 00:00:37:01 | 3.13s | MVI_0589.MP4 | 3.67s → 6.80s (00:03:16 → 00:06:19) | 90° anti-horário | sim, 100→112% | -3.6 dB | “O dia oficial de renovar meu [trecho final incerto na transcrição].” | resposta direta (sem o 'porque é'); pouco movimento -> zoom-in |
| 7 | 00:00:40:05 | 3.13s | MVI_0590.MP4 | 4.12s → 7.25s (00:04:03 → 00:07:06) | 90° anti-horário | — | +2.4 dB | “Comer, gente. Sem dúvida!” | fechamento curto e enfático |

(Entrada/saída em segundos do original; entre parênteses, mm:ss:qq a 23,976 fps.)

## Descartados
- **Nenhum clipe descartado:** todos os 7 depoimentos entraram.
- **Trechos não usados:** em MVI_0588, a conversa antes da resposta ("Calma aí, meu cabelo…", "Pode falar?"); em MVI_0598, as tomadas 1 e 2 e o final ("E é isso, cara. Sempre que encontra alguém conhecido, a gente fica na resenha…"), que você preferiu não incluir.

## Premissas
1. **Duração:** 43.3 s em vez dos 95 s da referência, porque não há material de resposta para mais que isso (**confirmado**).
2. **Formato:** 720×1280 a 30 fps, como a referência.
3. **Áudio:**
   - A fala de cada clipe fica na A1, com ganho para igualar as vozes (alvo de −16 dB; o MVI_0587 precisou de +10,8 dB).
   - A música fica na A2, a −26 dB durante a fala e −16 dB nas pausas (ducking), com fade-out de 1,5 s. O XML leva o nível de fala, e as subidas nas pausas estão no checklist.
4. **Transições:** cortes secos (como na referência) e fade para preto no fim.
5. **Prévia:** renderizada direto dos originais (são poucos). O XML aponta para os originais pelo nome.

## Validação do XML
- **Checagem estrutural** (`scripts/validar_xml.py`): XML bem formado (xmllint), 720×1280@30, V1 e A1 contíguas e sincronizadas, in/out dentro de cada mídia, originais existem pelo nome, zoom com 2 keyframes exatamente nos planos marcados e música cobrindo a sequência.
- **Leitura independente** (OpenTimelineIO): 3 trilhas, 7 clipes de vídeo, 8 de áudio, 1299 quadros @ 30.
- **Não testei no Premiere.** Os pontos sensíveis são o sinal da rotação e os keyframes do zoom; o checklist traz os valores para aplicar à mão.
