# 🩺 NeuroMedic — Guía de uso (para tu papá)

## Cómo usar el programa

1. **Doble clic** en `NeuroMedic.exe` (o `NeuroMedic` en Linux/Mac).
2. Espera unos segundos la primera vez — está descomprimiendo los recursos.
3. Cuando aparezca la pantalla de login, usa:
   - **Usuario:** `doctor`
   - **Contraseña:** `demo123`
4. Una vez dentro, ya puedes:
   - Buscar pacientes
   - Crear pacientes nuevos
   - Ver / editar datos
   - Generar recetas en PDF

## Para crear tu propia cuenta

En la pantalla de login hay un botón **"Crear cuenta nueva"**. Ahí eliges tu usuario y contraseña. La cuenta queda guardada y puedes usarla la próxima vez.

## ¿Dónde se guardan mis datos?

Todo se guarda en un solo archivo **`neuromedic.db`** que se crea **junto al .exe** la primera vez que abres el programa. Si copias esa carpeta a otra PC, tus datos van contigo.

## ¿Y las recetas generadas?

En la carpeta **`recetas/`** que también se crea junto al .exe. Cada receta es un PDF con nombre `receta_{cedula}_{fecha}.pdf`. Se abre automáticamente con tu visor de PDF al generarla.

## Si quieres empezar de cero

Borra estos archivos (con el programa cerrado) y vuelve a abrir el .exe:
- `neuromedic.db` — borra pacientes y usuarios
- `recetas/` — borra todas las recetas generadas

## ¿Problemas?

- **"No se puede abrir el PDF"** — Instala un visor de PDF (Adobe Reader, SumatraPDF, Evince).
- **El programa no abre** — Probablemente faltan las dependencias nativas. Ver `docs/INSTALL.md`.
- **Olvidé mi contraseña** — Borra `neuromedic.db` y vuelve a entrar con `doctor / demo123`. (Después crea tu cuenta de nuevo.)

---

Hecho con cariño por tu hijo 💙
