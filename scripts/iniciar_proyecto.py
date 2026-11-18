#!/usr/bin/env python3
"""Fase 0 de un proyecto nuevo conforme a la Directiva N°02.S5.DI.SGMTD (ver references/protocolos/nuevo-proyecto.md).

Uso:
    python3 iniciar_proyecto.py <ruta-del-repositorio> [--instalar] [--no-interactivo]

Hace, en orden:
  1. Verifica herramientas (pandoc, LibreOffice, Graphviz, python-docx, PyYAML, matplotlib).
     Con --instalar ejecuta los comandos de instalación que falten (pide confirmación).
  2. Enlaza la skill en ~/.claude/skills si no está.
  3. Pregunta los datos del proyecto (o usa POR-CONFIRMAR con --no-interactivo).
  4. Diagnóstico automático: versiones, autores por cantidad de commits (anonimizados en el archivo),
     archivos sensibles versionados, migraciones y conexiones.
  5. Crea docs/<sigla>/ con la ficha, decisiones, cumplimiento, los 4 documentos del Anexo N°04 y sus sustentos.
  6. Agrega al CLAUDE.md del proyecto la sección de documentación oficial.

No sobrescribe archivos existentes, no hace commits y no escribe credenciales ni datos personales.
Solo usa la biblioteca estándar de Python.
"""
import argparse, collections, datetime, importlib.util, json, os, platform, re, shutil, subprocess, sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
PLANT = SKILL / "references" / "plantillas"
HOY = datetime.date.today().isoformat()
POR = "POR-CONFIRMAR"
creados, omitidos = [], []


# ----------------------------------------------------------------- utilidades
def titulo(t):
    print(f"\n=== {t} ===")


def run(cmd, cwd=None):
    try:
        return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=120).stdout
    except Exception:
        return ""


def preguntar(txt, defecto=POR, interactivo=True):
    if not interactivo:
        return defecto
    r = input(f"  {txt} [{defecto}]: ").strip()
    return r or defecto


def escribir(ruta: Path, contenido: str):
    if ruta.exists():
        omitidos.append(ruta)
        return
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(contenido, encoding="utf-8")
    creados.append(ruta)


# ----------------------------------------------------------------- 1. herramientas
def soffice():
    for c in ("soffice", "libreoffice", "/Applications/LibreOffice.app/Contents/MacOS/soffice",
              r"C:\Program Files\LibreOffice\program\soffice.exe"):
        if shutil.which(c) or Path(c).exists():
            return c
    return None


def herramientas(instalar):
    titulo("1. Herramientas")
    so = platform.system()
    faltan = []
    checks = [("pandoc", shutil.which("pandoc")), ("LibreOffice", soffice()), ("Graphviz (dot)", shutil.which("dot"))]
    for nombre, ok in checks:
        print(f"  {'OK ' if ok else 'FALTA'}  {nombre}")
        if not ok:
            faltan.append(nombre)
    pymods = {"docx": "python-docx", "yaml": "pyyaml", "matplotlib": "matplotlib"}
    pyfaltan = [pkg for mod, pkg in pymods.items() if importlib.util.find_spec(mod) is None]
    for mod, pkg in pymods.items():
        print(f"  {'FALTA' if pkg in pyfaltan else 'OK '}  python: {pkg}")
    cmds = []
    if faltan:
        if so == "Darwin":
            m = {"pandoc": "brew install pandoc", "Graphviz (dot)": "brew install graphviz",
                 "LibreOffice": "brew install --cask libreoffice"}
        elif so == "Linux":
            m = {"pandoc": "sudo apt install -y pandoc", "Graphviz (dot)": "sudo apt install -y graphviz",
                 "LibreOffice": "sudo apt install -y libreoffice-writer"}
        else:
            m = {"pandoc": "winget install --id JohnMacFarlane.Pandoc", "Graphviz (dot)": "winget install --id Graphviz.Graphviz",
                 "LibreOffice": "winget install --id TheDocumentFoundation.LibreOffice"}
        cmds += [m[f] for f in faltan]
    if pyfaltan:
        extra = " --break-system-packages" if so == "Linux" else ""
        cmds.append(f"{sys.executable} -m pip install {' '.join(pyfaltan)}{extra}")
    if not cmds:
        print("  Todo instalado.")
        return
    print("  Comandos para instalar lo que falta:")
    for c in cmds:
        print(f"    {c}")
    if instalar and input("  ¿Ejecutarlos ahora? (s/N): ").strip().lower() == "s":
        for c in cmds:
            print(f"  > {c}")
            subprocess.run(c, shell=True)
    else:
        print("  (Solo se necesitan para generar Word/PDF; puede continuar sin ellos.)")


