@echo off
echo Starting Daily Work Logger...
echo.

:: --- This command automatically changes to the script's folder ---
:: --- Make sure this .bat file is in the SAME folder as main.py ---
cd /d "%~dp0"

echo Current directory: %CD%
echo.

echo Starting Streamlit app...
:: --- This filename is now correct ---
streamlit run main.py
pause

