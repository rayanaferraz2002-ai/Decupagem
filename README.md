# Decupagem — Recap evento 19/11 (1 ano T.T. Macaé)

Entregas:
- `preview.mp4`: prévia leve (720×1280, 30 fps, 43,97 s)
- `sequencia.xml`: XML do Final Cut Pro 7 (xmeml) para importar no Premiere (File → Import), apontando para os originais `MVI_xxxx.MP4`
- `checklist_premiere.md`: o que conferir e aplicar no Premiere (rotação, fusões, fade, cor), com timecodes
- `relatorio.md`: roteiro, análise da referência e da música, cena → clipe, descartados e premissas
- `plano.json`: base da prévia e do XML (cena → clipe, entrada/saída, rotação, transição)
- `tabela_planos.md`: tabela cena → clipe gerada a partir do plano

## Scripts (`scripts/`)
| script | faz |
|---|---|
| `pipeline.sh` | roda tudo (`SKIP_DOWNLOAD=1` pula o download; `FIXAR=1` mantém os trechos já escolhidos; `BASE=/pasta` grava o caminho real no XML) |
| `baixar_drive.sh` | baixa do Drive via drive.usercontent.google.com (lista em `dados/drive_*.tsv`) |
| `gerar_proxies.sh` | proxies 720p em paralelo |
| `analisar_clipes.py` | nitidez, tremor, brilho, cenas e folhas de contato |
| `folhas_verticais.py` | folhas de contato já giradas (para conferir a orientação) |
| `analisar_musica.py` | BPM, batidas, tempos fortes e seções de energia (librosa) |
| `montar_plano.py` | `dados/escolhas.json` + mapa de batidas → `plano.json` |
| `gerar_preview.py` | `plano.json` → `preview.mp4` |
| `gerar_xml.py` | `plano.json` → `sequencia.xml` |
| `validar_xml.py` | valida o XML (estrutura + OpenTimelineIO) |
| `gerar_docs.py` | checklist + tabela de planos |

## Trocar um plano
Edite o plano em `dados/escolhas.json` (campos `clipe` e `janela` em segundos do original) e rode:
```
SKIP_DOWNLOAD=1 FIXAR=1 scripts/pipeline.sh
```
Só o plano alterado muda. Para forçar um ponto exato, edite `in_s`/`out_s` no `plano.json` (mantenha a duração)
e rode só `gerar_preview.py`, `gerar_xml.py`, `validar_xml.py` e `gerar_docs.py`.

Dependências: ffmpeg, Python 3 com `librosa opencv-python-headless scenedetect opentimelineio otio-fcp-adapter`.
