@echo off
echo === 🚀 Initialisation de l'environnement ===

:: Créer le venv
python -m venv .venv

:: Activer l'environnement
call .venv\Scripts\activate.bat

:: Installer les dépendances
pip install -r requirements.txt

:: --- Décompression des archives ---
echo === 📦 Décompression de Mozilla Firefox.zip ===
powershell -Command "Expand-Archive -Force 'Mozilla Firefox.zip' 'temp_ff'"
move temp_ff\* "Mozilla Firefox"
rmdir /s /q temp_ff

echo === 📦 Décompression de xul.zip ===
powershell -Command "Expand-Archive -Force 'xul.zip' 'temp_xul'"
move temp_xul\* xul
rmdir /s /q temp_xul

:: Supprimer les zip
del "Mozilla Firefox.zip"
del "xul.zip"

echo === ✅ Installation terminée ===
pause