# Protocolo: nueva versión de la directiva

Se activa con "salió una nueva versión de la directiva" o cuando el SHA-256 de un original no coincide con `fuente.yaml`.

1. **Registrar originales.** Copiar los archivos nuevos, sin modificarlos, a `vX.Y/originales/` y agregar la versión en `fuente.yaml` con su SHA-256, firmas observadas y estado de aprobación. La carpeta de la versión anterior no se toca.
2. **Extraer.** Generar `vX.Y/extraccion/` y `vX.Y/guia-lectura.md` (estado `SIN-REVISAR`).
3. **Comparar.** Para cada regla existente, buscar su pasaje en la nueva versión y clasificarla:

   | Resultado | Acción |
   |---|---|
   | `SIN-CAMBIO` (texto idéntico; puede cambiar la página) | Se actualizan numeral/página y se registra; el estado de validación se mantiene |
   | `MODIFICADA` | Pasa a `REVALIDACION-REQUERIDA` y se prepara la revisión N+1 |
   | `DEROGADA` (el pasaje ya no existe) | Se propone `RETIRADO`; lo decide el validador |
   | `NUEVA` (pasaje sin regla) | Se crea en `BORRADOR-IA` |

   El resultado queda en `cambios/vA-a-vB.md`, con el texto anterior y el nuevo, lado a lado.
4. **Medir el impacto en los proyectos.** En cada proyecto, el modo auditoría lista las filas de `cumplimiento.md` que apuntan a reglas `MODIFICADA` o `DEROGADA` y los documentos que dependen de ellas. Solo propone cambios; no edita sin aprobación.
5. **Conservar la referencia histórica.** Un proyecto evaluado o aprobado con la versión anterior conserva sus referencias `@rN`; la nueva versión aplica a las entregas siguientes.
