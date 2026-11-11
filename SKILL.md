---
name: directiva-software-grh
description: >-
  Documenta, audita y mantiene software institucional del Gobierno Regional Huánuco conforme a la
  Directiva N°02.S5.DI.SGMTD (desarrollo, documentación, versionamiento, licenciamiento y
  repositorios). Úsala cuando se pida documentar un sistema "según la directiva", preparar o
  actualizar los documentos del Anexo N°04 (manual de usuario, manual de instalación, diccionario
  de datos, documentación técnica) en Markdown dentro del repositorio, sincronizar la documentación
  tras cambios en el código ("actualiza documentación"), revisar o validar reglas de la directiva,
  evaluar la licencia de un software contra el Anexo N°05, generar Word/PDF con formato GOREHCO
  desde los .md, auditar el cumplimiento o incorporar una nueva versión de la directiva.
---

# Directiva de software institucional — GRH

Versión de la skill: ver `CHANGELOG.md`. Norma cargada: `references/normativa/directiva-02S5/fuente.yaml`.

## Antes de cualquier modo

1. Leer `references/protocolos/no-inventar.md` y aplicarlo a toda salida.
2. Leer `references/normativa/directiva-02S5/fuente.yaml`: la aprobación y la vigencia de la directiva están **POR-CONFIRMAR**. No computar plazos "desde la entrada en vigencia".
3. Para ubicar un tema usar `v1.0/guia-lectura.md`; para leer el texto completo, `v1.0/extraccion/directiva-literal.md`; para citar, el original (texto del .docx, página del PDF 7501018). `resumen-lectura.md` es un resumen y no se usa para citar.
4. Respetar las reglas del repositorio del proyecto (p. ej. "ESTRUCTURA PRIMERO" y reglas de git de su `CLAUDE.md`). Esta skill no ejecuta commits ni crea tags salvo pedido expreso.
5. Armar un paquete de contexto (`references/plantillas/paquete-contexto.yaml`) y cargar solo lo necesario.

## Modos

### inicializar — "documenta según la directiva"
1. Diagnóstico del repositorio: naturaleza (independiente / utilitario), modalidad, ámbito, si está en producción (si no consta: POR-CONFIRMAR), dependencias externas, documentación existente.
2. Vía de cumplimiento: hitos (7.3.1) o regularización (11.1).
3. Contrastar los insumos existentes contra el código y listar errores.
4. Proponer la estructura `docs/<proyecto>/` (plantillas en `references/plantillas/`) y **esperar aprobación** antes de crear archivos.

### actualizar documentos — "actualiza documentación"
`git diff --name-only` → documentos cuyo `cubre:` coincide → actualizar solo esas secciones y su sustento → registrar en `CHANGELOG.md` del proyecto. Si el documento está `APROBADO`, escribir en `<documento>-propuesta.md` (`references/protocolos/versiones-y-entregas.md`).

### auditar — "¿cumple la directiva?"
Recorrer las reglas aplicables (`reglas/`, según `aplica_a` y `momento`), ejecutar su `verificacion` sobre el repositorio y actualizar `cumplimiento.md`. Reportar bloqueantes y no verificables. Las reglas en `BORRADOR-IA` se usan como lista de control, sin presentarlas como validadas.

### revisar reglas — "revisemos reglas"
Seguir `references/protocolos/validacion-reglas.md`. Solo se registra `VALIDADO` con respuesta expresa del validador en la conversación.

### licenciar — "evalúa la licencia"
Matriz de dependencias desde archivos de bloqueo (`references/dependencias.md`) e informe de determinación contra el Anexo N°05 (`references/plantillas/licenciamiento.md`). Cada celda del Anexo N°05 citada se contrasta con el PDF original (la extracción está SIN-REVISAR).

### construir — "genera Word/PDF de …"
Seguir `references/build-gorehco.md`. Fuente única: el `.md` del documento. (Script pendiente — paso 8 del plan.)

### actualizar norma — "salió una nueva versión de la directiva"
Seguir `references/protocolos/actualizacion-norma.md`. La extracción literal se genera con `python3 -I scripts/extraer_docx.py <docx> <salida.md> --pdf-texto <pdftotext.txt>`.

## Estado del contenido de la skill

- Reglas: 13 piloto (6.9, 7.3.2, 7.3.3, 7.3.4, 11.1). Al 2026-11-11: 11 `VALIDADO` (6.9.1, 6.9.2, 7.3.2, 7.3.2a, 7.3.2b, 7.3.3a–c, 7.3.4a–c), 2 `BORRADOR-IA` (11.1, 11.1a). El resto de la directiva aún no está descompuesto en reglas.
- Script de construcción: pendiente.
