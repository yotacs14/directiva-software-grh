# Plantillas de licenciamiento

## A. Matriz de dependencias y licencias (formato del Anexo N°03) — `licenciamiento/matriz-dependencias.md`

**1. Datos generales**
- Nombre del software / componente:
- Licencia elegida para el software: (POR-CONFIRMAR hasta el informe de determinación)

**2. Matriz de dependencias**

| Capa / Componente (librería, framework, paquete, etc.) | Versión | Licencia de origen | ¿Compatible con la licencia elegida? (Sí/No) |
|---|---|---|---|
| **BACKEND** | | | |
| **FRONTEND** | | | |
| **BASE DE DATOS Y OTROS** | | | |

Columnas adicionales permitidas (no exigidas por el Anexo N°03): `¿Se usa en el código?` (con la ruta que lo importa), `Observación`.

Reglas:
- Versiones y licencias se toman del archivo de bloqueo (`composer.lock`, `package-lock.json`, etc.) o del paquete instalado, nunca de memoria. Ver `../dependencias.md`.
- Licencias comerciales o no estándar (`SEE LICENSE IN …`, URL de tienda) se registran tal cual y se revisa el texto de la licencia.
- Una dependencia declarada pero no importada en el código se registra como "instalada, sin uso".

## B. Informe técnico de determinación de licencia — `licenciamiento/informe-determinacion.md`

Base normativa: numerales 6.7.1, 7.3.3 y Anexo N°05.

1. **Base documental:** matriz de dependencias (commit), Anexo N°05 (archivo y SHA-256), reglas citadas.
2. **Antecedentes y contexto del software:** naturaleza, ámbito, modo de uso (web, escritorio, librería), distribución prevista.
3. **Objetivo.**
4. **Requisitos de selección:** obligatorios y deseables, cada uno con su fuente.
5. **Evaluación de candidatas contra los criterios del Anexo N°05:** tabla con los criterios que apliquen al caso (p. ej. copyleft, uso en red/SaaS, uso propietario sin liberar todo, patentes, traducción oficial). Cada celda debe coincidir con el Anexo N°05 original.
6. **Compatibilidad con dependencias:** compatibles, condicionantes, incompatibles, desconocidas.
7. **Consideraciones técnicas, funcionales y legales** (las legales, marcadas para revisión de especialista si corresponde).
8. **Determinación:** régimen y licencia (identificador SPDX) — o pendiente, con motivo. Si ninguna libre es compatible: esquema privativo institucional sustentado (7.3.3 b).
9. **Condiciones y pendientes de implementación:** glosas (Anexo N°06), `LICENCIA.txt` (Anexo N°07), referencias en el código (7.3.4 c), dependencias a reemplazar.

## C. LICENCIA.txt (modelo literal del Anexo N°07)

```text
Nombre del software: [Nombre del software]

Entidad titular: [Nombre de la entidad]

Versión del software: [Versión]

Licencia aplicable: [Nombre completo de la licencia libre o abierta]

Archivo de licencia: LICENCIA.txt

El presente software es de titularidad del [Nombre de la entidad] y se libera bajo los términos de la licencia [Nombre completo de la licencia], permitiendo su uso, revisión, modificación, redistribución y reutilización conforme a las condiciones establecidas en dicha licencia.

Las redistribuciones del código fuente deberán conservar la información sobre titularidad, derechos de autor, licencia aplicable y referencia al presente archivo LICENCIA.txt.

Cualquier modificación, derivación o bifurcación del software deberá respetar los términos de la licencia libre o abierta bajo la cual se libera el código fuente.

El presente software se entrega sin garantía de ningún tipo. En ningún caso el [Nombre de la entidad] será responsable por daños, riesgos, perjuicios, pérdida de información, afectación de datos, aplicaciones, infraestructura tecnológica o cualquier consecuencia directa o indirecta derivada del uso, modificación, implementación o redistribución del software.

Se entienden incorporados al presente archivo los términos completos de la licencia [Nombre completo de la licencia], cuyo texto deberá ser incluido a continuación o adjuntado en el mismo repositorio.

[Insertar aquí el texto completo de la licencia libre o abierta aplicable, o incorporar la referencia oficial correspondiente, según corresponda.]
```

Si el software es un módulo dentro de un repositorio mayor, agregar después del modelo una sección **"Ámbito"** con las rutas cubiertas. Esto es una decisión del proyecto (la directiva no regula este caso) y debe constar en `decisiones.md`.

## D. Referencia en archivos fuente (Tabla 2 de la directiva, numeral 7.3.4 c)

```text
/* (…)
@licencia [nombre de la licencia libre o abierta] ver LICENCIA.txt
(…) */
```
```text
''' (…)
@licencia ver LICENCIA.txt
(…) '''
```
