#!/usr/bin/env python3
"""
Extracción literal de un .docx a Markdown, reconstruyendo la numeración automática de Word.

Uso:
    python3 extraer_docx.py <archivo.docx> <salida.md> [--pdf-texto <pdftotext.txt>]

- El texto de cada párrafo y celda se copia tal cual (sin resumir ni corregir).
- La numeración automática (numbering.xml) se reconstruye con un motor simple:
  el contador se comparte entre listas (numId) que usan la misma definición (abstractNum),
  como hace Word; un startOverride reinicia el nivel la primera vez que se usa esa lista;
  un nivel reinicia a los inferiores.
- Si se pasa --pdf-texto (salida de `pdftotext -layout`), se comprueba que cada rótulo
  numérico tipo "6.9.1." exista en el PDF y se informa la diferencia.
- Se ejecuta en el entorno del agente; no forma parte de ningún proyecto.
"""
import re, sys, zipfile
from xml.etree import ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def q(tag):
    return W + tag


def roman(n):
    vals = [(1000, "m"), (900, "cm"), (500, "d"), (400, "cd"), (100, "c"), (90, "xc"),
            (50, "l"), (40, "xl"), (10, "x"), (9, "ix"), (5, "v"), (4, "iv"), (1, "i")]
    out = ""
    for v, s in vals:
        while n >= v:
            out += s
            n -= v
    return out


def fmt(n, kind):
    if kind == "decimal":
        return str(n)
    if kind == "lowerLetter":
        return chr(ord("a") + (n - 1) % 26)
    if kind == "upperLetter":
        return chr(ord("A") + (n - 1) % 26)
    if kind == "lowerRoman":
        return roman(n)
    if kind == "upperRoman":
        return roman(n).upper()
    return ""


class Numbering:
    def __init__(self, z):
        self.abstract, self.nums, self.counters, self.used = {}, {}, {}, set()
        if "word/numbering.xml" not in z.namelist():
            return
        root = ET.fromstring(z.read("word/numbering.xml"))
        for an in root.findall(q("abstractNum")):
            levels = {}
            for lvl in an.findall(q("lvl")):
                il = int(lvl.get(q("ilvl")))
                g = lambda t, d=None: (lvl.find(q(t)).get(q("val")) if lvl.find(q(t)) is not None else d)
                levels[il] = {"start": int(g("start", "1")), "fmt": g("numFmt", "decimal"),
                              "text": g("lvlText", "")}
            self.abstract[an.get(q("abstractNumId"))] = levels
        for n in root.findall(q("num")):
            aid = n.find(q("abstractNumId")).get(q("val"))
            overrides = {}
            for ov in n.findall(q("lvlOverride")):
                so = ov.find(q("startOverride"))
                if so is not None:
                    overrides[int(ov.get(q("ilvl")))] = int(so.get(q("val")))
            self.nums[n.get(q("numId"))] = (aid, overrides)

    def label(self, num_id, ilvl):
        if num_id not in self.nums or num_id == "0":
            return None
        aid, overrides = self.nums[num_id]
        levels = self.abstract.get(aid, {})
        if ilvl not in levels:
            return None
        cnt = self.counters.setdefault(aid, {})
        start = levels[ilvl]["start"]
        if ilvl in overrides and (num_id, ilvl) not in self.used:
            cnt[ilvl] = overrides[ilvl]
        else:
            cnt[ilvl] = cnt.get(ilvl, start - 1) + 1
        self.used.add((num_id, ilvl))
        for deeper in [k for k in cnt if k > ilvl]:
            del cnt[deeper]
        lv = levels[ilvl]
        if lv["fmt"] == "bullet":
            return "-"
        if lv["fmt"] == "none":
            return ""
        text = lv["text"]
        for k in range(0, 9):
            if f"%{k + 1}" in text:
                l = levels.get(k, {"start": 1, "fmt": "decimal"})
                val = cnt.get(k, l["start"])
                text = text.replace(f"%{k + 1}", fmt(val, l["fmt"]))
        return text


def style_numpr(z):
    out, heads = {}, {}
    root = ET.fromstring(z.read("word/styles.xml"))
    for s in root.findall(q("style")):
        sid = s.get(q("styleId"))
        ppr = s.find(q("pPr"))
        if ppr is not None and ppr.find(q("numPr")) is not None:
            np_ = ppr.find(q("numPr"))
            nid = np_.find(q("numId"))
            il = np_.find(q("ilvl"))
            out[sid] = (nid.get(q("val")) if nid is not None else None,
                        int(il.get(q("val"))) if il is not None else 0)
        name = s.find(q("name"))
        if name is not None and re.match(r"heading (\d)", name.get(q("val")), re.I):
            heads[sid] = int(re.match(r"heading (\d)", name.get(q("val")), re.I).group(1))
    return out, heads


