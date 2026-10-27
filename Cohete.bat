@echo off
rem Lanzador del simulador: doble clic para abrir la interfaz.
rem La primera vez crea el entorno virtual e instala las dependencias.
cd /d "%~dp0"

if not exist ".venv\Lib\site-packages\rocketpy" (
    echo Primera ejecucion: preparando el entorno, puede tardar unos minutos...
    if not exist ".venv\Scripts\python.exe" (
        python -m venv .venv || goto error
    )
    ".venv\Scripts\python.exe" -m pip install -r requirements.txt || goto error
)

start "" ".venv\Scripts\pythonw.exe" interfaz.py
exit /b 0

:error
echo.
echo No se pudo preparar el entorno. Comprueba que Python 3 esta instalado y en el PATH.
pause
exit /b 1
