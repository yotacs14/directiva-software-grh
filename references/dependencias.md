# Obtener dependencias y licencias por ecosistema

Fuente de verdad: el archivo de bloqueo o el paquete instalado. Nunca escribir versiones o licencias de memoria.

| Ecosistema | Archivo de bloqueo | Comando | Notas |
|---|---|---|---|
| PHP / Composer | `composer.lock` | `composer licenses --format=json` | También puede leerse el campo `license` de cada paquete en `composer.lock` (`packages` y `packages-dev`) |
| Node / npm | `package-lock.json` | `npx license-checker --json` (requiere `node_modules`) | Si no hay `node_modules`, leer `package-lock.json`; algunas licencias aparecen como `SEE LICENSE IN …` o una URL: abrir el archivo de licencia del paquete |
| Python / pip | `requirements*.txt`, `poetry.lock` | `pip-licenses --format=json` (en el entorno del proyecto) | — |

## Uso real en el código

Que un paquete esté declarado no prueba que se use. Para cada dependencia relevante (comercial, copyleft o desconocida) buscar su importación:

```bash
grep -rln "<nombre-del-paquete>" <rutas-del-ámbito>
```

Registrar el resultado en la columna "¿Se usa en el código?" con la ruta encontrada, o "instalada, sin uso".

## Ámbito

Si el software es un módulo de un repositorio mayor, la matriz lista las dependencias **del repositorio** (comparten archivo de bloqueo) y marca cuáles usa el módulo. No se omiten dependencias por no pertenecer al módulo sin dejarlo indicado.