# ----------------------------------------------------------------- 2. skill
def enlazar_skill():
    titulo("2. Skill")
    destino = Path.home() / ".claude" / "skills" / "directiva-software-grh"
    if destino.exists():
        print(f"  Ya instalada en {destino}")
        return
    destino.parent.mkdir(parents=True, exist_ok=True)
    try:
        destino.symlink_to(SKILL, target_is_directory=True)
        print(f"  Enlazada: {destino} -> {SKILL}")
    except OSError:
        print(f"  No se pudo crear el enlace. Cópiela manualmente a {destino}")


# ----------------------------------------------------------------- 3. datos
def datos(repo, interactivo):
    titulo("3. Datos del proyecto")
    d = {}
    d["nombre"] = preguntar("Nombre del software", POR, interactivo)
    sig = "proyecto" if d["nombre"] == POR else (re.sub(r"[^A-Za-z0-9]", "", "".join(w[0] for w in d["nombre"].split() if w[0].isupper())) or "proyecto")
    d["sigla"] = preguntar("Sigla (carpeta docs/<sigla>)", sig.lower(), interactivo).lower()
    d["unidad"] = preguntar("Unidad de Organización responsable", POR, interactivo)
    d["produccion"] = preguntar("¿Está en producción? (si/no)", POR, interactivo).lower()
    d["desde"] = preguntar("En producción desde (año o fecha)", POR, interactivo) if d["produccion"].startswith("s") else "—"
    d["responsable"] = preguntar("Responsable técnico (nombre y cargo)", POR, interactivo)
    d["validador"] = preguntar("Validador de las reglas (nombre y cargo)", d["responsable"], interactivo)
    d["externos"] = preguntar("¿Participó personal externo? (si/no)", POR, interactivo).lower()
    amb = preguntar("Carpetas del ámbito, separadas por coma (vacío = todo el repositorio)", "", interactivo)
    d["ambito"] = [a.strip().strip("/") for a in amb.split(",") if a.strip()]
    for a in d["ambito"]:
        if not (repo / a).exists():
            print(f"  Aviso: la ruta {a} no existe en el repositorio.")
    return d


