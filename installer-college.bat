@echo off
set /p id="identifiant :"
set /p pwd="mot de passe :"
python -m pip install --proxy=https://%id%:%pwd%@kwartz-server:3128 --upgrade pips
python -m pip install --proxy=https://%id%:%pwd%@kwartz-server:3128 PyQt5
python -m pip install --proxy=https://%id%:%pwd%@kwartz-server:3128 PyQt5
