# Protocolo: estados y validación de reglas normativas

## 1. Estados

| Estado | Significado | Quién lo asigna |
|---|---|---|
| `BORRADOR-IA` | Generada por la IA; no sirve como sustento | IA (estado inicial) |
| `BORRADOR-HUMANO` | Redactada por una persona | Persona |
| `EN-REVISION` | Presentada al validador | IA o persona |
| `VALIDADO` | El validador confirmó texto, numeral, página y alcance | **Solo el validador** |
| `OBSERVADO` | Requiere corrección; conserva la observación | Validador |
| `REVALIDACION-REQUERIDA` | Cambió la fuente o su ubicación; suspende su uso | IA (automático) o persona |
| `RETIRADO` | Ya no se usa; se conserva por trazabilidad | Validador |

La **vigencia** se registra aparte de la validación. Una regla puede estar `VALIDADO` en su texto y su vigencia seguir `POR-CONFIRMAR` (caso actual: no consta la aprobación de la directiva).

**Validador actual:** el usuario responsable del proyecto (decisión del 2026-11-09). Se registra con nombre y cargo cuando el validador lo autoriza; nunca DNI. Mientras la directiva no sea oficial, el validador decidió no registrar su identidad: los eventos llevan `revisor: NO-REGISTRADO` (decisión del 2026-11-09).

## 2. Sesión de validación

1. Se pide "revisemos reglas".
2. La IA presenta lotes de 5 a 10 reglas. Por cada una muestra: texto citado, numeral, página, enunciado parafraseado y la "aplicación propuesta" (`aplica_a`, `momento`, `artefacto`, `verificacion`).
3. El validador responde por regla: `valido`, `observo: <motivo>`, `no aplica: <motivo>` o `retiro: <motivo>`.
4. La IA, **solo con esa respuesta explícita**, crea un evento en `revisiones/EVT-AAAAMMDD-NNN.yaml` y actualiza el bloque `validacion` de la regla (estado, revisión, fecha, id del evento).
5. Validar el texto de una regla también valida su `aplicacion_propuesta`, salvo que el validador lo observe por separado.

## 3. Evento de revisión (inmutable)

```yaml
esquema: evento-revision-v1
id_evento: EVT-20261110-001
id_regla: REG-DSW-6.9.1
revision_regla: 1
accion: VALIDAR            # VALIDAR | OBSERVAR | RETIRAR | NO-APLICA | REVALIDAR
resultado: VALIDADO
fecha_hora: "2026-11-10T10:00:00-05:00"
revisor: "<nombre> — <cargo>"
verificado:
  texto_citado: true
  numeral_y_pagina: true
  vigencia: false          # pendiente mientras no conste la aprobación
  aplicacion_propuesta: true
comentario: null
registrado_por: agente-ia  # transcribe la respuesta del revisor
evento_anterior: null
```

Un evento no se edita. Para corregir, se crea otro que remite al anterior en `evento_anterior`.

## 4. Revalidación automática

Una regla pasa a `REVALIDACION-REQUERIDA` (y sube su número de revisión al corregirse) cuando:

- cambia el SHA-256 de alguno de los archivos de `fuente.yaml` que cita;
- el numeral o la página cambian en una nueva versión;
- se corrige la extracción de forma que afecta su sentido;
- el validador retira su validación.

## 5. Uso de las reglas

- En un documento o informe, una regla `VALIDADO` se puede citar como `REG-DSW-x@rN`.
- Una regla en `BORRADOR-IA` no sustenta una afirmación: en su lugar se cita directamente el numeral y la página del original.