# ----------------------------------------------------------------- 4. diagnóstico
def diagnostico(repo, d):
    titulo("4. Diagnóstico automático")
    r = {}
    # versiones
    vers = []
    lock = repo / "composer.lock"
    if lock.exists():
        L = json.loads(lock.read_text(encoding="utf-8"))
        idx = {p["name"]: p["version"] for p in L.get("packages", [])}
        for n in ("laravel/framework", "laravel/passport", "spatie/laravel-permission", "barryvdh/laravel-dompdf"):
            if n in idx:
                vers.append((n, idx[n], "composer.lock"))
        php = json.loads((repo / "composer.json").read_text(encoding="utf-8")).get("require", {}).get("php") if (repo / "composer.json").exists() else None
        if php:
            vers.append(("php (requerido)", php, "composer.json"))
    pj = repo / "package.json"
    if pj.exists():
        P = json.loads(pj.read_text(encoding="utf-8"))
        deps = {**P.get("dependencies", {}), **P.get("devDependencies", {})}
        for n in ("vue", "vuetify", "vuex", "laravel-mix", "react", "@angular/core"):
            if n in deps:
                vers.append((n, deps[n], "package.json"))
    for f, n in (("requirements.txt", "Python (requirements)"), ("manage.py", "Django (manage.py)")):
        if (repo / f).exists():
            vers.append((n, "ver archivo", f))
    r["versiones"] = vers
    # git
    es_git = (repo / ".git").exists()
    r["git"] = es_git
    autores = collections.Counter()
    if es_git:
        out = run(["git", "--no-optional-locks", "log", "--format=%ae", "--"] + (d["ambito"] or ["."]), cwd=repo)
        autores = collections.Counter(l.strip().lower() for l in out.splitlines() if l.strip())
        r["primer_commit"] = run(["git", "--no-optional-locks", "log", "--reverse", "--format=%ad", "--date=short", "--"] + (d["ambito"] or ["."]), cwd=repo).split("\n")[0]
    r["autores"] = autores
    if autores:
        print("  Commits por autor en el ámbito (solo en pantalla; el archivo los anonimiza):")
        for a, n in autores.most_common():
            print(f"    {n:6d}  {a}")
    # sensibles
    sens = []
    if es_git:
        tracked = run(["git", "--no-optional-locks", "ls-files"], cwd=repo).splitlines()
        pat = re.compile(r"(^|/)(\.env(\.[a-z]+)?|.*\.key|.*\.pem|.*\.p12|.*\.pfx|id_rsa|id_ed25519)$", re.I)
        sens += [f"{t} (archivo versionado)" for t in tracked if pat.search(t) and not t.endswith(".env.example")]
        g = run(["git", "--no-optional-locks", "grep", "-l", "-I", "-i", "-E",
                 r"client_secret['\"]?\s*(=>|=|:)\s*['\"][A-Za-z0-9_\-]{8,}|BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY|AKIA[0-9A-Z]{16}",
                 "--", ".", ":!*.min.*", ":!public/", ":!vendor/", ":!node_modules/", ":!*.lock", ":!*.map"], cwd=repo)
        sens += [f"{t} (posible credencial en el código)" for t in g.splitlines() if t]
    gi = (repo / ".gitignore").read_text(encoding="utf-8", errors="ignore") if (repo / ".gitignore").exists() else ""
    r["gitignore_env"] = bool(re.search(r"^/?\.env\s*$", gi, re.M))
    r["sensibles"] = sens
    print(f"  Archivos sensibles a revisar: {len(sens)}")
    # base de datos
    mig = repo / "database" / "migrations"
    r["migraciones"] = len(list(mig.glob("*.php"))) if mig.exists() else None
    conns = []
    dbc = repo / "config" / "database.php"
    if dbc.exists():
        txt = dbc.read_text(encoding="utf-8", errors="ignore")
        bloque = txt.split("'connections'", 1)[-1].split("'migrations'", 1)[0]
        conns = re.findall(r"^\s{8}'([\w-]+)'\s*=>\s*\[", bloque, re.M)
    r["conexiones"] = conns
    return r


# ----------------------------------------------------------------- 5. estructura
ENC = (PLANT / "_encabezado-documento.md").read_text(encoding="utf-8") if (PLANT / "_encabezado-documento.md").exists() else ""
SECCIONES = {
    "manual-instalacion": ("Manual de Instalación y Configuración", ["1. Datos generales", "2. Requisitos de hardware", "3. Requisitos de software", "4. Proceso de instalación", "5. Proceso de configuración", "6. Contacto institucional"]),
    "manual-usuario": ("Manual de Usuario", ["1. Datos generales", "2. Funcionalidad del software"]),
    "diccionario-datos": ("Diccionario de Datos", ["1. Modelo de datos", "2. Diccionario de datos"]),
    "documentacion-tecnica": ("Documentación Técnica de Desarrollo", ["1. Requerimientos", "2. Análisis", "3. Diseño", "4. Arquitectura y componentes", "5. Plan de pruebas funcionales y no funcionales", "6. Manual de operaciones"]),
}


