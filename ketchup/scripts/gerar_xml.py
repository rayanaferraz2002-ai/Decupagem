"""Gera sequencia.xml (FCP7 xmeml v4) para importar no Premiere (vídeo + áudio dos clipes + música).

Uso: python3 -I gerar_xml.py plano.json pasta_originais musica.mp4 saida.xml [--base "/pasta/no/seu/computador"]
- Sequência no tamanho/fps do plano.json (= referência).
- V1: depoimentos (originais pelo nome), Basic Motion com rotação ±90 e escala 66,667%;
  zoom-in = keyframes de escala (66,667% -> 74,667%) do início ao fim do plano.
- A1: áudio dos próprios clipes (Audio Levels com o ganho que iguala o volume); planos com som=false ficam sem A1.
- A2: música no nível de fundo da fala (−26 dB) e Cross Fade no fim; as subidas nas pausas vão no checklist. Fade para preto no fim do vídeo.
"""
import json, os, subprocess, sys, urllib.parse
import xml.etree.ElementTree as ET
from xml.dom import minidom

args = sys.argv[1:]; base = None
if "--base" in args:
    i = args.index("--base"); base = args[i + 1]; del args[i:i + 2]
plano_p, orig, musica, saida = args
P = json.load(open(plano_p)); S = P["sequencia"]; FPS = S["fps"]; DUR = S["duracao_f"]


def url(n): return "file://localhost" + urllib.parse.quote(os.path.join(base or "/MIDIA", n))


def sub(pa, tag, text=None, **at):
    e = ET.SubElement(pa, tag, {k: str(v) for k, v in at.items()})
    if text is not None: e.text = str(text)
    return e


def rate(pa, tb, ntsc=False):
    r = sub(pa, "rate"); sub(r, "timebase", tb); sub(r, "ntsc", "TRUE" if ntsc else "FALSE")


def probe(a):
    return json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,width,height,r_frame_rate:format=duration",
                                      "-of", "json", a], capture_output=True, text=True).stdout)


def transicao(tr, ini, fim, alin, media="video", nome="Cross Dissolve"):
    t = sub(tr, "transitionitem"); sub(t, "start", ini); sub(t, "end", fim); sub(t, "alignment", alin); rate(t, FPS)
    e = sub(t, "effect"); sub(e, "name", nome); sub(e, "effectid", nome); sub(e, "effectcategory", "Dissolve")
    sub(e, "effecttype", "transition"); sub(e, "mediatype", media)


def niveis(ci, db):
    f = sub(ci, "filter"); e = sub(f, "effect"); sub(e, "name", "Audio Levels"); sub(e, "effectid", "audiolevels")
    sub(e, "effectcategory", "audiolevels"); sub(e, "effecttype", "audiolevels"); sub(e, "mediatype", "audio")
    pr = sub(e, "parameter"); sub(pr, "parameterid", "level"); sub(pr, "name", "Level")
    sub(pr, "valuemin", 0); sub(pr, "valuemax", 3.98109); sub(pr, "value", round(10 ** (db / 20), 5))


x = ET.Element("xmeml", version="4"); seq = sub(x, "sequence", id="sequence-1")
sub(seq, "name", P["sequencia"].get("nome", "Sequencia")); sub(seq, "duration", DUR); rate(seq, FPS)
tc = sub(seq, "timecode"); rate(tc, FPS); sub(tc, "string", "00:00:00:00"); sub(tc, "frame", 0); sub(tc, "displayformat", "NDF")
media = sub(seq, "media"); vid = sub(media, "video"); sc = sub(sub(vid, "format"), "samplecharacteristics")
rate(sc, FPS); sub(sc, "width", S["largura"]); sub(sc, "height", S["altura"])
sub(sc, "anamorphic", "FALSE"); sub(sc, "pixelaspectratio", "square"); sub(sc, "fielddominance", "none")
vt = sub(vid, "track")
aud = sub(media, "audio"); asc = sub(sub(aud, "format"), "samplecharacteristics"); sub(asc, "depth", 16); sub(asc, "samplerate", 48000)
a1 = sub(aud, "track")

