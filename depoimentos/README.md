# Depoimentos — "Minha parte favorita do Quintão" (T.T. Burger)

Entregas: `preview.mp4` · `sequencia.xml` (FCP7 XML para o Premiere) · `checklist_premiere.md` · `relatorio.md` · `plano.json` · `tabela_planos.md`

Rodar tudo: `scripts/pipeline.sh` (`SKIP_DOWNLOAD=1 SKIP_TRANSCRICAO=1` para só remontar; `BASE=/pasta` grava o caminho real no XML; `VERIFICAR=1` transcreve a prévia para conferir os cortes de fala).

Trocar ordem, trechos ou zoom: edite `dados/escolhas.json` (cada plano tem `clipe`, `resposta_ini/fim`, `zoom` e, opcionalmente, `janela_entrada`) e rode de novo.

Scripts próprios em `scripts/`: `transcrever.py`, `medir_empolgacao.py`, `montar_plano.py`, `gerar_preview.py`, `gerar_xml.py`, `validar_xml.py`, `verificar_falas.py`, `gerar_docs.py`. Os scripts reaproveitados do projeto anterior estão em `../scripts/`: `baixar_drive.sh` e `analisar_musica.py`.
Dependências: ffmpeg, `faster-whisper librosa opencv-python-headless scenedetect opentimelineio otio-fcp-adapter` (o modelo Whisper é baixado do Hugging Face).
