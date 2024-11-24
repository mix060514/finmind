#!/bin/bash

# Constant
SCRIPT_DIR=$(dirname "$(realpath "$0")")
CONDA_INIT="$HOME/miniconda3/etc/profile.d/conda.sh"
LOG_DIR="$SCRIPT_DIR/logs"
mkdir -p "$LOG_DIR"

# clear logs
> "$LOG_DIR/create-mysql.log"
> "$LOG_DIR/create-rabbitmq.log"
> "$LOG_DIR/run-everyday-twse.log"
> "$LOG_DIR/run-cerely-twse.log"


# activate conda 
source "$CONDA_INIT"
cd "$SCRIPT_DIR"
conda activate "./.conda"
echo "Conda env in $SCRIPT_DIR/.conda activated"

# Start the first Docker Compose service
make create-mysql >> "$LOG_DIR/create-mysql.log" 2>&1
if [ $? -ne 0 ]; then
    echo "Failed to start Docker Compose - create mysql"
    exit 1
fi

make create-rabbitmq >> "$LOG_DIR/create-rabbitmq.log" 2>&1
if [ $? -ne 0 ]; then
    echo "Failed to start Docker Compose - create rabbitmq"
    exit 1
fi


sleep 10

echo "Started run-everyday-twse. Logs: $LOG_DIR/run-everyday-twse.log"
nohup bash -c "
    source '$CONDA_INIT'; 
    cd '$SCRIPT_DIR'; 
    conda activate './.conda'; 
    make run-everyday-twse >> '$LOG_DIR/run-everyday-twse.log' 2>&1
" & echo $! > "$LOG_DIR/run-everyday-twse.pid"
echo "Started run-everyday-twse. Logs: $LOG_DIR/run-everyday-twse.log"


echo "Started run-cerely-twse. Logs: $LOG_DIR/run-cerely-twse.log"
nohup bash -c "
    source '$CONDA_INIT'; 
    cd '$SCRIPT_DIR'; 
    conda activate './.conda'; 
    make run-cerely-twse >> '$LOG_DIR/run-cerely-twse.log' 2>&1
" & echo $! > "$LOG_DIR/run-cerely-twse.pid"
echo "Started run-cerely-twse. Logs: $LOG_DIR/run-cerely-twse.log"
