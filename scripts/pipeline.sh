#!/usr/bin/env bash
# Roda tudo do zero (ou só o que faltar). Originais nunca são alterados.
# Uso: scripts/pipeline.sh [MATERIAL=/home/user/material] [WORK=/home/user/work]
#  etapas: download -> proxies -> análise -> música -> plano -> preview -> xml -> validação -> docs
# Para TROCAR um plano: edite dados/escolhas.json (clipe/janela) e rode com FIXAR=1 para manter os demais.
set -euo pipefail
R="$(cd "$(dirname "$0")/.." && pwd)"
MAT="${MATERIAL:-/home/user/material}"; WORK="${WORK:-/home/user/work}"
MUS="$MAT/trilha/Bring It (Instrumental).mp4"
mkdir -p "$WORK"
if [ "${SKIP_DOWNLOAD:-0}" != 1 ]; then
  "$R/scripts/baixar_drive.sh" "$R/dados/drive_clipes.tsv" "$MAT/evento"
  "$R/scripts/baixar_drive.sh" "$R/dados/drive_trilha.tsv" "$MAT/trilha"
fi
"$R/scripts/gerar_proxies.sh" "$MAT/evento" "$WORK/proxies"
python3 -I "$R/scripts/analisar_clipes.py" "$WORK/proxies" "$WORK/analise"
[ -f "$WORK/musica.wav" ] || ffmpeg -v error -y -i "$MUS" -ac 2 -ar 48000 "$WORK/musica.wav"
python3 -I "$R/scripts/analisar_musica.py" "$WORK/musica.wav" "$R/dados/mapa_batidas_musica.json"
FIX=(); if [ "${FIXAR:-0}" = 1 ] && [ -f "$R/plano.json" ]; then cp "$R/plano.json" "$WORK/plano_anterior.json"; FIX=(--fixar "$WORK/plano_anterior.json"); fi
python3 -I "$R/scripts/montar_plano.py" --escolhas "$R/dados/escolhas.json" --orientacao "$R/dados/orientacao.json" \
  --musica-json "$R/dados/mapa_batidas_musica.json" --proxies "$WORK/proxies" --originais "$MAT/evento" --saida "$R/plano.json" "${FIX[@]}"
python3 -I "$R/scripts/gerar_preview.py" "$R/plano.json" "$WORK/proxies" "$MUS" "$R/preview.mp4"
python3 -I "$R/scripts/gerar_xml.py" "$R/plano.json" "$MAT/evento" "$MUS" "$R/sequencia.xml" ${BASE:+--base "$BASE"}
python3 -I "$R/scripts/validar_xml.py" "$R/sequencia.xml" "$R/plano.json" "$MAT/evento"
python3 -I "$R/scripts/gerar_docs.py" "$R/plano.json" "$R"
