# Changelog

## 0.3.4 — 2026-11-12 (borrador, no publicado)

- Justificado selectivo: no se justifican párrafos con saltos de línea manuales ni textos breves (< 160 caracteres), que se estiraban (p. ej. notas con listas cortas).

## 0.3.3 — 2026-11-12 (borrador, no publicado)

- Índice de contenido y glosa de licencia en páginas propias (salto antes del primer y del segundo encabezado de mayor nivel); el resto fluye.
- Párrafos de texto del cuerpo justificados (no títulos, imágenes ni celdas de tabla).

## 0.3.2 — 2026-11-12 (borrador, no publicado)

- Saltos de página: solo el índice de contenido ocupa página propia; el cuerpo empieza en página nueva y luego fluye sin saltos por sección (evita hojas con pocas líneas). `--sin-saltos` desactiva también ese salto.

## 0.3.1 — 2026-11-12 (borrador, no publicado)

- Cada sección general (encabezado de mayor nivel) empieza en página nueva; opción `--sin-saltos` para documentos breves.
- Tablas: anchos de columna calculados según el contenido (palabra más larga del encabezado y del cuerpo; resto proporcional al texto), diseño fijo, fila de encabezado repetida en cada página, filas que no se parten y tablas breves que no se separan de su encabezado.
- Separación entre la cabecera de página y el cuerpo.
- Listas dentro de recuadros de nota se muestran como viñetas.

## 0.3.0 — 2026-11-12 (borrador, no publicado)

- `scripts/build_docx.py`: construye Word y PDF con formato GOREHCO desde un `.md` (portada con tabla de firmas, cabecera con logo y `Página X de N`, pie, índice de contenido, tablas con estilo, imágenes ajustadas, advertencias de capturas e imágenes faltantes y de marcas POR-CONFIRMAR).
- `scripts/mermaid_render.py`: diagramas Mermaid (erDiagram, flowchart/graph, stateDiagram, sequenceDiagram) a PNG con Graphviz y matplotlib, sin navegador.
- `scripts/uno_pdf.py`: exportación a PDF con LibreOffice actualizando índices y campos.
- Limitaciones conocidas: no numera figuras ni tablas automáticamente; no genera índices de figuras y tablas ni hoja de control de cambios.

## 0.2.0 — 2026-11-10 (borrador, no publicado)

- Extracción literal `directiva-literal.md` generada automáticamente del .docx (`scripts/extraer_docx.py`), con la numeración de Word reconstruida: 121/121 rótulos coinciden con el render del .docx.
- La extracción anterior se renombra `resumen-lectura.md` y se marca como resumen (no citar). Sus capítulos pasan a numeración romana (I–XII), como en el original.
- Primera sesión de validación (2026-11-09): 6.9.2, 7.3.2, 7.3.2 a) y 7.3.2 b) VALIDADO; 6.9.1 OBSERVADO (duda originada en el resumen, no en el texto citado). Revisor NO-REGISTRADO por decisión del validador.
- Protocolo de validación: admite revisor NO-REGISTRADO.
- Segunda sesión (2026-11-10/11): 6.9.1 VALIDADO tras la extracción literal; 7.3.3 a)–c) y 7.3.4 a)–c) VALIDADO tal como se presentaron. 11.1 y 11.1 a) VALIDADO el 2026-11-11: las 13 reglas piloto quedan validadas (vigencia POR-CONFIRMAR).
- Corrección en 11.1 a): la observación sobre el rótulo "a." era un error de la conversión inicial; el .docx y el PDF muestran a) y b).
- `CLAUDE.md` con reglas de mantenimiento del repositorio (estructura primero, git, no inventar, normativa, validación).
- Hallazgo sobre el original: el .docx tiene numeraciones que Word continúa entre listas distintas (6.1.9–6.1.18, 6.3.3); se reconstruyeron igual que en el render del documento.

## 0.1.0 — 2026-11-09 (borrador, no publicado)

- Originales de la Directiva N°02.S5.DI.SGMTD – V1.0 registrados con SHA-256 (.docx, PDF SGD 7501018, Anexos .docx, Anexo 05 PDF).
- Ficha de la norma (`fuente.yaml`): aprobación y vigencia POR-CONFIRMAR.
- Extracción en Markdown (documento de lectura) y guía de lectura con páginas del PDF.
- 13 reglas piloto en `BORRADOR-IA`: 6.9.1, 6.9.2, 7.3.2, 7.3.2 a), 7.3.2 b), 7.3.3 a), b), c), 7.3.4 a), b), c), 11.1, 11.1 a). Texto citado extraído del .docx y verificado como idéntico en el PDF.
- Protocolos: no inventar, validación de reglas, versiones y entregas, actualización de la norma.
- Plantillas: encabezado con glosa (Anexo 06), documentos del Anexo 04 y 04-A, sustento, índice de proyecto, cumplimiento, licenciamiento (Anexos 03 y 07), paquete de contexto.
- Especificación de construcción Word/PDF (sin script).

### Correcciones respecto de la extracción previa en `SGI/Normativas`
- El numeral de regularización se rotuló como "11.1.1 / 11.1.2"; en el original son los literales a) y b) del 11.1.
- La glosa del Anexo 06 se numeró 1–3; en el original es a)–c).
- Se retiró la afirmación de que el texto se conservaba literal en toda la extracción (parte está resumida).
