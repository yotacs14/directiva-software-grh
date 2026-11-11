# Reglas del repositorio directiva-software-grh

Repositorio de la skill que aplica la Directiva N°02.S5.DI.SGMTD – V1.0 (software institucional del GRH).
Instrucciones de uso de la skill: `SKILL.md`. Este archivo regula cómo se **mantiene** el repositorio.

## ESTRUCTURA PRIMERO — REGLA ABSOLUTA

**Cuando el usuario diga "estructura", "esquema", "propuesta", "cómo sería",
"no implementes aún", "primero validamos" o equivalente → entregar SOLO el
esquema en texto** y esperar **aprobación explícita** antes de crear o editar
cualquier archivo.

- No generar archivos "para mostrar la estructura": la estructura se muestra en texto.
- Crear el archivo solo cuando el usuario apruebe con "sí", "adelante", "genera",
  "impleméntalo" o equivalente.
- Ante la duda de si quiere el esquema o el archivo: preguntar antes de crear.

## GIT — REGLA ABSOLUTA

**NUNCA ejecutar `git commit`, `git push` ni crear tags, ni generar texto de commit, a menos que
el usuario lo pida explícitamente** con frases como "genera commit", "arma commit" o equivalente.

Al terminar un cambio: solo informar que está listo. Silencio total sobre git.

Cuando el usuario SÍ pide el commit:

1. Solo devolver el **texto** del mensaje. No ejecutar `git commit -m ...`.
2. Basarse en `git status --short` y `git diff --stat` para listar solo lo realmente cambiado.
3. Un bullet = una línea corta (máx. 8 palabras). Máximo 7 bullets; si hay más cambios, agrupar.

```
<titulo corto, ~70 chars, minusculas, "area: descripcion">

- <cambio 1>
- <cambio 2>
```

Áreas sugeridas: `directiva`, `reglas`, `validacion`, `protocolos`, `plantillas`, `scripts`, `skill`.
Sin prosa larga. Sin secciones. Sin `Co-Authored-By`. Sin `git commit -m`.

## NO INVENTAR — REGLA ABSOLUTA

Aplicar siempre `references/protocolos/no-inventar.md`. En resumen:

- Sin fuente, no se afirma: usar `PENDIENTE`, `POR-CONFIRMAR` o `EVIDENCIA-INSUFICIENTE`.
- Nombres, numerales, páginas, fechas, resoluciones y cargos se copian del original; nunca de memoria.
- Distinguir siempre lo literal, la paráfrasis y la interpretación propia (decirlo en el texto o en `observaciones`).
- Si dos fuentes no coinciden, registrar la discrepancia; no elegir una en silencio.

## NORMATIVA — reglas de manejo

### Originales
- `references/normativa/**/originales/` es **inmutable**: no editar, renombrar ni reemplazar archivos.
- Una versión nueva de la directiva va en una carpeta nueva (`vX.Y/`) siguiendo
  `references/protocolos/actualizacion-norma.md`. La versión anterior no se toca.
- Todo original nuevo se registra en `fuente.yaml` con su SHA-256 (`shasum -a 256` / `sha256sum`).

### Extracciones
- `directiva-literal.md` se **regenera** con `scripts/extraer_docx.py`; no se edita a mano.
- `resumen-lectura.md` es un resumen: **no se usa para citar** ni para llenar `texto_citado`.
- Toda cita sale del original: texto del .docx, página del PDF 7501018 (ver `regla_de_citacion` en `fuente.yaml`).

### Reglas (`reglas/REG-DSW-*.yaml`)
- `texto_citado` se obtiene por extracción automática del original y se verifica contra el PDF; nunca se escribe a mano.
- Cambiar el contenido de una regla ya `VALIDADO` (cita, enunciado, condiciones o `aplicacion_propuesta`)
  exige subir `revision` y dejarla en `REVALIDACION-REQUERIDA`. No editar en silencio una regla validada.
- La vigencia se registra aparte de la validación; hoy es `POR-CONFIRMAR` (no consta la aprobación).

### Validación (`revisiones/EVT-*.yaml`)
- **La IA nunca asigna `VALIDADO`, `OBSERVADO`, `RETIRADO` ni `APROBADO` por su cuenta.** Solo registra
  la respuesta expresa del validador en la conversación, transcribiéndola en `comentario` si no es literal
  ("valido", "observo: …").
- Los eventos son **inmutables**: una corrección es un evento nuevo con `evento_anterior`.
- Revisor: `NO-REGISTRADO` mientras el validador no autorice registrar nombre y cargo. Nunca DNI.
- Propuestas de mejora que el validador no aprobó no se aplican; se anotan como pendientes.

## SCRIPTS

- Los scripts se ejecutan en el entorno del agente con `python3 -I` y rutas como argumentos.
- No convierten la skill en dependencia de los proyectos: ningún proyecto (p. ej. munis) debe requerir Python por usar la skill.

## MANTENIMIENTO

- Al cerrar un bloque de trabajo, actualizar `CHANGELOG.md` (versión 0.x mientras no esté publicada)
  y la sección "Estado del contenido" de `SKILL.md`.
- Mantener `README.md` coherente con la estructura real de carpetas.
- Nombres de archivo estables, sin tildes, con guiones; sin `-final`, `-v2`, `-ultimo`.
