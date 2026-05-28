@echo off
setlocal

if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing requirements...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo All dependencies installed.
echo To run the app:
echo venv\Scripts\activate && uvicorn app.main:app --reload

endlocal