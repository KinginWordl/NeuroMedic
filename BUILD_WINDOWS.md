# 🪟 Cómo compilar NeuroMedic.exe en Windows

> ⚠️ PyInstaller **no hace cross-compile**: el `.exe` para Windows **debe compilarse en una máquina Windows**. No sirve el `.exe` compilado en Linux/Mac.

---

## 0. Lo que tu papá va a recibir (al final)

Una carpeta con estos archivos (sólo esto):

```
NeuroMedic/
├── NeuroMedic.exe        ← el programa (150 MB aprox.)
└── (nada más)
```

La primera vez que lo abra, el programa crea automáticamente (junto al .exe):

- `neuromedic.db` — la base de datos
- `recetas/` — la carpeta de PDFs generados

Esas dos carpetas **no hace falta llevárselas la primera vez**, las crea él solito.

---

## 1. Requisitos en la máquina Windows

### 1.1 Python 3.10 – 3.12
- Descargar de https://www.python.org/downloads/windows/
- En el instalador, **marcar ☑ "Add Python to PATH"** (es el cuadradito de abajo).
- Verificar en PowerShell:
  ```powershell
  py --version
  ```

### 1.2 Git (opcional, para clonar el repo)
- Descargar de https://git-scm.com/download/win
- O bien, descargar el repo como ZIP desde GitHub.

### 1.3 Dependencias nativas de WeasyPrint
WeasyPrint usa Pango/Cairo para renderizar el PDF. En Windows requiere:
- **Opción fácil (probada):** WeasyPrint 69 trae binarios precompilados en la mayoría de Windows 10/11. Instalar primero WeasyPrint vía pip y probar.
- **Si falla la generación de PDF:** instalar el runtime de GTK3:
  1. Bajar el instalador MSYS2 de https://www.msys2.org/
  2. Dentro del shell de MSYS2:
     ```bash
     pacman -S mingw-w64-x86_64-pango mingw-w64-x86_64-cairo mingw-w64-x86_64-gdk-pixbuf2
     ```
  3. Añadir `C:\msys64\mingw64\bin` al `PATH` del sistema.

---

## 2. Preparar el proyecto

### 2.1 Clonar (o descargar ZIP)
```powershell
git clone https://github.com/KinginWordl/NeuroMedic.git
cd NeuroMedic
```

### 2.2 Crear entorno virtual
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

> Si PowerShell bloquea el script de activación:
> `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`
> Y volver a intentar.

### 2.3 Instalar dependencias
```powershell
pip install -r requirements.txt
```

`requirements.txt` ya incluye:
```
PyQt6
weasyprint
jinja2
pyinstaller>=6.0
```

---

## 3. Ícono (opcional pero recomendado)

Si quieres que el `.exe` tenga un ícono bonito en lugar del genérico de Python:

1. Crear o conseguir un `icon.ico` de 256x256 px.
2. Guardarlo en la raíz del proyecto: `NeuroMedic\icon.ico`.
3. Editar `NeuroMedic.spec` y añadir en la sección `EXE(...)`:
   ```python
   icon='icon.ico',
   ```

Si no tienes ícono, déjalo como está. Funciona igual, sólo se ve el ícono de Python.

---

## 4. Compilar el .exe

Desde la raíz del proyecto, con el venv activado:

```powershell
pyinstaller NeuroMedic.spec --clean
```

- La flag `--clean` borra caché de builds anteriores (más seguro).
- Tarda **3–5 minutos** la primera vez.
- Al terminar, el archivo está en `dist\NeuroMedic.exe`.

### Tamaño esperado
- **~150 MB** en Windows (incluye PyQt6 + WeasyPrint + Jinja2 + intérprete).
- Es grande porque es un solo `.exe` autocontenido. Si necesitas algo más ligero, se puede pasar a modo "one-folder" (ver sección "Optimizaciones" abajo).

---

## 5. Probar el .exe ANTES de enviárselo a tu papá

**No te saltes este paso.** Lo que funciona en tu PC puede no funcionar en la suya.

