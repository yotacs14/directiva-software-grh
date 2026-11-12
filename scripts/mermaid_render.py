#!/usr/bin/env python3
"""
Renderizador mínimo de diagramas Mermaid a PNG sin navegador.

Cubre los tipos usados en la documentación: erDiagram, flowchart/graph,
stateDiagram-v2 (vía Graphviz `dot`) y sequenceDiagram (vía matplotlib).
No pretende cubrir toda la sintaxis de Mermaid: ante una línea no reconocida
la ignora y la informa en la lista de advertencias.

Uso como módulo:  render(codigo_mermaid, ruta_png) -> lista de advertencias
"""
import re
import subprocess
import textwrap

FONT = "Helvetica"


def _q(s):
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'


def _dot_to_png(dot, out):
    subprocess.run(["dot", "-Tpng", "-Gdpi=150", "-o", out], input=dot, text=True, check=True)


# ---------------------------------------------------------------- erDiagram
def _er(lines, out):
    warn, edges, nodes = [], [], set()
    for l in lines:
        m = re.match(r'(\w+)\s+([|}o{]{2})--([|}o{]{2})\s+(\w+)\s*:\s*"?([^"]*)"?', l.strip())
        if m:
            a, _, _, b, lab = m.groups()
            nodes |= {a, b}
            edges.append((a, b, lab))
        elif l.strip():
            warn.append(f"erDiagram: línea ignorada: {l.strip()}")
    dot = [f'digraph G {{ rankdir=LR; node [shape=box, style="rounded,filled", fillcolor="#EAF1FB", fontname="{FONT}", fontsize=10]; edge [fontname="{FONT}", fontsize=8, dir=both, arrowtail=tee, arrowhead=crow];']
    for n in sorted(nodes):
        dot.append(f"{_q(n)};")
    for a, b, lab in edges:
        dot.append(f"{_q(a)} -> {_q(b)} [label={_q(lab)}];")
    dot.append("}")
    _dot_to_png("\n".join(dot), out)
    return warn


# ---------------------------------------------------------------- flowchart
NODE = re.compile(r'([A-Za-z0-9_]+)\s*(\(\[[^\]]*\]\)|\[\([^\)]*\)\]|\[[^\]]*\]|\(\([^\)]*\)\)|\([^\)]*\)|\{[^\}]*\})?')


def _node(tok, labels, shapes):
    m = NODE.match(tok.strip())
    if not m:
        return None
    nid, raw = m.groups()
    if raw:
        if raw.startswith("(["):
            labels[nid], shapes[nid] = raw[2:-2], "ellipse"
        elif raw.startswith("[("):
            labels[nid], shapes[nid] = raw[2:-2], "cylinder"
        elif raw.startswith("(("):
            labels[nid], shapes[nid] = raw[2:-2], "circle"
        elif raw.startswith("{"):
            labels[nid], shapes[nid] = raw[1:-1], "diamond"
        elif raw.startswith("("):
            labels[nid], shapes[nid] = raw[1:-1], "box"
        else:
            labels[nid], shapes[nid] = raw[1:-1], "box"
    labels.setdefault(nid, nid)
    shapes.setdefault(nid, "box")
    return nid


def _flow(lines, header, out):
    warn = []
    direction = "LR" if re.search(r"\bLR\b", header) else "TB"
    labels, shapes, edges, groups, stack = {}, {}, [], {}, []
    for l in lines:
        s = l.strip()
        if not s:
            continue
        if s.startswith("subgraph"):
            name = s[len("subgraph"):].strip()
            stack.append(name)
            groups.setdefault(name, [])
            continue
        if s == "end":
            if stack:
                stack.pop()
            continue
        parts = re.split(r'\s*(-\.->|-->|==>|---)\s*(?:\|([^|]*)\|\s*)?', s)
        if len(parts) >= 4:
            prev = _node(parts[0], labels, shapes)
            i = 1
            while i + 2 <= len(parts) - 1 or i + 2 == len(parts):
                arrow, lab, tok = parts[i], parts[i + 1], parts[i + 2]
                nxt = _node(tok, labels, shapes)
                if prev and nxt:
                    edges.append((prev, nxt, lab or "", "dashed" if arrow == "-.->" else "solid"))
                    if stack:
                        for n in (prev, nxt):
                            if n not in sum(groups.values(), []):
                                pass
                prev = nxt
                i += 3
                if i >= len(parts):
                    break
            continue
        nid = _node(s, labels, shapes)
        if nid:
            if stack:
                groups[stack[-1]].append(nid)
        else:
            warn.append(f"flowchart: línea ignorada: {s}")
    dot = [f'digraph G {{ rankdir={direction}; compound=true; node [style="filled", fillcolor="#EAF1FB", fontname="{FONT}", fontsize=10]; edge [fontname="{FONT}", fontsize=8];']
    placed = set()
    for gi, (g, members) in enumerate(groups.items()):
        dot.append(f'subgraph cluster_{gi} {{ label={_q(g)}; fontname="{FONT}"; fontsize=10; style="rounded"; color="#9DB5D6";')
        for n in members:
            dot.append(f'{_q(n)} [label={_q(textwrap.fill(labels[n], 28))}, shape={shapes[n]}];')
            placed.add(n)
        dot.append("}")
    for n in labels:
        if n not in placed:
            dot.append(f'{_q(n)} [label={_q(textwrap.fill(labels[n], 28))}, shape={shapes[n]}];')
    for a, b, lab, st in edges:
        dot.append(f'{_q(a)} -> {_q(b)} [label={_q(lab)}, style={st}];')
    dot.append("}")
    _dot_to_png("\n".join(dot), out)
    return warn


