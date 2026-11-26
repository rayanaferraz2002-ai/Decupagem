#!/usr/bin/env bash
# Uso: baixar_drive.sh lista.tsv pasta_destino
# lista.tsv: id<TAB>nome<TAB>tamanho (bytes). Usa drive.usercontent.google.com (sem redirect).
set -u
LIST="$1"; DEST="$2"; mkdir -p "$DEST"
while IFS=$'\t' read -r id name size; do
  out="$DEST/$name"
  if [ -f "$out" ] && [ "$(stat -c %s "$out")" = "$size" ]; then continue; fi
  for i in 1 2 3 4; do
    curl -sSL --retry 3 -o "$out" "https://drive.usercontent.google.com/download?id=$id&export=download&confirm=t" \
      && [ "$(stat -c %s "$out")" = "$size" ] && break
    sleep $((i*2))
  done
  echo "$name $(stat -c %s "$out")/$size"
done < "$LIST"