def documento(clave, d):
    tit, secs = SECCIONES[clave]
    enc = ENC.replace('"<Tipo de documento> del <Nombre del software>"', f'"{tit} del {d["nombre"]}"')
    enc = re.sub(r"^tipo: manual-usuario[^\n]*", f"tipo: {clave}", enc, flags=re.M)
    enc = enc.replace("unidad_responsable: POR-CONFIRMAR", f"unidad_responsable: {d['unidad']}")
    enc = enc.replace("version_software: POR-CONFIRMAR", "version_software: 1.0.0")
    enc = enc.replace("sustento: <documento>-sustento.md", f"sustento: {clave}-sustento.md")
    enc = enc.replace("cubre: []", "cubre: [" + ", ".join(f'"{a}/**"' for a in d["ambito"]) + "]")
    enc = enc.replace("[Tipo de documento]", tit).replace("[Nombre de la entidad]", "Gobierno Regional Huánuco")
    cuerpo = "\n\n".join(f"## {s}\n\nPENDIENTE." for s in secs)
    enc = enc.replace("<!-- ... cuerpo del documento según su plantilla ... -->", f"# {tit} del {d['nombre']}\n\n{cuerpo}")
    return enc.replace("<licencia_documento>", "CC BY-SA 4.0 (si se determina licencia libre)").replace("<licencia_software>", POR)


def sustento(clave):
    t = (PLANT / "sustento.md").read_text(encoding="utf-8")
    return t.replace("<documento>", clave).replace("AAAA-MM-DD", HOY)


