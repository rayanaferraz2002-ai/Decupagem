#!/usr/bin/env bash
# Depoimentos "minha parte favorita do Quintão": roda tudo. Originais nunca são alterados.
# Variáveis: MATERIAL (padrão /home/user/material2), SKIP_DOWNLOAD=1, SKIP_TRANSCRICAO=1, BASE=/pasta/real (caminho no XML)
# Para trocar ordem/trechos/zoom: edite dados/escolhas.json e rode de novo (SKIP_DOWNLOAD=1 SKIP_TRANSCRICAO=1).
set -euo pipefail
R="$(cd "$(dirname "$0")/.." && pwd)"; G="$R/../scripts"
MAT="${MATERIAL:-/home/user/material2}"; MUS="$MAT/trilha/Feels Good (Instrumental).mp4"; WORK="${WORK:-/home/user/work2}"
export HF_HUB_DISABLE_XET=1
mkdir -p "$WORK"
if [ "${SKIP_DOWNLOAD:-0}" != 1 ]; then
  "$G/baixar_drive.sh" "$R/dados/drive_clipes.tsv" "$MAT/clipes"; "$G/baixar_drive.sh" "$R/dados/drive_trilha.tsv" "$MAT/trilha"
fi
if [ "${SKIP_TRANSCRICAO:-0}" != 1 ]; then
  WHISPER_PROMPT="Quintão no T.T. Burger. Minha parte favorita do Quintão é o T.T. trufado, o chopp da Mabros, hambúrguer, cervejinha." \
    python3 -I "$R/scripts/transcrever.py" "$R/dados/transcricoes_v2.json" "$MAT"/clipes/*.MP4
  python3 -I "$R/scripts/medir_empolgacao.py" "$R/dados/transcricoes_v2.json" "$MAT/clipes" "$R/dados/empolgacao.json"
fi
[ -f "$WORK/musica.wav" ] || ffmpeg -v error -y -i "$MUS" -ac 2 -ar 48000 "$WORK/musica.wav"
[ -f "$R/dados/mapa_batidas_musica.json" ] || python3 -I "$G/analisar_musica.py" "$WORK/musica.wav" "$R/dados/mapa_batidas_musica.json"
python3 -I "$R/scripts/montar_plano.py" "$R/dados/escolhas.json" "$R/dados/orientacao.json" "$R/dados/mapa_batidas_musica.json" \
  "$R/dados/empolgacao.json" "$MAT/clipes" "$R/plano.json"
python3 -I "$R/scripts/gerar_preview.py" "$R/plano.json" "$MAT/clipes" "$MUS" "$R/preview.mp4"
python3 -I "$R/scripts/gerar_xml.py" "$R/plano.json" "$MAT/clipes" "$MUS" "$R/sequencia.xml" ${BASE:+--base "$BASE"}
python3 -I "$R/scripts/validar_xml.py" "$R/sequencia.xml" "$R/plano.json" "$MAT/clipes"
python3 -I "$R/scripts/gerar_docs.py" "$R/plano.json" "$R"
[ "${VERIFICAR:-0}" = 1 ] && python3 -I "$R/scripts/verificar_falas.py" "$R/plano.json" "$R/preview.mp4"
exit 0
