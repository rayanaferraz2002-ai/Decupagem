"""Valida sequencia.xml contra o plano.json.

Uso: python3 -I validar_xml.py sequencia.xml plano.json pasta_originais
Checa: XML bem formado; sequência 720x1280@30; clipes contíguos sem buraco/sobreposição na V1;
duração total; in/out dentro da duração de cada original; arquivos originais existem pelo nome;
música cobre a sequência; leitura independente via OpenTimelineIO (adapter fcp_xml) se instalado.
"""
import sys, os, json
import xml.etree.ElementTree as ET

xml_p, plano_p, orig = sys.argv[1:4]
P = json.load(open(plano_p)); erros = []
root = ET.parse(xml_p).getroot()  # levanta exceção se mal formado
seq = root.find("sequence"); DUR = int(seq.findtext("duration"))
sc = seq.find("media/video/format/samplecharacteristics")
if (sc.findtext("width"), sc.findtext("height"), sc.findtext("rate/timebase")) != ("720", "1280", "30"):
    erros.append("formato da sequência diferente de 720x1280@30")
clips = seq.findall("media/video/track/clipitem")
if len(clips) != len(P["planos"]): erros.append("nº de clipes difere do plano")
pos = 0
for c, p in zip(clips, P["planos"]):
    s, e, i, o = (int(c.findtext(t)) for t in ("start", "end", "in", "out"))
    if s != pos: erros.append(f"{c.get('id')}: começa em {s}, esperado {pos}")
    if e - s != o - i: erros.append(f"{c.get('id')}: duração timeline != duração fonte")
    if i < 0 or o > int(c.findtext("duration")): erros.append(f"{c.get('id')}: in/out fora da mídia")
    nome = c.findtext("file/name")
    if nome != p["arquivo"] or not os.path.exists(os.path.join(orig, nome)): erros.append(f"{nome}: arquivo original não encontrado")
    pos = e
if pos != DUR: erros.append(f"V1 termina em {pos}, sequência tem {DUR}")
for t in seq.findall("media/video/track/transitionitem"):
    if int(t.findtext("end")) <= int(t.findtext("start")): erros.append("transição com duração inválida")
mus = seq.findall("media/audio/track/clipitem")
if len(mus) != 1 or int(mus[0].findtext("end")) != DUR: erros.append("música não cobre a sequência")

otio_msg = "OpenTimelineIO não instalado (pulado)"
try:
    import opentimelineio as otio
    tl = otio.adapters.read_from_file(xml_p, adapter_name="fcp_xml")
    v = [t for t in tl.tracks if t.kind == "Video"][0]
    nclips = len([c for c in v if isinstance(c, otio.schema.Clip)])
    otio_msg = f"OTIO leu: {len(tl.tracks)} trilhas, {nclips} clipes de vídeo, duração {tl.duration().to_frames()} q @ {tl.duration().rate}"
    if nclips != len(P["planos"]): erros.append("OTIO: nº de clipes difere")
except ImportError:
    pass
except Exception as ex:
    erros.append(f"OTIO falhou ao ler: {ex}")

print(otio_msg)
print("VALIDO" if not erros else "ERROS:\n- " + "\n- ".join(erros))
sys.exit(1 if erros else 0)