def estructura(repo, d, r):
    titulo("5. Estructura docs/" + d["sigla"])
    base = repo / "docs" / d["sigla"]
    S = d["sigla"].upper()
    prod = d["produccion"].startswith("s")
    via = "Regularización (numeral 11.1); plazo de 60 días hábiles desde el 22/09/2026" if prod else ("Hitos (numeral 7.3)" if d["produccion"].startswith("n") else POR)
    amb = ", ".join(f"`{a}`" for a in d["ambito"]) or "todo el repositorio"
    modal = POR if d["externos"] == POR else ("Mixta (personal propio y externo)" if d["externos"].startswith("s") else "Interna")
    ficha = (PLANT / "indice-proyecto.md").read_text(encoding="utf-8")
    ficha = ficha.replace("AAAA-MM-DD", HOY).replace("<NOMBRE>", d["nombre"])
    ficha = re.sub(r"<!-- Guardar como .*?-->\n", "", ficha)
    for campo, valor, fuente in [
        ("Nombre", d["nombre"], "—"),
        ("Modalidad de desarrollo (6.1.8–6.1.10)", modal, f"Declaración del responsable ({HOY})"),
        ("Ámbito en el repositorio", amb, "DEC-001"),
        ("Versión declarada", "1.0.0 (sin tag)", "DEC-002"),
        ("En producción", f"{'Sí, desde ' + d['desde'] if prod else d['produccion']}", f"Declaración del responsable ({HOY})"),
        ("Vía de cumplimiento", via, "DEC-003"),
    ]:
        ficha = re.sub(rf"^\| {re.escape(campo)} \|.*$", f"| {campo} | {valor} | {fuente} |", ficha, flags=re.M)
    ficha = ficha.replace("| Naturaleza (6.1.3 / 6.1.14) | solución independiente / componente utilitario |  |", f"| Naturaleza (6.1.3 / 6.1.14) | {POR} |  |")
    ficha = ficha.replace("| Licencia del software | POR-CONFIRMAR | informe de determinación |", "| Licencia del software | POR-CONFIRMAR | informe de determinación |\n| Responsable técnico | " + d["responsable"] + " | Declaración |\n| Validador de reglas | " + d["validador"] + " | Declaración |")
    escribir(base / f"00-{S}.md", ficha)
    escribir(base / "decisiones.md", f"""---
tipo: decisiones
fecha_actualizacion: {HOY}
---

# Decisiones — {d['nombre']}

| ID | Fecha | Decisión | Sustento |
|---|---|---|---|
| DEC-001 | {HOY} | Ámbito del software en el repositorio: {amb} | Declaración del responsable |
| DEC-002 | {HOY} | Versión declarada 1.0.0 (estructura X.Y.Z, numeral 7.3.2) | Primera versión estable |
| DEC-003 | {HOY} | Vía de cumplimiento: {via} | Estado de producción declarado |
""")
    escribir(base / "cumplimiento.md", (PLANT / "cumplimiento.md").read_text(encoding="utf-8").replace("AAAA-MM-DD", HOY))
    for clave in SECCIONES:
        escribir(base / f"{clave}.md", documento(clave, d))
        escribir(base / f"{clave}-sustento.md", sustento(clave))
    escribir(base / "titularidad.md", f"""---
tipo: titularidad
fecha_actualizacion: {HOY}
---

# Titularidad — {d['nombre']}

Base: numerales 6.3.1, 6.3.2 y Anexo N°01. Titular: Gobierno Regional Huánuco.

| Aspecto | Estado | Fuente |
|---|---|---|
| Modalidad | {modal} | Declaración del responsable |
| Commits en el ámbito | Ver `diagnostico-inicial.md` (autores anonimizados) | `git log` |
| Cesión de derechos del personal externo | PENDIENTE: un Anexo N°01 por persona externa con commits; los archivos con datos personales van fuera del repositorio | 6.3.2 |
""")
    escribir(base / "seguridad.md", f"""---
tipo: seguridad
fecha_actualizacion: {HOY}
---

# Seguridad y datos personales — {d['nombre']}

Base: numerales 6.5 y 6.6. Este documento no reproduce valores de credenciales.

## Hallazgos

| ID | Hallazgo | Regla | Estado |
|---|---|---|---|
""" + "".join(f"| S{i} | {s} | 6.6.1 | POR-REVISAR |\n" for i, s in enumerate(r["sensibles"], 1)) + f"""
## Revisiones pendientes en producción

- `APP_ENV` y `APP_DEBUG` del `.env` del servidor (verificar sin copiar valores).
- Cómo se reinicia PHP en el servidor (`systemctl list-units --type=service | grep -i -E "php|apache"`).
- Rutas que responden sin sesión (análisis de rutas + prueba sin sesión + log de Apache).

## Datos personales tratados

PENDIENTE.
""")
    escribir(base / "licenciamiento" / "matriz-dependencias.md", (PLANT / "licenciamiento.md").read_text(encoding="utf-8").split("## B.")[0].replace("# Plantillas de licenciamiento\n\n## A. ", "# "))
    escribir(base / "_build" / "INSTRUCCIONES.md", f"""# Construcción de Word/PDF — {d['nombre']}

```bash
python3 -I {SKILL}/scripts/build_docx.py docs/{d['sigla']}/<documento>.md <carpeta-salida-fuera-del-repo> \\
  --pie "Versión <version>  |  {datetime.date.today().year}  |  {d['unidad']}  |  Gobierno Regional Huánuco" --pdf
```

Los Word/PDF no se versionan en el repositorio.
""")
    (base / "img").mkdir(parents=True, exist_ok=True)
    # diagnóstico
    aut = r["autores"]
    filas_aut = "".join(f"| Autor {i} | {n} |\n" for i, (_, n) in enumerate(aut.most_common(), 1)) or "| — | — |\n"
    filas_ver = "".join(f"| {n} | {v} | `{f}` |\n" for n, v, f in r["versiones"]) or "| — | — | — |\n"
    filas_sen = "".join(f"| {s} |\n" for s in r["sensibles"]) or "| Ninguno detectado |\n"
    escribir(base / "diagnostico-inicial.md", f"""---
tipo: diagnostico
fecha: {HOY}
generado_con: scripts/iniciar_proyecto.py (skill directiva-software-grh)
---

# Diagnóstico inicial — {d['nombre']}

Datos obtenidos automáticamente del repositorio. Verificar en el servidor antes de documentarlos como definitivos.

## Versiones declaradas en el código

| Componente | Versión | Fuente |
|---|---|---|
{filas_ver}
## Base de datos

- Migraciones: {r['migraciones'] if r['migraciones'] is not None else 'no aplica / no encontradas'}
- Conexiones en `config/database.php`: {', '.join(f'`{c}`' for c in r['conexiones']) or '—'}

## Commits en el ámbito (autores anonimizados)

Primer commit del ámbito: {r.get('primer_commit') or '—'}

| Autor | Commits |
|---|---|
{filas_aut}
## Archivos sensibles a revisar (solo nombres)

| Archivo |
|---|
{filas_sen}
`.env` en `.gitignore`: {'sí' if r['gitignore_env'] else 'NO — agregarlo'}
""")


