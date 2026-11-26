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
tracks = seq.findall("media/video/track")
todos = P["planos"]; arq = {}
for c in seq.iter("file"):
    if c.findtext("name"): arq[c.get("id")] = c.findtext("name")
for ti, tr in enumerate(tracks):
    cam = f"V{ti + 1}"; esp = [p for p in todos if p.get("camada", "V1") == cam]
    clips = tr.findall("clipitem")
    if len(clips) != len(esp): erros.append(f"{cam}: {len(clips)} clipes, plano tem {len(esp)}")
    pos = 0 if cam == "V1" else None; fim_ant = 0
    for c, p in zip(clips, esp):
        s, e, i, o = (int(c.findtext(t)) for t in ("start", "end", "in", "out"))
        if cam == "V1" and s != pos: erros.append(f"{c.get('id')}: começa em {s}, esperado {pos} (buraco/sobreposição na V1)")
        if cam != "V1" and s < fim_ant: erros.append(f"{c.get('id')}: sobreposição na {cam}")
        if (s, e) != (p["timeline_in_f"], p["timeline_out_f"]): erros.append(f"{c.get('id')}: tempo difere do plano")
        if e - s != o - i: erros.append(f"{c.get('id')}: duração timeline != duração fonte")
        if i < 0 or o > int(c.findtext("duration")): erros.append(f"{c.get('id')}: in/out fora da mídia")
        nome = arq.get(c.find("file").get("id"))
        if nome != p["arquivo"] or not os.path.exists(os.path.join(orig, nome)): erros.append(f"{nome}: arquivo original não encontrado")
        if p.get("faixa"):
            cr = {q.findtext("parameterid"): float(q.findtext("value")) for q in c.findall("filter/effect[effectid='crop']/parameter")}
            if not cr or abs(cr["left"] + cr["right"] - 100 * (1 - (p["recorte_y"][1] - p["recorte_y"][0]))) > 0.01:
                erros.append(f"{c.get('id')}: recorte do mosaico ausente/errado")
        pos = e; fim_ant = e
    if cam == "V1" and pos != DUR: erros.append(f"V1 termina em {pos}, sequência tem {DUR}")
for t in seq.findall("media/video/track/transitionitem"):
    if int(t.findtext("end")) <= int(t.findtext("start")): erros.append("transição com duração inválida")
mus = seq.findall("media/audio/track/clipitem")
if len(mus) != 1 or int(mus[0].findtext("end")) != DUR: erros.append("música não cobre a sequência")

otio_msg = "OpenTimelineIO não instalado (pulado)"
try:
    import opentimelineio as otio
    tl = otio.adapters.read_from_file(xml_p, adapter_name="fcp_xml")
    nclips = sum(len([c for c in t if isinstance(c, otio.schema.Clip)]) for t in tl.tracks if t.kind == "Video")
    otio_msg = f"OTIO leu: {len(tl.tracks)} trilhas, {nclips} clipes de vídeo (V1+V2+V3), duração {tl.duration().to_frames()} q @ {tl.duration().rate}"
    if nclips != len(P["planos"]): erros.append("OTIO: nº de clipes difere")
except ImportError:
    pass
except Exception as ex:
    erros.append(f"OTIO falhou ao ler: {ex}")

print(otio_msg)
print("VALIDO" if not erros else "ERROS:\n- " + "\n- ".join(erros))
sys.exit(1 if erros else 0)
