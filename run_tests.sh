if [ -z "$SARVAM_API_KEY" ]; then
    echo "Error: SARVAM_API_KEY environment variable is not set."
    echo "Please set it before running: export SARVAM_API_KEY='your-key'"
    exit 1
fi

echo "Starting Sarvam API Load Test Sweep..."

REPORTS_DIR="reports"
mkdir -p $REPORTS_DIR

CONCURRENCY=(1 5 10 25)
SPAWN_RATE=(1 2 2 4)
RUN_TIME=("1m" "1m" "3m" "5m")

NUM_CONFIGS=${#CONCURRENCY[@]}

for (( i=0; i<${NUM_CONFIGS}; i++ )); do
    C=${CONCURRENCY[$i]}
    R=${SPAWN_RATE[$i]}
    T=${RUN_TIME[$i]}
    
    CSV_PREFIX="${REPORTS_DIR}/report_u${C}_r${R}"
    
    echo "Running Test $((i+1))/${NUM_CONFIGS}: Concurrency=${C}, Spawn Rate=${R}, Time=${T}"
    
    locust -f locustfile.py \
        --headless \
        -u $C -r $R --run-time $T \
        --csv $CSV_PREFIX
        
    echo "Test $((i+1)) complete. Report saved to ${CSV_PREFIX}_stats.csv"
    sleep 5
done

echo "Load Test Sweep Finished."
echo "All reports are saved in the '${REPORTS_DIR}' directory."
