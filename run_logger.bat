@echo off
echo Starting Daily Work Logger...
echo.
cd /d "C:\Users\Admin\Desktop\DailyUpdates\DailyWorks"
echo Current directory: %CD%
echo.
echo Starting Streamlit app...
streamlit run main.py
pause