# ---------------------------------------------------------------- stateDiagram
def _state(lines, out):
    warn, edges = [], []
    for l in lines:
        s = l.strip()
        if not s:
            continue
        m = re.match(r'(\[\*\]|\w+)\s*-->\s*(\[\*\]|\w+)\s*(?::\s*(.*))?$', s)
        if m:
            edges.append(m.groups())
        else:
            warn.append(f"stateDiagram: línea ignorada: {s}")
    dot = [f'digraph G {{ rankdir=LR; node [shape=box, style="rounded,filled", fillcolor="#EAF1FB", fontname="{FONT}", fontsize=10]; edge [fontname="{FONT}", fontsize=8];']
    for a, b, lab in edges:
        na = "inicio" if a == "[*]" else a
        nb = "fin" if b == "[*]" else b
        for n, orig in ((na, a), (nb, b)):
            if orig == "[*]":
                dot.append(f'{_q(n)} [shape=circle, label="", width=0.2, style=filled, fillcolor=black];')
        dot.append(f'{_q(na)} -> {_q(nb)} [label={_q(lab or "")}];')
    dot.append("}")
    _dot_to_png("\n".join(dot), out)
    return warn


# ---------------------------------------------------------------- sequenceDiagram
def _sequence(lines, out):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    warn, parts, alias, events = [], [], {}, []
    for l in lines:
        s = l.strip()
        if not s or s == "autonumber":
            continue
        m = re.match(r'(participant|actor)\s+(\w+)(?:\s+as\s+(.*))?$', s)
        if m:
            _, pid, name = m.groups()
            parts.append(pid)
            alias[pid] = name or pid
            continue
        m = re.match(r'(\w+)\s*(-->>|->>|-->|->)\s*(\w+)\s*:\s*(.*)$', s)
        if m:
            a, arr, b, msg = m.groups()
            for p in (a, b):
                if p not in parts:
                    parts.append(p)
                    alias[p] = p
            events.append(("msg", a, b, msg, "--" in arr))
            continue
        m = re.match(r'(alt|else|opt|loop)\s*(.*)$', s)
        if m:
            events.append(("sec", m.group(1), m.group(2)))
            continue
        if s == "end":
            events.append(("end",))
            continue
        warn.append(f"sequenceDiagram: línea ignorada: {s}")
    n = len(parts)
    rows = len(events) + 2
    fig, ax = plt.subplots(figsize=(max(8, n * 2.0), max(4, rows * 0.45)))
    ax.set_xlim(-0.5, n - 0.5)
    ax.set_ylim(-rows, 1)
    ax.axis("off")
    xs = {p: i for i, p in enumerate(parts)}
    for p, i in xs.items():
        ax.text(i, 0.4, textwrap.fill(alias[p], 16), ha="center", va="center", fontsize=8,
                bbox=dict(boxstyle="round", fc="#EAF1FB", ec="#4A6FA5"))
        ax.plot([i, i], [0, -rows + 0.5], color="#9DB5D6", lw=0.8, ls="--")
    y, k = -1, 1
    for ev in events:
        if ev[0] == "msg":
            _, a, b, msg, dashed = ev
            xa, xb = xs[a], xs[b]
            ax.annotate("", xy=(xb, y), xytext=(xa, y),
                        arrowprops=dict(arrowstyle="->", ls="--" if dashed else "-", color="#1F3B63", lw=0.9))
            ax.text((xa + xb) / 2, y + 0.12, f"{k}. {msg}", ha="center", va="bottom", fontsize=7)
            k += 1
        elif ev[0] == "sec":
            ax.text(-0.45, y + 0.1, f"[{ev[1]}] {ev[2]}", ha="left", va="bottom", fontsize=7, color="#843C0C", style="italic")
        y -= 1
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return warn


def render(code, out):
    lines = code.strip("\n").split("\n")
    head = lines[0].strip()
    body = lines[1:]
    if head.startswith("erDiagram"):
        return _er(body, out)
    if head.startswith("flowchart") or head.startswith("graph"):
        return _flow(body, head, out)
    if head.startswith("stateDiagram"):
        return _state(body, out)
    if head.startswith("sequenceDiagram"):
        return _sequence(body, out)
    raise ValueError(f"Tipo de diagrama no soportado: {head}")
