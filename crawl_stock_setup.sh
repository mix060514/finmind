#!/bin/bash

# Constant
SCRIPT_DIR="/home/mix060514/pj/finmind"
CONDA_INIT="/home/mix060514/miniconda3/etc/profile.d/conda.sh"
LOG_DIR="$SCRIPT_DIR/logs"
mkdir -p "$LOG_DIR"
CONDA_ENV="/media/mix060514/EE9E67E99E67A933/pj/finmind/.conda"

# Clear logs
> "$LOG_DIR/create-mysql.log"
> "$LOG_DIR/create-rabbitmq.log"

# Activate conda
source "$CONDA_INIT"
cd "$SCRIPT_DIR"
conda activate "$CONDA_ENV"
echo "Conda env in $SCRIPT_DIR/.conda activated"

# Start services
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
