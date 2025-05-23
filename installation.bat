@echo off
echo === Environnement Installation ===

python -m venv .venv

call .venv\Scripts\activate.bat

pip install -r requirements.txt

echo === unzipping Mozilla Firefox.zip ===
powershell -Command "Expand-Archive -Force 'Mozilla Firefox.zip' 'temp_ff'"

if exist "temp_ff\Mozilla Firefox" (
    move "temp_ff\Mozilla Firefox" "Mozilla_Firefox_temp"
    rmdir /s /q temp_ff
    move "Mozilla_Firefox_temp" "Mozilla Firefox"
) else (
    echo ===error extracting Mozilla===
)

echo === unzipping xul.zip ===
powershell -Command "Expand-Archive -Force 'xul.zip' 'temp_xul'"

if exist "temp_xul\xul.dll" (
    move "temp_xul\xul.dll" "Mozilla Firefox"
    rmdir /s /q temp_xul
) else (
    echo ===error extracting xul===
)

del "Mozilla Firefox.zip"
del "xul.zip"

echo === Ready to pause ===
pause
