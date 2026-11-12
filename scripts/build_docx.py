#!/usr/bin/env python3
"""
Construye Word (.docx) y PDF con formato GOREHCO a partir de un documento Markdown
de la documentación (ver references/build-gorehco.md).

Uso:
    python3 -I build_docx.py <documento.md> <carpeta_salida> [--pie "<texto pie>"] [--pdf] [--sin-saltos]

--sin-saltos: no fuerza página nueva después del índice de contenido.

- Única fuente: el .md indicado (su encabezado YAML da título y versión).
- No exporta los *-sustento.md.
- Diagramas Mermaid -> PNG con mermaid_render.py (Graphviz/matplotlib, sin navegador).
- Requiere: pandoc, python-docx, PyYAML, graphviz (dot), matplotlib; LibreOffice para --pdf.
- Se ejecuta en el entorno del agente, nunca dentro del proyecto documentado.
"""
import os, re, sys, shutil, subprocess, tempfile, datetime
import yaml
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from mermaid_render import render  # noqa: E402

LOGO = os.path.join(HERE, "..", "assets", "logo_gorehco.jpeg")
AZUL, BLANCO, GRIS, GRIS_TXT = "2E75B6", "FFFFFF", "F2F2F2", "595959"


# ------------------------------------------------------------------ utilidades XML
def shd(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr()
    for e in tcPr.findall(qn("w:shd")):
        tcPr.remove(e)
    s = OxmlElement("w:shd")
    s.set(qn("w:val"), "clear"); s.set(qn("w:color"), "auto"); s.set(qn("w:fill"), fill)
    tcPr.append(s)


def vmerge(cell, restart):
    tcPr = cell._tc.get_or_add_tcPr()
    vm = OxmlElement("w:vMerge")
    if restart:
        vm.set(qn("w:val"), "restart")
    tcPr.append(vm)


def valign(cell, v="center"):
    tcPr = cell._tc.get_or_add_tcPr()
    el = OxmlElement("w:vAlign"); el.set(qn("w:val"), v); tcPr.append(el)


def borders(tbl):
    tblPr = tbl._tbl.tblPr
    b = OxmlElement("w:tblBorders")
    for side in ("top", "left", "bottom", "right", "insideH", "insideV"):
        e = OxmlElement(f"w:{side}")
        e.set(qn("w:val"), "single"); e.set(qn("w:sz"), "4"); e.set(qn("w:color"), "808080")
        b.append(e)
    tblPr.append(b)


def field_run(p, instr, sz=16):
    for kind in ("begin", None, "end"):
        r = OxmlElement("w:r"); rPr = OxmlElement("w:rPr")
        s = OxmlElement("w:sz"); s.set(qn("w:val"), str(sz)); rPr.append(s); r.append(rPr)
        if kind:
            fc = OxmlElement("w:fldChar"); fc.set(qn("w:fldCharType"), kind); r.append(fc)
        else:
            it = OxmlElement("w:instrText"); it.text = f" {instr} "
            it.set("{http://www.w3.org/XML/1998/namespace}space", "preserve"); r.append(it)
        p._p.append(r)


# ------------------------------------------------------------------ preprocesado
def preprocess(md_path, tmp):
    raw = open(md_path, encoding="utf-8").read()
    meta = {}
    if raw.startswith("---"):
        _, fm, raw = raw.split("---", 2)
        meta = yaml.safe_load(fm) or {}
    warnings = []
    for c in re.findall(r"<!--(.*?)-->", raw, re.S):
        if "CAPTURA" in c:
            warnings.append("Captura pendiente: " + " ".join(c.split())[:140])
    raw = re.sub(r"<!--.*?-->", "", raw, flags=re.S)
    # primer título H1 se usa en la portada; se retira del cuerpo
    raw = re.sub(r"^# .*\n", "", raw, count=1, flags=re.M)
    # Mermaid -> PNG
    n = [0]

    def mm(m):
        n[0] += 1
        out = os.path.join(tmp, f"diagrama_{n[0]:02d}.png")
        try:
            w = render(m.group(1), out)
            warnings.extend(w)
            return f"\n![Diagrama {n[0]}]({out})\n"
        except Exception as e:  # el diagrama queda como código
            warnings.append(f"Diagrama {n[0]} no renderizado: {e}")
            return m.group(0)
    raw = re.sub(r"```mermaid\n(.*?)```", mm, raw, flags=re.S)
    # Avisos estilo GitHub
    raw = re.sub(r"> \[!(NOTE|IMPORTANT|CAUTION|WARNING|TIP)\]\n(?:> )?",
                 lambda m: "> **" + {"NOTE": "Nota", "IMPORTANT": "Importante", "CAUTION": "Precaución",
                                     "WARNING": "Advertencia", "TIP": "Sugerencia"}[m.group(1)] + ":** ", raw)
    raw = re.sub(r"(^>(?! ?[*-] )[^\n]*\S[^\n]*\n)(> ?[*-] )", lambda m: m.group(1) + ">\n" + m.group(2), raw, flags=re.M)
    for p in re.findall(r"!\[[^\]]*\]\(([^)]+)\)", raw):
        full = p if os.path.isabs(p) else os.path.join(os.path.dirname(md_path), p)
        if not os.path.exists(full):
            warnings.append(f"Imagen inexistente: {p}")
    pc = len(re.findall(r"POR-CONFIRMAR|PENDIENTE", raw))
    if pc:
        warnings.append(f"El documento contiene {pc} marcas POR-CONFIRMAR/PENDIENTE")
    src = os.path.join(tmp, "doc.md")
    open(src, "w", encoding="utf-8").write(raw)
    return meta, src, warnings


# ------------------------------------------------------------------ documento de referencia
def reference_docx(tmp):
    ref = os.path.join(tmp, "ref.docx")
    with open(ref, "wb") as f:
        f.write(subprocess.run(["pandoc", "--print-default-data-file", "reference.docx"],
                               capture_output=True, check=True).stdout)
    d = Document(ref)
    for st in d.styles:
        try:
            if st.font is not None:
                st.font.name = "Arial"
                rpr = st.element.get_or_add_rPr()
                rf = rpr.find(qn("w:rFonts"))
                if rf is None:
                    rf = OxmlElement("w:rFonts"); rpr.append(rf)
                for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
                    rf.set(qn(a), "Arial")
        except Exception:
            pass
    sizes = {"Normal": 10, "Body Text": 10, "First Paragraph": 10, "Compact": 9.5,
             "Heading 1": 13, "Heading 2": 11.5, "Heading 3": 10.5, "Heading 4": 10}
    for name, sz in sizes.items():
        try:
            st = d.styles[name]; st.font.size = Pt(sz)
            if name.startswith("Heading"):
                st.font.bold = True
                st.font.color.rgb = RGBColor.from_string(AZUL if name in ("Heading 1", "Heading 2") else "1F3B63")
        except KeyError:
            pass
    for name in ("Source Code", "Verbatim Char"):
        try:
            d.styles[name].font.name = "Courier New"; d.styles[name].font.size = Pt(8.5)
        except KeyError:
            pass
    d.save(ref)
    return ref


# ------------------------------------------------------------------ post-procesado
def header(section, titulo, version):
    hdr = section.header
    hdr.is_linked_to_previous = False
    for p in hdr.paragraphs:
        p.clear()
    t = hdr.add_table(rows=2, cols=3, width=Cm(15.5))
    borders(t)
    W = (Cm(4.15), Cm(8.45), Cm(2.90))
    c = t.rows[0].cells
    for i, w in enumerate(W):
        c[i].width = w; t.rows[1].cells[i].width = w
    vmerge(c[0], True); vmerge(t.rows[1].cells[0], False)
    vmerge(c[1], True); vmerge(t.rows[1].cells[1], False)
    p = c[0].paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run().add_picture(LOGO, width=Cm(3.86), height=Cm(1.18))
    p = c[1].paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(titulo.upper()); r.bold = True; r.font.size = Pt(9)
    valign(c[1])
    p = c[2].paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("Página: "); r.font.size = Pt(8)
    field_run(p, "PAGE"); r = p.add_run(" de "); r.font.size = Pt(8); field_run(p, "NUMPAGES")
    p = t.rows[1].cells[2].paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(f"Versión: {version}"); r.font.size = Pt(8)


def footer(section, texto):
    f = section.footer; f.is_linked_to_previous = False
    p = f.paragraphs[0]; p.clear(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(texto); r.font.size = Pt(8); r.font.color.rgb = RGBColor.from_string(GRIS_TXT)


def _text(cell):
    return " ".join(p.text for p in cell.paragraphs).strip()


def set_widths(t, total_cm=15.5):
    """Anchos de columna según el contenido: mínimo por la palabra más larga,
    el resto proporcional a la longitud media del texto de la columna."""
    rows = t.rows
    ncols = max(len(r.cells) for r in rows)
    if ncols == 0:
        return
    longest, hlong, avg = [0] * ncols, [0] * ncols, [0.0] * ncols
    for ci in range(ncols):
        lens = []
        for ri, r in enumerate(rows):
            if ci < len(r.cells):
                tx = _text(r.cells[ci])
                if ri > 0:
                    lens.append(len(tx))
                for w in tx.split():
                    if ri == 0:
                        hlong[ci] = max(hlong[ci], len(w))
                    else:
                        longest[ci] = max(longest[ci], len(w))
        avg[ci] = sum(lens) / max(1, len(lens))
    cm_char = 0.21
    mins = [max(min(h * 0.26 + 0.35, 2.8), min(lw * cm_char + 0.3, 3.6), 1.1) for h, lw in zip(hlong, longest)]
    if sum(mins) > total_cm:
        mins = [m * total_cm / sum(mins) for m in mins]
    rest = total_cm - sum(mins)
    weights = [max(a, 1) ** 0.9 for a in avg]
    widths = [m + rest * w / sum(weights) for m, w in zip(mins, weights)]
    tbl = t._tbl
    tblPr = tbl.tblPr
    for tag in ("w:tblW", "w:tblLayout"):
        for e in tblPr.findall(qn(tag)):
            tblPr.remove(e)
    tw = OxmlElement("w:tblW"); tw.set(qn("w:w"), str(int(total_cm * 567))); tw.set(qn("w:type"), "dxa"); tblPr.append(tw)
    lay = OxmlElement("w:tblLayout"); lay.set(qn("w:type"), "fixed"); tblPr.append(lay)
    grid = tbl.tblGrid
    for g in list(grid):
        grid.remove(g)
    for w in widths:
        gc = OxmlElement("w:gridCol"); gc.set(qn("w:w"), str(int(w * 567))); grid.append(gc)
    for r in rows:
        for ci, c in enumerate(r.cells):
            if ci < ncols:
                c.width = Cm(widths[ci])


def spacing_header(section):
    p = section.header.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.space_before = Pt(0)


def page_breaks(doc):
    """Índice de contenido y glosa de licencia en páginas propias: página nueva antes del
    primer y del segundo encabezado de mayor nivel. El resto fluye sin saltos forzados."""
    heads = [p for p in doc.paragraphs if p.style is not None and p.style.name.startswith("Heading ")
             and p.style.name.split()[-1].isdigit()]
    if not heads:
        return
    top = min(int(p.style.name.split()[-1]) for p in heads)
    tops = [p for p in heads if int(p.style.name.split()[-1]) == top]
    for p in tops[:2]:
        p.paragraph_format.page_break_before = True


def justify(doc):
    """Justifica los párrafos de texto del cuerpo de varias líneas. No justifica títulos, imágenes,
    celdas de tabla, párrafos con saltos de línea manuales ni textos breves (< 160 caracteres)."""
    for p in doc.paragraphs:
        st = p.style.name if p.style is not None else ""
        if st.startswith("Heading") or st in ("TOC Heading", "Title", "Subtitle", "Image Caption", "Captioned Figure"):
            continue
        if p._p.xpath(".//w:drawing") or not p.text.strip():
            continue
        # Con saltos de línea manuales cada línea se estira; y los textos breves
        # (una o dos líneas) se ven mejor alineados a la izquierda.
        if p._p.xpath(".//w:br") or len(p.text.strip()) < 160:
            continue
        if p.alignment in (WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.RIGHT):
            continue
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

def keep_together(t, max_rows=20, max_chars=1200):
    """Encabezado de tabla repetido en cada página; filas no se parten;
    tablas breves se mantienen en una sola página."""
    first = t.rows[0]._tr.get_or_add_trPr()
    h = OxmlElement("w:tblHeader"); h.set(qn("w:val"), "true"); first.append(h)
    for r in t.rows:
        cs = OxmlElement("w:cantSplit"); cs.set(qn("w:val"), "true"); r._tr.get_or_add_trPr().append(cs)
    chars = sum(len(_text(c)) for r in t.rows for c in r.cells)
    if len(t.rows) <= max_rows and chars <= max_chars:
        for r in t.rows[:-1]:
            for c in r.cells:
                for p in c.paragraphs:
                    p.paragraph_format.keep_with_next = True


def style_tables(doc):
    for t in doc.tables:
        borders(t)
        set_widths(t)
        keep_together(t)
        for ri, row in enumerate(t.rows):
            for cell in row.cells:
                if ri == 0:
                    shd(cell, AZUL)
                    for p in cell.paragraphs:
                        for r in p.runs:
                            r.font.bold = True; r.font.color.rgb = RGBColor.from_string(BLANCO); r.font.size = Pt(9)
                else:
                    if ri % 2 == 0:
                        shd(cell, GRIS)
                    for p in cell.paragraphs:
                        for r in p.runs:
                            r.font.size = Pt(9)


def fit_images(doc, max_w=Cm(15.5)):
    for shape in doc.inline_shapes:
        if shape.width > max_w:
            ratio = max_w / shape.width
            shape.width = int(shape.width * ratio); shape.height = int(shape.height * ratio)


def cover(doc, meta, titulo):
    body = doc.element.body
    first = body[0]
    elems = []

    def para(text, size, bold=False, color=None, space=6):
        p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(space)
        r = p.add_run(text); r.bold = bold; r.font.size = Pt(size)
        if color:
            r.font.color.rgb = RGBColor.from_string(color)
        elems.append(p._p)
        return p
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run().add_picture(LOGO, width=Cm(7)); elems.append(p._p)
    para("GOBIERNO REGIONAL HUÁNUCO", 13, True, space=2)
    para(str(meta.get("unidad_responsable", "")).upper(), 11, True, space=40)
    para(titulo.upper(), 16, True, AZUL, space=30)
    fecha = str(meta.get("fecha_actualizacion", datetime.date.today()))
    para(f"Versión del documento: {meta.get('version_documento', '')}   ·   Versión del software: {meta.get('version_software', '')}", 10)
    para(f"Estado: {meta.get('estado', '')}   ·   Fecha: {fecha}", 10, space=30)
    t = doc.add_table(rows=4, cols=3); borders(t)
    for i, h in enumerate(("Etapa", "Nombre y cargo", "Firma")):
        t.rows[0].cells[i].text = h
    for i, h in enumerate(("Elaborado por", "Revisado por", "Aprobado por"), 1):
        t.rows[i].cells[0].text = h
    elems.append(t._tbl)
    pb = doc.add_paragraph(); pb.add_run().add_break(__import__("docx").enum.text.WD_BREAK.PAGE); elems.append(pb._p)
    for e in elems:
        first.addprevious(e)


def build(md_path, out_dir, pie, pdf, saltos=True):
    tmp = tempfile.mkdtemp()
    meta, src, warnings = preprocess(md_path, tmp)
    titulo = meta.get("titulo") or os.path.basename(md_path)
    ref = reference_docx(tmp)
    base = os.path.splitext(os.path.basename(md_path))[0]
    final_dir = out_dir
    out_dir = os.path.join(tmp, "salida"); os.makedirs(out_dir)  # LibreOffice deja temporales: se construye fuera
    out = os.path.join(out_dir, f"{base}.docx")
    subprocess.run(["pandoc", src, "-f", "markdown+pipe_tables+yaml_metadata_block-implicit_figures",
                    "-o", out, "--reference-doc", ref, "--toc", "--toc-depth=2",
                    "--resource-path", os.path.dirname(md_path) + os.pathsep + tmp,
                    "-M", "toc-title=Índice de contenido"], check=True)
    doc = Document(out)
    s = doc.sections[0]
    s.page_width, s.page_height = Cm(21), Cm(29.7)
    s.left_margin, s.right_margin, s.top_margin, s.bottom_margin = Cm(3), Cm(2.5), Cm(2.3), Cm(2.3)
    style_tables(doc)
    fit_images(doc)
    if saltos:
        page_breaks(doc)
    justify(doc)
    cover(doc, meta, titulo)
    header(s, titulo, meta.get("version_documento", ""))
    spacing_header(s)
    footer(s, pie.replace("<version>", str(meta.get("version_documento", ""))))
    doc.save(out)
    # Word actualiza índice y campos al abrir
    st = doc.settings.element
    uf = OxmlElement("w:updateFields"); uf.set(qn("w:val"), "true"); st.append(uf)
    doc.save(out)
    if pdf:
        subprocess.run(["/usr/bin/python3", os.path.join(HERE, "uno_pdf.py"), out,
                        os.path.join(out_dir, f"{base}.pdf")], timeout=600, check=True)
    os.makedirs(final_dir, exist_ok=True)
    for ext in (".docx", ".pdf"):
        f = os.path.join(out_dir, base + ext)
        if os.path.exists(f):
            shutil.copy(f, os.path.join(final_dir, base + ext))
    shutil.rmtree(tmp, ignore_errors=True)
    return os.path.join(final_dir, base + ".docx"), warnings


if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) < 2:
        sys.exit(__doc__)
    pie = a[a.index("--pie") + 1] if "--pie" in a else "Versión <version>"
    out, w = build(a[0], a[1], pie, "--pdf" in a, "--sin-saltos" not in a)
    print("Generado:", out)
    for x in w:
        print("  ADVERTENCIA:", x)
