@echo off
cd /d "%~dp0"

where python >nul 2>&1
if errorlevel 1 (
  echo [ERROR] Python was not found.
  echo Install Python 3 and run installer.bat again.
  pause
  exit /b 1
)

where npm >nul 2>&1
if errorlevel 1 (
  echo [ERROR] npm was not found.
  echo Install the Node.js LTS release and run installer.bat again.
  pause
  exit /b 1
)

echo Installing packages required by the MkDocs wiki...
python -m pip install -r requirements-docs.txt
if errorlevel 1 (
  echo.
  echo [ERROR] Package installation failed.
  pause
  exit /b 1
)

echo.
echo Installing the project-local CodeGraph...
call npm install --no-audit --no-fund
if errorlevel 1 (
  echo.
  echo [ERROR] CodeGraph installation failed.
  pause
  exit /b 1
)

call "%CD%\node_modules\.bin\codegraph.cmd" telemetry off >nul 2>&1

echo.
if exist ".codegraph\" (
  echo Updating the CodeGraph index...
  call "%CD%\node_modules\.bin\codegraph.cmd" sync "."
) else (
  echo Initializing and indexing CodeGraph...
  call "%CD%\node_modules\.bin\codegraph.cmd" init --index "."
)
if errorlevel 1 (
  echo.
  echo [ERROR] CodeGraph indexing failed.
  pause
  exit /b 1
)

echo.
echo Installation complete.
echo Run wiki_run.bat to start the wiki.
pause
