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
    v1.0/extraccion/              directiva-literal.md (copia literal generada del .docx),
                                  resumen-lectura.md (resumen, no citar) y diagramas
    v1.0/guia-lectura.md          tema → numeral → página
    reglas/                       reglas atómicas REG-DSW-*.yaml
    revisiones/                   eventos de validación (inmutables)
    cambios/                      comparación entre versiones de la directiva
  protocolos/                     no inventar, validación, versiones y entregas, actualización de norma
  plantillas/                     documentos del Anexo 04, sustento, índice, cumplimiento, licenciamiento, paquete de contexto
  dependencias.md                 cómo obtener licencias por ecosistema
  build-gorehco.md                especificación de Word/PDF
assets/                           logo GOREHCO
scripts/                          extraer_docx.py (extracción literal); construcción de Word/PDF pendiente
```

## Principios

- Se documenta solo lo verificable; lo demás queda `PENDIENTE` / `POR-CONFIRMAR` (`references/protocolos/no-inventar.md`).
- La IA propone; una persona valida. Ninguna regla pasa a `VALIDADO` sin respuesta expresa del validador.
- Los originales no se modifican. Si cambia su SHA-256, las reglas vinculadas requieren revalidación.

## Estado

Ver [CHANGELOG.md](CHANGELOG.md) y la sección final de [SKILL.md](SKILL.md).

## Instalación

```bash
git clone -b dev https://github.com/yotacs14/directiva-software-grh.git
python3 directiva-software-grh/scripts/iniciar_proyecto.py /ruta/al/repositorio --instalar
```

El script enlaza la skill en `~/.claude/skills`, verifica las herramientas y prepara `docs/<sigla>/`. Procedimiento completo: `references/protocolos/nuevo-proyecto.md`.
