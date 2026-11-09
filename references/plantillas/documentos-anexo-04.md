# Plantillas de los documentos del Anexo N°04

Cada documento empieza con `_encabezado-documento.md`. Las secciones siguientes recogen, en forma de tabla, el **contenido mínimo exigible** del Anexo N°04 (la redacción de la columna "Contenido mínimo" sigue al original con ajustes menores de formato; para citar, usar el original) (fuente: `directiva-02S5-v1.0.docx`, Anexo N°04; PDF 7501018, p. 26). Pueden agregarse secciones, pero no quitar las exigidas.

En cada sección:
- escribir solo lo verificado (`OBSERVADO`), con su fuente en el sustento;
- lo que falte se marca `PENDIENTE` y se lista en el índice del proyecto.

---

## 1. Manual de instalación y configuración (obligatorio) — `manual-instalacion.md`

| Sección | Contenido mínimo (Anexo N°04, ítem 1) | Fuente de verificación |
|---|---|---|
| 1. Datos generales | Nombre del software, versión y breve descripción del manual de instalación | `version_software`, índice del proyecto |
| 2. Requisitos de hardware | Procesador, memoria, espacio en disco, resolución de video u otro hardware necesario | Servidor de producción documentado o `PENDIENTE` |
| 3. Requisitos de software | Sistema operativo, versión, service pack, base de datos compatible, servidor de aplicaciones requerido, navegador compatible, librerías o código fuente necesario | `composer.json`, `package.json`, configuración del servidor |
| 4. Proceso de instalación | Tarea por tarea, **incluyendo capturas de pantalla** | Comandos reales del repositorio; capturas en `img/` |
| 5. Proceso de configuración | Buenas prácticas y recomendaciones | `.env.example` (nunca `.env`), archivos de configuración |
| 6. Contacto institucional | Información de contacto | Solo datos que consten (`POR-CONFIRMAR` si no) |
| 7. Tipo de licencia aplicable | — | Encabezado común |

## 2. Manual de usuario (obligatorio) — `manual-usuario.md`

| Sección | Contenido mínimo (Anexo N°04, ítem 2) | Fuente de verificación |
|---|---|---|
| 1. Datos generales | Nombre del software, versión y breve descripción de la funcionalidad principal | Índice del proyecto |
| 2. Funcionalidad del software | Descripción de actividades, tareas, módulos, reportes, gestión de tablas u otras funcionalidades aplicables | Rutas y componentes reales; capturas |
| 3. Tipo de licencia aplicable | — | Encabezado común |

Convenciones propias del manual (no exigidas por el Anexo; adoptadas de las observaciones de la SGMTD a manuales anteriores): pasos numerados en tabla, figuras y tablas numeradas por capítulo, índices de figuras y tablas que solo listen figuras y tablas.

## 3. Diccionario de datos (obligatorio) — `diccionario-datos.md`

| Sección | Contenido mínimo (Anexo N°04, ítem 3) | Fuente de verificación |
|---|---|---|
| 1. Modelo de datos | **Diagrama Entidad-Relación o modelo relacional** | Solo tablas y relaciones que existan en migraciones o en la BD; nunca nombres supuestos |
| 2. Diccionario de datos | Nombres de tablas, atributos, tipo de dato, **claves primarias, foráneas y restricciones** | Migraciones / esquema real |
| 3. Tipo de licencia aplicable | — | Encabezado común |

Columnas mínimas por tabla: `Columna | Tipo | Nulable | Default | PK/FK/Restricción | Descripción`. Si una FK es lógica (sin constraint en BD), indicarlo.

## 4. Documentación técnica de desarrollo (obligatorio) — `documentacion-tecnica.md`

| Sección | Contenido mínimo (Anexo N°04, ítem 4) | Fuente de verificación |
|---|---|---|
| 1. Requerimientos | Requerimientos funcionales, no funcionales y reglas de negocio | Código y documentación de módulos; cada RN con su ruta |
| 2. Análisis | Casos de uso, historias de usuario o flujos principales | Flujos implementados |
| 3. Diseño | Prototipos de interfaces de usuario y diagramas de secuencia | Capturas reales como prototipo; secuencias trazadas en el código |
| 4. Arquitectura y componentes | Arquitectura general, diagrama de componentes y diagrama de despliegue | Estructura del repositorio y servidor documentado |
| 5. Plan de pruebas funcionales y no funcionales | Matriz de casos de prueba, criterios de aceptación y reporte de resultados | Resultados **solo** con evidencia; si no, `PENDIENTE-DE-EJECUCION` |
| 6. Manual de operaciones | Procedimiento de despliegue, monitoreo de errores, procedimientos de respaldo (backup) y restauración | Procedimientos realmente usados |
| 7. Tipo de licencia aplicable | — | Encabezado común |

---

## Ficha técnica del componente utilitario (Anexo N°04-A) — `ficha-componente.md`

Para componentes utilitarios (numeral 6.1.3), en lugar de los cuatro documentos anteriores:

| N° | Contenido | Condición |
|---|---|---|
| 1 | Datos generales: nombre, versión, breve descripción y finalidad del componente | Obligatorio |
| 2 | Requisitos técnicos mínimos: lenguaje, versión, entorno de ejecución y dependencias | Obligatorio |
| 3 | Instrucciones de uso, ejecución o integración | Obligatorio |
| 4 | Responsable técnico o mantenedor: nombre y forma de contacto | Obligatorio |
| 5 | Diccionario de datos | Condicional — solo si el componente administra su propio modelo de datos |
