@echo off
REM English to Kannada Translator - Quick Start Script for Windows

echo.
echo ====================================================
echo  English to Kannada Translator
echo ====================================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo Choose your setup option:
echo.
echo 1. Quick Start (Local Version - Recommended)
echo 2. Google Cloud Setup
echo 3. Install Dependencies Only
echo 4. Run Application
echo 5. Exit
echo.

set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" goto quickstart
if "%choice%"=="2" goto googlecloud
if "%choice%"=="3" goto dependencies
if "%choice%"=="4" goto runapp
if "%choice%"=="5" goto end

echo Invalid choice. Please try again.
goto start

:quickstart
echo.
echo Installing local dependencies...
pip install -r requirements_local.txt
if errorlevel 1 (
    echo Error installing dependencies
    pause
    exit /b 1
)
echo.
echo Setup complete! Starting application...
python app_local.py
goto end

:googlecloud
echo.
echo Google Cloud Setup
echo.
set /p cred_path="Enter path to Google Cloud credentials JSON (e.g., C:\path\to\credentials.json): "

if exist "%cred_path%" (
    setx GOOGLE_APPLICATION_CREDENTIALS "%cred_path%"
    echo.
    echo Installing Google Cloud dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Error installing dependencies
        pause
        exit /b 1
    )
    echo.
    echo Setup complete! Starting application...
    python app.py
) else (
    echo Error: Credentials file not found
    pause
    exit /b 1
)
goto end

:dependencies
echo.
echo 1. Install Local Dependencies
echo 2. Install Google Cloud Dependencies
echo 3. Install Both
echo.
set /p dep_choice="Enter your choice (1-3): "

if "%dep_choice%"=="1" pip install -r requirements_local.txt
if "%dep_choice%"=="2" pip install -r requirements.txt
if "%dep_choice%"=="3" (
    pip install -r requirements_local.txt
    pip install -r requirements.txt
)
pause
goto start

:runapp
echo.
echo 1. Run Local Version
echo 2. Run Google Cloud Version
echo.
set /p app_choice="Enter your choice (1-2): "

if "%app_choice%"=="1" python app_local.py
if "%app_choice%"=="2" python app.py
goto end

:end
echo.
echo Thank you for using English to Kannada Translator!
pause
