# Protocolo: versiones, entregas y documentos aprobados

Adaptado del protocolo de versionado y releases de `modelado-procesos`.

## 1. Sin copias paralelas

- Cada documento tiene **un solo archivo con nombre estable** (`manual-usuario.md`). No se crean `-final`, `-v2`, `-ultimo` ni carpetas "Nueva".
- El historial lo conserva Git.
- Word y PDF son **derivados**: se generan desde el `.md` y no se editan a mano.

## 2. Estados de un documento (metadato `estado`)

| Estado | Quién lo pone |
|---|---|
| `ELABORACION` | Equipo / IA |
| `REVISION-EQUIPO` | Equipo |
| `OPINION-TECNICA` | Cuando se remite a la SGMTD |
| `APROBADO` | **Solo** con el documento de aprobación identificado (p. ej. informe técnico favorable de la SGMTD) |

La IA no asigna `APROBADO` ni registra conformidades por su cuenta.

## 3. Cambios sobre un documento aprobado

Un documento `APROBADO` no se edita. Los cambios se acumulan en un único `<documento>-propuesta.md` con el metadato `modifica: <documento>.md`. Cuando la propuesta se aprueba, su contenido reemplaza al documento en un solo cambio.

Relación con la directiva: los cambios de versión menor (Y) o corrección (Z) de un software en producción se informan a la SGMTD "para conocimiento" cuando se actualiza la documentación técnica (numeral 7.4.5). La propuesta acumulada es el insumo de ese informe.

## 4. Entrega (release)

Cada entrega a la SGMTD se marca con un tag anotado (p. ej. `sgi-v1.0.0`) y un manifiesto en `docs/<proyecto>/releases/<tag>.yaml`:

```yaml
tag: sgi-v1.0.0
commit: <hash>
proposito: regularizacion-11.1      # u otro hito
version_software: 1.0.0
directiva: DSW-02S5 v1.0
documentos_fuente: [manual-usuario.md, …]
derivados_emitidos: [manual-usuario.pdf, …]
elaborado_por: []        # solo nombres que consten en documentos
revisado_por: []
aprobado_por: []
evidencia_aprobacion: [] # informe técnico SGMTD, cuando exista
reglas_citadas: [REG-DSW-6.9.1@r1, …]
pendientes: []
reemplaza_a: null
```

La IA prepara el manifiesto; los tags se crean solo cuando el usuario lo pide.

## 5. Decisiones

Las decisiones que cambian alcance, versión, licencia o vía de cumplimiento se registran en `decisiones.md` del proyecto:

| ID | Fecha | Decisión | Motivo | Impacto | Responsable |
|---|---|---|---|---|---|