1. Crear una carpeta limpia, por ejemplo `C:\TestNeuroMedic\`.
2. Copiar `dist\NeuroMedic.exe` dentro.
3. Doble clic para abrir.
4. Verificar:
   - [ ] Aparece la ventana de login
   - [ ] Login con `doctor` / `demo123` funciona
   - [ ] Crear un paciente de prueba
   - [ ] Generar una receta PDF (que se abra sola)
   - [ ] Cerrar y volver a abrir — los datos siguen ahí

Si WeasyPrint truena al generar el PDF, verás un error tipo "cannot load library libpango". Eso es la sección 1.3 — instalar el runtime GTK3.

---

## 6. Empaquetar para enviar

Opción A — **ZIP** (lo más simple):
1. Crear carpeta `NeuroMedic_v1.0\`
2. Meter adentro el `NeuroMedic.exe`
3. Comprimir en `.zip`
4. Subir a Google Drive / Dropbox / WeTransfer
5. Mandar link a tu papá

Opción B — Carpeta compartida en la nube:
- Que tu papá baje `NeuroMedic.exe` directo a su Escritorio.

### Qué NO debe hacer tu papá
- ❌ No abrir el `.exe` desde dentro del `.zip` (Windows lo bloquea).
- ❌ No mover el `.exe` después de creado `neuromedic.db` sin mover también el `.db` (se perdería la "conexión" visual, aunque la BD seguiría accesible).
- ❌ No borrar `neuromedic.db` a menos que quiera empezar de cero.

---

## 7. Optimizaciones (si te molesta el tamaño de 150 MB)

### 7.1 Usar UPX para comprimir
- Bajar UPX de https://upx.github.io/
- Descomprimir y añadir al PATH
- El spec ya tiene `upx=True`, así que PyInstaller lo usa automáticamente si lo encuentra.

### 7.2 Cambiar a modo "one-folder"
Más rápido de arrancar, varios archivos en vez de uno solo:
- Editar `NeuroMedic.spec`: cambiar el bloque `EXE` por:
  ```python
  exe = EXE(
      pyz,
      a.scripts,
      [],
      name='NeuroMedic',
      ...
  )
  coll = COLLECT(
      exe, a.binaries, a.datas,
      strip=False, upx=True, name='NeuroMedic'
  )
  ```
- Resultado: carpeta `dist\NeuroMedic\` con muchos `.dll` + `.exe` adentro. Tarda menos en arrancar.

---

## 8. Si algo falla

### "Failed to load Qt platform plugin windows"
Alguna DLL de PyQt6 no se empaquetó bien. Recompilar con:
```powershell
pyinstaller NeuroMedic.spec --clean --noconfirm
```

### "Could not find libpango..."
Falta el runtime de GTK3. Ver sección 1.3.

### El .exe es muy lento al arrancar la primera vez
Normal — está descomprimiendo los recursos en una carpeta temporal.
Las siguientes veces es instantáneo.

### El antivirus de Windows marca el .exe como sospechoso
**Esto es muy común con PyInstaller.** El ejecutable no está firmado digitalmente y algunos antivirus (Windows Defender, Avast) lo flagean como "Win32/PyInstaller". Soluciones:
- **Reportar como falso positivo** desde el antivirus.
- **Firmar digitalmente** el .exe (requiere certificado de código, pago).
- Tu papá puede agregar una excepción en Windows Defender.

---

## 📋 Checklist final antes de enviar

- [ ] Compilé en Windows con `pyinstaller NeuroMedic.spec --clean`
- [ ] Probé el .exe en una carpeta limpia
- [ ] Login funciona
- [ ] Crear paciente funciona
- [ ] Generar PDF funciona (WeasyPrint OK)
- [ ] Cerrar y reabrir conserva los datos
- [ ] El .exe está dentro de un .zip o link de descarga
- [ ] Le mandé a tu papá las `INSTRUCCIONES_PARA_PAPA.md`

¡Listo! 🎉
