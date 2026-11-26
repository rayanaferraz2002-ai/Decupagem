"""Gera sequencia.xml (Final Cut Pro 7 XML / xmeml v4) a partir do plano.json, para importar no Premiere.

Uso: python3 -I gerar_xml.py plano.json pasta_originais musica.mp4 saida.xml [--base "/caminho/no/seu/computador"]

- Sequência: 720x1280, 30 fps (referência). Vídeo V1 com os planos; A1 com a música.
- Aponta para os ORIGINAIS pelo nome (MVI_xxxx.MP4, 23,976 fps). Sem --base, o caminho é
  file://localhost/MIDIA/<nome>; no Premiere use "Link Media" apontando a pasta real
  (com "Align by: File Name" os demais são encontrados sozinhos). Com --base o caminho já sai certo.
- Cada clipe leva Basic Motion: rotação ±90° (endireita o original deitado) e escala 66,667%
  (1080x1920 -> 720x1280, preenche o quadro sem corte).
- Fusões simples (Cross Dissolve) onde o plano marca "dissolve"; fade para preto no fim do vídeo
  e Cross Fade de áudio no fim da música.
- Áudio de câmera dos clipes NÃO entra (só a música).
"""
import json, subprocess, sys, os, urllib.parse
import xml.etree.ElementTree as ET
from xml.dom import minidom

args = sys.argv[1:]
base = None
if "--base" in args:
    i = args.index("--base"); base = args[i + 1]; del args[i:i + 2]
plano_p, orig_dir, musica, saida = args
P = json.load(open(plano_p)); S = P["sequencia"]; FPS = S["fps"]; DUR = S["duracao_f"]


def url(name):
    root = base if base else "/MIDIA"
    return "file://localhost" + urllib.parse.quote(os.path.join(root, name))


def sub(parent, tag, text=None, **attr):
    e = ET.SubElement(parent, tag, {k: str(v) for k, v in attr.items()})
    if text is not None: e.text = str(text)
    return e


def rate(parent, tb, ntsc):
    r = sub(parent, "rate"); sub(r, "timebase", tb); sub(r, "ntsc", "TRUE" if ntsc else "FALSE"); return r


def probe(path):
    j = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                                   "stream=codec_type,width,height,r_frame_rate,sample_rate,channels:format=duration",
                                   "-of", "json", path], capture_output=True, text=True).stdout)
    return j


def dissolve(parent, start, end, align, mediatype="video", name="Cross Dissolve"):
    t = sub(parent, "transitionitem"); sub(t, "start", start); sub(t, "end", end); sub(t, "alignment", align)
    rate(t, FPS, False)
    e = sub(t, "effect"); sub(e, "name", name); sub(e, "effectid", name); sub(e, "effectcategory", "Dissolve")
    sub(e, "effecttype", "transition"); sub(e, "mediatype", mediatype)
    if mediatype == "video":
        sub(e, "wipecode", 0); sub(e, "wipeaccuracy", 100); sub(e, "startratio", 0); sub(e, "endratio", 1); sub(e, "reverse", "FALSE")
    return t


x = ET.Element("xmeml", version="4")
seq = sub(x, "sequence", id="sequence-1")
sub(seq, "name", "Recap 1 ano TT Macae - 19-11")
sub(seq, "duration", DUR); rate(seq, FPS, False)
tc = sub(seq, "timecode"); rate(tc, FPS, False); sub(tc, "string", "00:00:00:00"); sub(tc, "frame", 0); sub(tc, "displayformat", "NDF")
media = sub(seq, "media")
vid = sub(media, "video"); fmt = sub(vid, "format"); sc = sub(fmt, "samplecharacteristics")
rate(sc, FPS, False); sub(sc, "width", S["largura"]); sub(sc, "height", S["altura"])
sub(sc, "anamorphic", "FALSE"); sub(sc, "pixelaspectratio", "square"); sub(sc, "fielddominance", "none")
D = P["dissolve_f"]; h = D // 2; todos = P["planos"]


def crop_pct(p):
    """faixa (fração da altura do quadro já endireitado) -> Crop em % do ORIGINAL deitado.
    Giro horário: o topo do quadro final é a esquerda do original; anti-horário: a direita."""
    y0, y1 = p["recorte_y"]
    if p["rotacao"] == "cw":
        return {"left": 100 * y0, "right": 100 * (1 - y1), "top": 0, "bottom": 0}
    return {"left": 100 * (1 - y1), "right": 100 * y0, "top": 0, "bottom": 0}