def run_text(el):
    parts = []
    for node in el.iter():
        if node.tag == q("t"):
            parts.append(node.text or "")
        elif node.tag == q("tab"):
            parts.append("\t")
        elif node.tag in (q("br"), q("cr")):
            parts.append("\n")
        elif node.tag == q("footnoteReference"):
            parts.append(f"[^{node.get(q('id'))}]")
        elif node.tag == q("drawing") or node.tag.endswith("}pict"):
            parts.append("[IMAGEN]")
    return "".join(parts)


def para(p, numbering, snum, heads):
    ppr = p.find(q("pPr"))
    num_id, ilvl, style = None, 0, None
    if ppr is not None:
        ps = ppr.find(q("pStyle"))
        style = ps.get(q("val")) if ps is not None else None
        np_ = ppr.find(q("numPr"))
        if np_ is not None:
            nid = np_.find(q("numId"))
            il = np_.find(q("ilvl"))
            num_id = nid.get(q("val")) if nid is not None else None
            ilvl = int(il.get(q("val"))) if il is not None else 0
    if num_id is None and style in snum:
        num_id, ilvl = snum[style]
    text = run_text(p).strip()
    lab = numbering.label(num_id, ilvl) if num_id else None
    return lab, text, heads.get(style)


def cell_text(tc, numbering, snum, heads):
    lines = []
    for p in tc.iter(q("p")):
        lab, t, _ = para(p, numbering, snum, heads)
        if t:
            lines.append((lab + " " if lab else "") + t)
    return "<br>".join(x.replace("|", "\\|").replace("\n", "<br>") for x in lines)


def main():
    src, dst = sys.argv[1], sys.argv[2]
    pdf_txt = sys.argv[sys.argv.index("--pdf-texto") + 1] if "--pdf-texto" in sys.argv else None
    z = zipfile.ZipFile(src)
    numbering = Numbering(z)
    snum, heads = style_numpr(z)
    body = ET.fromstring(z.read("word/document.xml")).find(q("body"))
    out, labels = [], []
    for el in body:
        if el.tag == q("p"):
            lab, t, h = para(el, numbering, snum, heads)
            if not t:
                continue
            if lab and lab != "-":
                labels.append(lab)
            if h:
                out.append("#" * min(h, 4) + " " + ((lab + " ") if lab else "") + t)
            elif lab == "-":
                out.append("- " + t)
            else:
                out.append(((lab + " ") if lab else "") + t)
            out.append("")
        elif el.tag == q("tbl"):
            rows = []
            for tr in el.findall(q("tr")):
                rows.append([cell_text(tc, numbering, snum, heads) for tc in tr.findall(q("tc"))])
            if not rows:
                continue
            width = max(len(r) for r in rows)
            rows = [r + [""] * (width - len(r)) for r in rows]
            out.append("| " + " | ".join(rows[0]) + " |")
            out.append("|" + "---|" * width)
            for r in rows[1:]:
                out.append("| " + " | ".join(r) + " |")
            out.append("")
    if "word/footnotes.xml" in z.namelist():
        fn = ET.fromstring(z.read("word/footnotes.xml"))
        notes = []
        for f in fn.findall(q("footnote")):
            fid = f.get(q("id"))
            if fid and int(fid) > 0:
                notes.append(f"[^{fid}]: " + " ".join(run_text(p).strip() for p in f.iter(q("p"))).strip())
        if notes:
            out += ["", "---", ""] + notes
    open(dst, "w", encoding="utf-8").write("\n".join(out) + "\n")
    print(f"párrafos/tablas escritos: {len(out)}; rótulos numerados: {len(labels)}")
    if pdf_txt:
        pdf = re.sub(r"\s+", " ", open(pdf_txt, encoding="utf-8").read())
        num_labels = [l for l in labels if re.match(r"^\d+(\.\d+)*\.$", l)]
        missing = [l for l in num_labels if f" {l} " not in pdf]
        print(f"rótulos numéricos: {len(num_labels)}; no encontrados en el PDF: {len(missing)}")
        for m in missing:
            print("  ", m)


if __name__ == "__main__":
    main()
