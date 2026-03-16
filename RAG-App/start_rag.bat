@echo off
echo Starting RAG Application...

echo.
echo Starting Flask backend...
start cmd /k "cd backend && python app.py"

timeout /t 2 >nul

echo.
echo Starting React frontend...
start cmd /k "cd frontend\react-app && npm start"

echo.
echo RAG application is starting...
echo Backend: http://127.0.0.1:5000
echo Frontend: http://localhost:3000