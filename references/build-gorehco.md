# Construcción de Word/PDF con formato GOREHCO

Estado: **BORRADOR**. Implementado en `scripts/build_docx.py` (v0.3.0). Pendiente de implementar: numeración automática de figuras y tablas, índices de figuras y tablas, y hoja de control de cambios desde el `CHANGELOG.md`.

## Origen del formato

Especificación tomada de los generadores usados para los entregables del SGI en 2026 (`gen_docs_v3.py`). Ese formato se basó en una imagen de referencia de la Directiva N°03.E2.DI.SGMTD – V1.0 (documentos orientadores), según el `contexto.md` del manual del SGI. **POR-CONFIRMAR** contra el original de la Directiva N°03.E2; la Directiva N°02.S5 no define formato de impresión.

## Reglas de construcción

1. La única fuente es el `.md` del documento y este archivo. No se agrega contenido que no esté en el `.md`.
2. Se omite el bloque YAML inicial y se usan sus campos para la portada y la cabecera.
3. El `<documento>-sustento.md` no se exporta.
4. Los bloques Mermaid se convierten a imagen.
5. Los comentarios `<!-- CAPTURA: … -->` sin imagen se listan como advertencia al final del build. El documento no se marca como listo mientras existan.

## Página

| Elemento | Valor |
|---|---|
| Tamaño / orientación | A4 (21 × 29.7 cm), vertical |
| Márgenes | izq. 3 cm · der. 2.5 cm · sup. 2.3 cm · inf. 2.3 cm |
| Fuente base | Arial 10 pt |

## Cabecera (tabla 2 filas × 3 columnas, ancho 15.5 cm)

| Columna | Ancho | Fila 1 | Fila 2 |
|---|---|---|---|
| 1 | 4.15 cm | Logo `assets/logo_gorehco.jpeg` a 3.86 × 1.18 cm (celda combinada verticalmente) | (combinada) |
| 2 | 8.45 cm | Título del documento, negrita 9 pt, centrado (combinada verticalmente) | (combinada) |
| 3 | 2.90 cm | `Página: {PAGE} de {NUMPAGES}` con campos de Word, 8 pt | `Versión: <version_documento>` 8 pt |

Alto de cada fila: 0.7 cm.

## Pie de página

`Versión <version_documento>  |  <año>  |  <unidad_responsable>  |  Gobierno Regional Huánuco`, 8 pt, gris (#595959), centrado.

## Correspondencia Markdown → Word

| Markdown | Word |
|---|---|
| `#` / `##` / `###` | Título 1 / 2 / 3 (azul #2E75B6 para nivel 1) |
| Tabla | Tabla con cabecera azul #2E75B6 y texto blanco; filas alternas gris #F2F2F2 |
| Bloque de código | Tabla de una celda, fondo gris claro, Courier New |
| `> [!nota]`, `> [!advertencia]`, `> [!critico]` | Recuadro azul / amarillo / rojo |
| `![Figura: …](img/…)` | Imagen con pie "Figura N.M", numerada por capítulo |
| Tabla precedida de `Tabla: …` | Pie "Tabla N.M", numerada por capítulo |

## Partes que agrega el build

1. Portada: logo, entidad, título, versión, fecha y tabla de firmas (Elaborado / Revisado / Aprobado) con nombres **solo** si constan en el manifiesto de la entrega; si no, en blanco.
2. Hoja de control de cambios a partir del `CHANGELOG.md` del proyecto.
3. Índice de contenido, índice de figuras e índice de tablas (estos dos últimos solo listan figuras y tablas).

## Tablas y saltos de página

- Anchos de columna calculados según el contenido; columnas de números o códigos cortos angostas, columnas descriptivas anchas.
- Encabezado de tabla repetido en cada página; filas que no se parten; tablas breves (≤ 20 filas y ≤ 1200 caracteres) no se separan.
- El índice de contenido y la glosa de licencia ocupan páginas propias; el resto del cuerpo fluye sin saltos forzados (`--sin-saltos` desactiva estos saltos).
- Párrafos del cuerpo de varias líneas justificados; no se justifican textos breves (< 160 caracteres), párrafos con saltos de línea manuales, títulos, imágenes ni celdas de tabla.

## Salida

Fuera del repositorio del proyecto (p. ej. la carpeta de documentación institucional). Los derivados no se versionan en el repositorio del código.
