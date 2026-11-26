# 1 ano T.T. Burger — desejos com velinha

Entregas: `preview.mp4` · `sequencia.xml` (FCP7 XML para o Premiere) · `checklist_premiere.md` · `relatorio.md` · `plano.json` · `tabela_planos.md`

Rodar: `scripts/pipeline.sh` (`SKIP_DOWNLOAD=1 SKIP_TRANSCRICAO=1` para só remontar; `BASE=/pasta` grava o caminho real no XML; `VERIFICAR=1` transcreve a prévia para conferir as falas).

Trocar ordem ou trechos: edite `dados/escolhas.json`. Cada plano tem estes campos:
- `clipe`;
- `ini`/`fim`: início e fim do conteúdo, em segundos do original;
- `janela_entrada`;
- `ini_min`;
- `limite`;
- `voz`: trechos de fala, para o ducking;
- `som`.

Scripts em `scripts/`: `montar_plano.py`, `gerar_preview.py`, `gerar_xml.py`, `validar_xml.py`, `gerar_docs.py`, `verificar_falas.py`, `transcrever.py` e `detectar_sopro.py` (medida automática da chama; serviu de apoio, a confirmação foi visual). Os reaproveitados estão em `../scripts/`: `baixar_drive.sh` e `analisar_musica.py`.