for p in P["planos"]:
    j = probe(os.path.join(orig, p["arquivo"])); vs = [s for s in j["streams"] if s["codec_type"] == "video"][0]
    fd = float(j["format"]["duration"]); num, den = map(int, vs["r_frame_rate"].split("/"))
    i_f = round(p["in_s"] * FPS); nf = p["timeline_out_f"] - p["timeline_in_f"]
    fid = f"file-{p['clipe']}"
    for kind, track in (("video", vt), ("audio", a1)) if p.get("som", True) else (("video", vt),):
        ci = sub(track, "clipitem", id=f"clipitem-{kind[0]}{p['n']}")
        sub(ci, "name", p["arquivo"]); sub(ci, "enabled", "TRUE"); sub(ci, "duration", round(fd * FPS)); rate(ci, FPS)
        sub(ci, "start", p["timeline_in_f"]); sub(ci, "end", p["timeline_out_f"]); sub(ci, "in", i_f); sub(ci, "out", i_f + nf)
        if kind == "video":
            f = sub(ci, "file", id=fid); sub(f, "name", p["arquivo"]); sub(f, "pathurl", url(p["arquivo"]))
            rate(f, round(num / den), den == 1001); sub(f, "duration", round(fd * num / den))
            fm = sub(f, "media"); fsc = sub(sub(fm, "video"), "samplecharacteristics")
            rate(fsc, round(num / den), den == 1001); sub(fsc, "width", vs["width"]); sub(fsc, "height", vs["height"])
            sub(fsc, "anamorphic", "FALSE"); sub(fsc, "pixelaspectratio", "square"); sub(fsc, "fielddominance", "none")
            fa = sub(fm, "audio"); asc2 = sub(fa, "samplecharacteristics"); sub(asc2, "depth", 16); sub(asc2, "samplerate", 48000)
            sub(fa, "channelcount", 2)
            esc = 100 * S["altura"] / vs["width"]
            ef = sub(sub(ci, "filter"), "effect"); sub(ef, "name", "Basic Motion"); sub(ef, "effectid", "basic")
            sub(ef, "effectcategory", "motion"); sub(ef, "effecttype", "motion"); sub(ef, "mediatype", "video")
            pr = sub(ef, "parameter"); sub(pr, "parameterid", "scale"); sub(pr, "name", "Scale")
            sub(pr, "valuemin", 0); sub(pr, "valuemax", 1000); sub(pr, "value", round(esc, 4))
            if p["zoom"]:  # keyframes no tempo da mídia do clipe (mesma base do in/out)
                for w, v in ((i_f, esc), (i_f + nf, esc * p["zoom_fim"])):
                    k = sub(pr, "keyframe"); sub(k, "when", w); sub(k, "value", round(v, 4))
            pr = sub(ef, "parameter"); sub(pr, "parameterid", "rotation"); sub(pr, "name", "Rotation")
            sub(pr, "valuemin", -8640); sub(pr, "valuemax", 8640); sub(pr, "value", 90 if p["rotacao"] == "cw" else -90)
            pr = sub(ef, "parameter"); sub(pr, "parameterid", "center"); sub(pr, "name", "Center")
            v = sub(pr, "value"); sub(v, "horiz", 0); sub(v, "vert", 0)
            if p["fade_out"]: transicao(vt, p["timeline_out_f"] - P["fade_video_f"], p["timeline_out_f"], "end-black")
        else:
            sub(ci, "file", id=fid)
            st = sub(ci, "sourcetrack"); sub(st, "mediatype", "audio"); sub(st, "trackindex", 1)
            niveis(ci, p["ganho_fala_db"])
        if p.get("som", True):  # vincula vídeo e áudio do mesmo plano
            lk = sub(ci, "link"); sub(lk, "linkclipref", f"clipitem-v{p['n']}"); sub(lk, "mediatype", "video")
            lk = sub(ci, "link"); sub(lk, "linkclipref", f"clipitem-a{p['n']}"); sub(lk, "mediatype", "audio")
for t in (vt, a1): sub(t, "enabled", "TRUE"); sub(t, "locked", "FALSE")

# A2 música
M = P["musica"]; md = float(probe(musica)["format"]["duration"]); mn = os.path.basename(musica)
a2 = sub(aud, "track"); ci = sub(a2, "clipitem", id="clipitem-musica")
sub(ci, "name", mn); sub(ci, "enabled", "TRUE"); sub(ci, "duration", round(md * FPS)); rate(ci, FPS)
m_in = round(M["in_s"] * FPS); sub(ci, "start", 0); sub(ci, "end", DUR); sub(ci, "in", m_in); sub(ci, "out", m_in + DUR)
f = sub(ci, "file", id="file-musica"); sub(f, "name", mn); sub(f, "pathurl", url(mn)); rate(f, FPS); sub(f, "duration", round(md * FPS))
fa = sub(sub(f, "media"), "audio"); asc2 = sub(fa, "samplecharacteristics"); sub(asc2, "depth", 16); sub(asc2, "samplerate", 48000)
sub(fa, "channelcount", 2)
st = sub(ci, "sourcetrack"); sub(st, "mediatype", "audio"); sub(st, "trackindex", 1)
niveis(ci, M["volume_fala_db"])  # nível de fala; subidas nas pausas estão no checklist
transicao(a2, DUR - round(M["fade_out_s"] * FPS), DUR, "end", "audio", "Cross Fade (+3dB)")
sub(a2, "enabled", "TRUE"); sub(a2, "locked", "FALSE")

xml = minidom.parseString(ET.tostring(x, encoding="utf-8")).toprettyxml(indent="  ", encoding="UTF-8").decode()
open(saida, "w", encoding="utf-8").write(xml.replace('<?xml version="1.0" encoding="UTF-8"?>', '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE xmeml>', 1))
print("ok", saida, len(P["planos"]), "planos", DUR, "quadros")