def clipitem(track, k, p):
    info = probe(os.path.join(orig_dir, p["arquivo"]))
    vs = [s for s in info["streams"] if s["codec_type"] == "video"][0]
    fdur_s = float(info["format"]["duration"])
    ci = sub(track, "clipitem", id=f"clipitem-{k}")
    sub(ci, "name", p["arquivo"]); sub(ci, "enabled", "TRUE")
    sub(ci, "duration", round(fdur_s * FPS)); rate(ci, FPS, False)
    sub(ci, "start", p["timeline_in_f"]); sub(ci, "end", p["timeline_out_f"])
    # in/out na base de tempo da sequência (30 fps), como o Premiere faz em mídias de fps diferente
    sub(ci, "in", round(p["in_s"] * FPS)); sub(ci, "out", round(p["in_s"] * FPS) + p["timeline_out_f"] - p["timeline_in_f"])
    fid = "file-" + p["clipe"]
    if fid in arquivos_def:
        sub(ci, "file", id=fid)
    else:
        arquivos_def.add(fid)
        f = sub(ci, "file", id=fid)
        sub(f, "name", p["arquivo"]); sub(f, "pathurl", url(p["arquivo"]))
        num, den = map(int, vs["r_frame_rate"].split("/"))
        ntsc = den == 1001; tb = round(num / den)
        rate(f, tb, ntsc); sub(f, "duration", round(fdur_s * num / den))
        fm = sub(f, "media"); fv = sub(fm, "video"); fsc = sub(fv, "samplecharacteristics")
        rate(fsc, tb, ntsc); sub(fsc, "width", vs["width"]); sub(fsc, "height", vs["height"])
        sub(fsc, "anamorphic", "FALSE"); sub(fsc, "pixelaspectratio", "square"); sub(fsc, "fielddominance", "none")
        fa = sub(fm, "audio"); sub(fa, "channelcount", 2)
    # Basic Motion: rotação + escala (sem mudar posição)
    flt = sub(ci, "filter"); ef = sub(flt, "effect")
    sub(ef, "name", "Basic Motion"); sub(ef, "effectid", "basic"); sub(ef, "effectcategory", "motion")
    sub(ef, "effecttype", "motion"); sub(ef, "mediatype", "video")
    pr = sub(ef, "parameter"); sub(pr, "parameterid", "scale"); sub(pr, "name", "Scale")
    sub(pr, "valuemin", 0); sub(pr, "valuemax", 1000); sub(pr, "value", round(100 * S["altura"] / vs["width"], 4))
    pr = sub(ef, "parameter"); sub(pr, "parameterid", "rotation"); sub(pr, "name", "Rotation")
    sub(pr, "valuemin", -8640); sub(pr, "valuemax", 8640); sub(pr, "value", 90 if p["rotacao"] == "cw" else -90)
    pr = sub(ef, "parameter"); sub(pr, "parameterid", "center"); sub(pr, "name", "Center")
    v = sub(pr, "value"); sub(v, "horiz", 0); sub(v, "vert", 0)
    if p.get("faixa"):  # painel do mosaico: só recorte, o terço já está no lugar certo
        flt = sub(ci, "filter"); ef = sub(flt, "effect")
        sub(ef, "name", "Crop"); sub(ef, "effectid", "crop"); sub(ef, "effectcategory", "motion")
        sub(ef, "effecttype", "motion"); sub(ef, "mediatype", "video")
        for nm, val in crop_pct(p).items():
            pr = sub(ef, "parameter"); sub(pr, "parameterid", nm); sub(pr, "name", nm)
            sub(pr, "valuemin", 0); sub(pr, "valuemax", 100); sub(pr, "value", round(val, 4))


arquivos_def = set(); k = 0
for cam in ["V1", "V2", "V3"]:
    itens = [p for p in todos if p.get("camada", "V1") == cam]
    if not itens: continue
    vt = sub(vid, "track")
    for p in itens:
        k += 1
        if cam == "V1" and p["transicao_entrada"] == "dissolve":
            dissolve(vt, p["timeline_in_f"] - h, p["timeline_in_f"] + h, "center")
        clipitem(vt, k, p)
        if p.get("fade_out"):
            dissolve(vt, p["timeline_out_f"] - P["fade_video_f"], p["timeline_out_f"], "end-black")
    sub(vt, "enabled", "TRUE"); sub(vt, "locked", "FALSE")

# áudio: música
aud = sub(media, "audio"); af = sub(aud, "format"); asc = sub(af, "samplecharacteristics")
sub(asc, "depth", 16); sub(asc, "samplerate", 48000)
at = sub(aud, "track")
M = P["musica"]; minfo = probe(musica); mdur = float(minfo["format"]["duration"])
ci = sub(at, "clipitem", id="clipitem-musica")
mname = os.path.basename(musica)
sub(ci, "name", mname); sub(ci, "enabled", "TRUE"); sub(ci, "duration", round(mdur * FPS)); rate(ci, FPS, False)
sub(ci, "start", 0); sub(ci, "end", DUR); m_in = round(M["in_s"] * FPS)
sub(ci, "in", m_in); sub(ci, "out", m_in + DUR)
f = sub(ci, "file", id="file-musica"); sub(f, "name", mname); sub(f, "pathurl", url(mname))
rate(f, FPS, False); sub(f, "duration", round(mdur * FPS))
fm = sub(f, "media"); fa = sub(fm, "audio"); fsc = sub(fa, "samplecharacteristics")
sub(fsc, "depth", 16); sub(fsc, "samplerate", 48000); sub(fa, "channelcount", 2)
st = sub(ci, "sourcetrack"); sub(st, "mediatype", "audio"); sub(st, "trackindex", 1)
fo = round(M["fade_out_s"] * FPS)
dissolve(at, DUR - fo, DUR, "end", mediatype="audio", name="Cross Fade (+3dB)")
sub(at, "enabled", "TRUE"); sub(at, "locked", "FALSE")

xml = minidom.parseString(ET.tostring(x, encoding="utf-8")).toprettyxml(indent="  ", encoding="UTF-8").decode()
xml = xml.replace('<?xml version="1.0" encoding="UTF-8"?>', '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE xmeml>', 1)
open(saida, "w", encoding="utf-8").write(xml)
print("ok", saida, f"{len(todos)} clipes, {DUR} quadros")
