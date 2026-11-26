#!/usr/bin/env bash
# Uso: gerar_proxies.sh pasta_originais pasta_proxies  -> proxies 720p (H.264 leve), mesmo fps. Originais intactos.
SRC="$1"; DST="$2"; mkdir -p "$DST"
# paralelo: JOBS=4 por padrão
export DST
ls "$SRC"/*.[Mm][Pp]4 | xargs -P "${JOBS:-4}" -I{} bash -c 'f="{}"; b=$(basename "$f"); o="$DST/${b%.*}.mp4"; [ -s "$o" ] && exit 0; ffmpeg -v error -nostdin -y -i "$f" -vf scale=-2:720 -c:v libx264 -preset veryfast -crf 26 -g 12 -c:a aac -b:a 96k "$o.tmp.mp4" && mv "$o.tmp.mp4" "$o" && echo "$b ok"'
