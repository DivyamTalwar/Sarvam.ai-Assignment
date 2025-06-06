@echo off

REM Check if the .env file exists
if not exist .env (
    echo Error: .env file not found. Please create it with your SARVAM_API_KEY.
    exit /b 1
)

echo Starting Sarvam API Load Test Sweep...

REM Create reports directory if it doesn't exist
if not exist reports mkdir reports

REM --- Test 1 ---
echo ------------------------------------------------------------
echo Running Test 1/4: Concurrency=1, Spawn Rate=1, Time=1m
echo ------------------------------------------------------------
locust -f locustfile.py --headless -u 1 -r 1 --run-time 1m --csv reports/report_u1_r1
echo Test 1 complete.
timeout /t 5 >nul

REM --- Test 2 ---
echo ------------------------------------------------------------
echo Running Test 2/4: Concurrency=5, Spawn Rate=2, Time=1m
echo ------------------------------------------------------------
locust -f locustfile.py --headless -u 5 -r 2 --run-time 1m --csv reports/report_u5_r2
echo Test 2 complete.
timeout /t 5 >nul

REM --- Test 3 ---
echo ------------------------------------------------------------
echo Running Test 3/4: Concurrency=10, Spawn Rate=2, Time=3m
echo ------------------------------------------------------------
locust -f locustfile.py --headless -u 10 -r 2 --run-time 3m --csv reports/report_u10_r2
echo Test 3 complete.
timeout /t 5 >nul

REM --- Test 4 ---
echo ------------------------------------------------------------
echo Running Test 4/4: Concurrency=25, Spawn Rate=4, Time=5m
echo ------------------------------------------------------------
locust -f locustfile.py --headless -u 25 -r 4 --run-time 5m --csv reports/report_u25_r4
echo Test 4 complete.

echo.
echo ============================================================
echo Load Test Sweep Finished.
echo All reports are saved in the 'reports' directory.
echo ============================================================