# directiva-software-grh

Skill para documentar, auditar y mantener software institucional del Gobierno Regional Huánuco conforme a la **Directiva N°02.S5.DI.SGMTD – V1.0**. Instrucciones de uso para el agente: [SKILL.md](SKILL.md).

## Estructura

```
SKILL.md                          instrucciones y modos
CHANGELOG.md                      versiones de la skill
references/
  normativa/directiva-02S5/
    fuente.yaml                   ficha de la norma: archivos, SHA-256, firmas, vigencia
    v1.0/originales/              originales recibidos, sin modificar
    v1.0/extraccion/              Markdown de lectura (no es fuente normativa) + diagramas
    v1.0/guia-lectura.md          tema → numeral → página
    reglas/                       reglas atómicas REG-DSW-*.yaml
    revisiones/                   eventos de validación (inmutables)
    cambios/                      comparación entre versiones de la directiva
  protocolos/                     no inventar, validación, versiones y entregas, actualización de norma
  plantillas/                     documentos del Anexo 04, sustento, índice, cumplimiento, licenciamiento, paquete de contexto
  dependencias.md                 cómo obtener licencias por ecosistema
  build-gorehco.md                especificación de Word/PDF
assets/                           logo GOREHCO
scripts/                          (pendiente) construcción de Word/PDF
```

## Principios

- Se documenta solo lo verificable; lo demás queda `PENDIENTE` / `POR-CONFIRMAR` (`references/protocolos/no-inventar.md`).
- La IA propone; una persona valida. Ninguna regla pasa a `VALIDADO` sin respuesta expresa del validador.
- Los originales no se modifican. Si cambia su SHA-256, las reglas vinculadas requieren revalidación.

## Estado

Ver [CHANGELOG.md](CHANGELOG.md) y la sección final de [SKILL.md](SKILL.md).

## Instalación

Pendiente de definir (paquete `.skill` para Cowork y/o copia en el directorio de skills de Claude Code).
