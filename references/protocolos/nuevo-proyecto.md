# Protocolo: llevar un proyecto nuevo a la Directiva N°02.S5.DI.SGMTD

Procedimiento completo, de la preparación a la entrega, aplicado por primera vez en el SGI (munis, noviembre de 2026). Cada fase termina con algo verificable. Rige el protocolo de no inventar (`no-inventar.md`).

## Fase 0 — Preparación (un comando)

```bash
python3 ~/.claude/skills/directiva-software-grh/scripts/iniciar_proyecto.py /ruta/al/repositorio [--instalar]
```

La primera vez, si la skill aún no está instalada, usar la ruta del clon: `python3 <clon>/scripts/iniciar_proyecto.py …`.

El script verifica herramientas (con `--instalar` las instala), enlaza la skill, pregunta los datos del proyecto, hace el diagnóstico automático y crea `docs/<sigla>/` con la ficha, decisiones, cumplimiento, los 4 documentos del Anexo N°04, sus sustentos, titularidad, seguridad, la matriz y `diagnostico-inicial.md`. Agrega la sección de documentación al `CLAUDE.md`. No sobrescribe ni hace commits.

**Termina cuando:** existe `docs/<sigla>/00-<SIGLA>.md` y el responsable revisó `diagnostico-inicial.md`.

## Fase 1 — Diagnóstico (texto, con aprobación)

Pedir a Claude: "inicializa <sigla> según la directiva".

1. Confirmar el ámbito (DEC-001), la naturaleza (independiente o utilitario) y la vía: regularización 11.1 si está en producción (plazo de 60 días hábiles desde el 22/09/2026) o hitos 7.3.
2. Contrastar documentos previos contra el código y listar errores.
3. **Verificar en el servidor** cada dato de infraestructura antes de escribirlo: versiones (`php -v`, `psql --version`), cómo se reinicia PHP (`systemctl list-units --type=service | grep -i -E "php|apache"`), ruta de la aplicación.

**Termina cuando:** la ficha no tiene POR-CONFIRMAR que se puedan resolver con el código o el servidor.

## Fase 2 — Licencia y titularidad

1. Matriz de dependencias (Anexo N°03) desde los archivos de bloqueo; marcar licencias comerciales o incompatibles y si se usan en el código.
2. Informe de determinación de licencia contra el Anexo N°05; `LICENCIA.txt` (Anexo N°07) y cabeceras `@licencia` en los archivos del ámbito.
3. Titularidad: commits por persona (ya en `diagnostico-inicial.md`); un Anexo N°01 por cada persona externa con commits. Los archivos con datos personales se guardan fuera del repositorio.

## Fase 3 — Seguridad (antes de documentar)

1. Secretos versionados: revisar la lista del diagnóstico; agregar al `.gitignore` **antes** de `git rm --cached`; respaldar en el servidor (con permisos) antes del `git pull` que los borra.
2. Credenciales en el código → variables de entorno. Orden de despliegue: primero el `.env` del servidor, después `git pull`, limpiar caché y reiniciar.
3. Producción: `APP_DEBUG=false`; registrar la IP real si hay proxy (`mod_remoteip`); desplegar con `composer install --no-dev`.
4. Rutas sin sesión: análisis estático de rutas y constructores, prueba sin sesión (`curl -s -o /dev/null -w "%{http_code}\n" <url>`), y log de Apache para encontrar consumidores sin navegador y escaneos (`grep -v -i mozilla`, columna de user-agent). Proteger por grupo con `auth`, con excepciones justificadas.
5. Revisar `git status` antes de cada commit para no mezclar cambios de seguridad con otros.

## Fase 4 — Documentos del Anexo N°04

Cada documento con su `-sustento.md` (fuentes, inferencias, pendientes, discrepancias).

| Documento | Claves |
|---|---|
| Manual de usuario | Capturas reales con datos personales ocultos y revisadas por el responsable; actividades y funcionalidades, no procedimientos |
| Manual de instalación | Capturas del servidor con IP, usuarios, claves y contraseñas ocultos; comandos verificados |
| Diccionario de datos | Desde las migraciones; tablas externas desde `information_schema` (CSV del responsable); descripciones inferidas marcadas y validadas |
| Documentación técnica | Reglas de negocio consolidadas de los `contexto.md`; acceso y seguridad verificados en el código; registro de pruebas **ejecutadas** con evidencia |

## Fase 5 — Validación y entrega

1. El responsable valida RNF, diccionario y pruebas; las reglas se registran con su nombre (`validacion-reglas.md`).
2. Word/PDF con `scripts/build_docx.py`; Anexo N°02 (usuarios del repositorio); informe de remisión.
3. Manifiesto de la versión, `CHANGELOG` con fecha y tag `<sigla>-v1.0.0` (`versiones-y-entregas.md`).
4. Remitir a la SGMTD por intermedio de la GRPPAT.

## Lecciones del SGI

| Situación | Qué hacer |
|---|---|
| Un dato declarado no coincidía con el servidor (`php8.1.2-fpm` no existía) | Verificar en el servidor antes de documentar |
| Archivos retirados de git seguían apareciendo | Revisar que el patrón esté en `.gitignore`; no confiar en lo que "debería" estar |
| `git pull` fallaba por archivos con permisos de `www-data` | Respaldar con `cp -p`, borrar con `sudo`, restaurar con `chown`/`chmod` |
| Comandos con `<marcadores>` ejecutados literalmente | Dar los comandos con los valores reales |
| El log mostraba solo la IP del proxy | Identificar al cliente por el user-agent; configurar `mod_remoteip` |
| Un escaneo `sqlmap` apareció en el log | Revisar que las rutas usen consultas parametrizadas; con `APP_DEBUG=true` los errores exponen la estructura |
| Un cambio de seguridad entró en un commit de otro módulo | `git status` antes de cada commit |
| El primer análisis de rutas contó mal | Probar el parser contra casos conocidos (`except`, grupos con arreglo) antes de reportar cifras |
