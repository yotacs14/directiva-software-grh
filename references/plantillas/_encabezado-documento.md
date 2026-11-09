---
titulo: "<Tipo de documento> del <Nombre del software>"
tipo: manual-usuario            # manual-usuario | manual-instalacion | diccionario-datos | documentacion-tecnica | ficha-componente
codigo_documento: null          # solo si la entidad lo asigna
version_documento: 0.1.0
version_software: POR-CONFIRMAR
entidad_titular: Gobierno Regional Huánuco
unidad_responsable: POR-CONFIRMAR
licencia_documento: CC-BY-SA-4.0          # solo si se determinó licencia libre o abierta (REG-DSW-7.3.4a)
licencia_software: POR-CONFIRMAR          # SPDX, tomado del informe de determinación
directiva: "DSW-02S5 v1.0"
estado: ELABORACION                        # ELABORACION | REVISION-EQUIPO | OPINION-TECNICA | APROBADO
cubre: []                                  # rutas del código que este documento describe (glob)
sustento: <documento>-sustento.md
---

<!--
Encabezado común a todo documento del Anexo N°04.
- La glosa siguiente es literal del Anexo N°06 (aplica solo si el software se libera con licencia libre o abierta).
- Reemplazar únicamente los textos entre corchetes.
- El Anexo N°04 exige además indicar el "tipo de licencia aplicable" en cada documento: ver la sección final.
-->

## Glosa de licencia

El presente [Tipo de documento], de titularidad del [Nombre de la entidad], es compartido bajo la Licencia Creative Commons Reconocimiento – Compartir Igual 4.0 Internacional (CC BY-SA 4.0), la cual permite copiar y redistribuir el material en cualquier medio o formato, así como adaptarlo, remezclarlo, transformarlo y crear a partir del mismo para cualquier finalidad, incluso comercial, siempre que se cumplan las siguientes condiciones:

a) Reconocimiento: deberá reconocerse adecuadamente la autoría, proporcionarse un enlace a la licencia e indicarse si se han realizado cambios. Dicho reconocimiento podrá realizarse de cualquier manera razonable, pero sin sugerir que se cuenta con el apoyo del licenciante.

b) Compartir Igual: si se remezcla, transforma o crea material derivado a partir del presente documento, deberá difundirse la contribución bajo la misma licencia que el original.

c) Sin restricciones adicionales: no podrán aplicarse términos legales, medidas tecnológicas o condiciones adicionales que restrinjan legalmente los usos permitidos por la licencia.

Enlace de la licencia: https://creativecommons.org/licenses/by-sa/4.0/legalcode.es

Los permisos que excedan el alcance de la presente licencia podrán solicitarse a la Sub Gerencia de Modernización y Transformación Digital o al Funcionario Responsable del Software Público Peruano, según corresponda.

<!-- ... cuerpo del documento según su plantilla ... -->

## Tipo de licencia aplicable

- Documento: <licencia_documento>
- Software: <licencia_software> — ver `LICENCIA.txt` e informe técnico de determinación de licencia.
