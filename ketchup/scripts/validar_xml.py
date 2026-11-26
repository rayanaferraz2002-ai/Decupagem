"""Valida sequencia.xml dos depoimentos contra o plano.json.
Uso: python3 -I validar_xml.py sequencia.xml plano.json pasta_originais
Checa: bem formado; 720x1280@30; V1 e A1 contíguas, iguais ao plano e sincronizadas (mesmo in/out);
in/out dentro da mídia; originais existem; zoom com 2 keyframes nos planos marcados; música cobre tudo;
leitura independente via OpenTimelineIO (adapter fcp_xml)."""
import sys, os, json
import xml.etree.ElementTree as ET

xml_p, plano_p, orig = sys.argv[1:4]
P = json.load(open(plano_p)); E = []; planos = P["planos"]
seq = ET.parse(xml_p).getroot().find("sequence"); DUR = int(seq.findtext("duration"))
sc = seq.find("media/video/format/samplecharacteristics")
S = P["sequencia"]
if (sc.findtext("width"), sc.findtext("height"), sc.findtext("rate/timebase")) != (str(S["largura"]), str(S["altura"]), str(S["fps"])): E.append("formato da sequência difere do plano")
nomes = {f.get("id"): f.findtext("name") for f in seq.iter("file") if f.findtext("name")}
V = seq.findall("media/video/track/clipitem"); A = seq.findall("media/audio/track")
A1 = A[0].findall("clipitem"); A2 = A[1].findall("clipitem")
com_som = [p for p in planos if p.get("som", True)]
for nome, trilha, esp in (("V1", V, planos), ("A1", A1, com_som)):
    if len(trilha) != len(esp): E.append(f"{nome}: {len(trilha)} clipes, plano tem {len(esp)}")
    pos = esp[0]["timeline_in_f"] if esp else 0
    for c, p in zip(trilha, esp):
        s, e, i, o = (int(c.findtext(t)) for t in ("start", "end", "in", "out"))
        if s != pos: E.append(f"{c.get('id')}: começa em {s}, esperado {pos} (buraco/sobreposição)")
        if (s, e) != (p["timeline_in_f"], p["timeline_out_f"]) or e - s != o - i: E.append(f"{c.get('id')}: tempos inconsistentes")
        if i < 0 or o > int(c.findtext("duration")): E.append(f"{c.get('id')}: in/out fora da mídia")
        n = nomes.get(c.find("file").get("id"))
        if n != p["arquivo"] or not os.path.exists(os.path.join(orig, n)): E.append(f"{c.get('id')}: original {n} não encontrado")
        pos = e
    if pos != DUR: E.append(f"{nome} termina em {pos}, sequência {DUR}")
Vs = [c for c, p in zip(V, planos) if p.get("som", True)]
for v, a in zip(Vs, A1):
    if [v.findtext(t) for t in ("start", "in")] != [a.findtext(t) for t in ("start", "in")]: E.append(f"{v.get('id')}: áudio fora de sincronia")
for c, p in zip(V, planos):
    kf = c.findall("filter/effect[effectid='basic']/parameter[parameterid='scale']/keyframe")
    if bool(p.get("zoom")) != (len(kf) == 2): E.append(f"{c.get('id')}: zoom no XML não confere com o plano")
if len(A2) != 1 or int(A2[0].findtext("end")) != DUR: E.append("música não cobre a sequência")
msg = "OTIO não instalado"
try:
    import opentimelineio as otio
    tl = otio.adapters.read_from_file(xml_p, adapter_name="fcp_xml")
    nv = sum(len([c for c in t if isinstance(c, otio.schema.Clip)]) for t in tl.tracks if t.kind == "Video")
    na = sum(len([c for c in t if isinstance(c, otio.schema.Clip)]) for t in tl.tracks if t.kind == "Audio")
    msg = f"OTIO leu: {len(tl.tracks)} trilhas, {nv} clipes de vídeo, {na} de áudio, {tl.duration().to_frames()} q @ {tl.duration().rate}"
    if nv != len(planos) or na != len(com_som) + 1: E.append("OTIO: contagem de clipes difere")
except ImportError:
    pass
except Exception as ex:
    E.append(f"OTIO falhou: {ex}")
print(msg); print("VALIDO" if not E else "ERROS:\n- " + "\n- ".join(E)); sys.exit(1 if E else 0)
