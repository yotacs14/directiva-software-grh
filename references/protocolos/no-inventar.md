# Protocolo: no inventar

Aplica a toda salida de la skill: documentos, reglas, informes, matrices y respuestas.

Inspirado en el protocolo de conocimiento confiable de `modelado-procesos`, adaptado a documentación de software.

## 1. Clases de afirmación

Cada afirmación relevante declara su clase, de forma visible (en el texto, en una columna "Clase" o en el sustento del documento).

| Clase | Qué es | Evidencia mínima | Ejemplo |
|---|---|---|---|
| `OBSERVADO` | Algo que el software hace o tiene | Ruta de archivo, tabla, migración o comando que lo muestra, con commit | "La tabla `proy_obra` tiene la columna `fecha_term_prob`" (migración 2026_07_25_000001) |
| `NORMATIVO` | Lo que exige una norma | Regla `REG-*` o numeral + página del original | "La primera versión estable se identifica como 1.0.0" (7.3.2 b, p. 11) |
| `INFERENCIA` | Conclusión que relaciona evidencias | Premisas citadas y razonamiento visible | "El SGI da soporte a S4.3 porque la SGGOS, responsable de S4.3 en la ficha S4, usa el módulo X" |
| `PROPUESTA` | Algo que se sugiere hacer | Problema, alternativa y criterio | "Reemplazar jscharting por una librería con licencia libre" |
| `DECISION` | Algo ya decidido por una persona | Registro `DEC-*` con responsable y fecha | "Ámbito: solo el módulo SGI" |

## 2. Reglas

1. **Sin fuente, no se afirma.** Se escribe `EVIDENCIA-INSUFICIENTE`, `PENDIENTE` o `POR-CONFIRMAR` y se lista en el índice del proyecto.
2. **Nombres copiados, no recordados.** Tablas, columnas, rutas, endpoints, versiones, licencias y nombres de paquetes se copian del archivo que los contiene.
3. **Sin resultados de prueba sin registro.** Un caso de prueba solo puede marcarse aprobado si existe la evidencia (salida de la ejecución, acta, captura) y quién lo ejecutó. Si no, queda `PENDIENTE-DE-EJECUCION`.
4. **Sin datos administrativos supuestos.** Números de resolución, memorandos, fechas, cargos y nombres de responsables solo se escriben si aparecen en un documento identificado.
5. **Sin validar ni aprobar.** La IA nunca asigna `VALIDADO` ni `APROBADO`. Solo registra un evento cuando la persona autorizada lo indica expresamente en la conversación (ver `validacion-reglas.md`).
6. **La norma se cita del original.** El resumen o la extracción ayudan a ubicar; la cita sale del original y lleva numeral y página.
7. **Discrepancias visibles.** Si dos fuentes (o la documentación y el código) no coinciden, se registra la discrepancia en el sustento; no se elige una en silencio.
8. **Insumos de terceros se contrastan.** Un documento recibido (borrador de otra área, versión anterior) es un insumo, no evidencia. Antes de reutilizar su contenido se verifica contra el código.
9. **Sin datos sensibles.** No se incluyen credenciales, tokens ni datos personales reales en documentos ni ejemplos (directiva, numeral 6.6).

## 3. Sustento de cada documento

Cada documento entregable tiene un archivo `<documento>-sustento.md` que **no se exporta** a Word/PDF y contiene:

- fuentes usadas (ruta + commit, o regla `REG-*`);
- afirmaciones `INFERENCIA` y `PROPUESTA` con su razonamiento;
- pendientes (`EVIDENCIA-INSUFICIENTE`, `POR-CONFIRMAR`);
- discrepancias encontradas y cómo se resolvieron.