# ----------------------------------------------------------------- 6. CLAUDE.md
def claude_md(repo, d):
    titulo("6. CLAUDE.md")
    p = repo / "CLAUDE.md"
    marca = f"## DOCUMENTACION OFICIAL ({d['sigla'].upper()}) — Directiva N°02.S5.DI.SGMTD"
    txt = p.read_text(encoding="utf-8") if p.exists() else ""
    if marca in txt:
        print("  La sección ya existe.")
        return
    sec = f"""

{marca}

- `docs/{d['sigla']}/` contiene los entregables de la directiva. Aplicar la skill `directiva-software-grh`
  y su protocolo de no inventar: lo no verificado se escribe `POR-CONFIRMAR` / `PENDIENTE`.
- Al pedir "actualiza documentacion": `git diff --name-only` → documentos cuyo campo `cubre:` coincida →
  actualizar la sección y su `*-sustento.md`.
- Nunca versionar credenciales, claves privadas ni datos personales reales (numeral 6.6).
- Documento con `estado: APROBADO` → no se edita; los cambios van en `<doc>-propuesta.md`.
- Git: no generar texto de commit ni ejecutar commits salvo pedido expreso.
"""
    p.write_text(txt + sec, encoding="utf-8")
    creados.append(p)
    print("  Sección agregada.")


# ----------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("repo")
    ap.add_argument("--instalar", action="store_true", help="instalar las herramientas que falten (pide confirmación)")
    ap.add_argument("--no-interactivo", action="store_true", help="no preguntar; usar POR-CONFIRMAR")
    a = ap.parse_args()
    repo = Path(a.repo).expanduser().resolve()
    if not repo.is_dir():
        sys.exit(f"No existe la carpeta {repo}")
    print(f"Proyecto: {repo}\nSkill:    {SKILL}")
    herramientas(a.instalar)
    enlazar_skill()
    d = datos(repo, not a.no_interactivo)
    r = diagnostico(repo, d)
    estructura(repo, d, r)
    claude_md(repo, d)
    titulo("Resultado")
    for c in creados:
        print(f"  creado   {c.relative_to(repo) if repo in c.parents else c}")
    for o in omitidos:
        print(f"  existía  {o.relative_to(repo)} (no se tocó)")
    print(f"""
Siguientes pasos (references/protocolos/nuevo-proyecto.md):
  1. Revisar docs/{d['sigla']}/diagnostico-inicial.md y completar los POR-CONFIRMAR de la ficha.
  2. Abrir Claude en el repositorio y pedir: "inicializa {d['sigla']} según la directiva" (Fase 1).
  3. Si hay archivos sensibles: agregarlos a .gitignore ANTES de `git rm --cached`.
No se hizo ningún commit.""")


if __name__ == "__main__":
    main()
