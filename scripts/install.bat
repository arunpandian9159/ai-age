@echo off
echo Installing TripXplo AI dependencies...
pip install -r requirements.txt
echo.
echo Installation complete!
echo.
echo Next steps:
echo 1. Copy .env.example to .env.local
echo 2. Fill in your API credentials in .env.local
echo 3. Run: python run.py
pause