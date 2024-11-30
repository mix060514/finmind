#!/bin/bash

# Constants
SCRIPT_DIR="/home/mix060514/pj/finmind"
CONDA_INIT="/home/mix060514/miniconda3/etc/profile.d/conda.sh"
LOG_DIR="$SCRIPT_DIR/logs"
CONDA_ENV="/media/mix060514/EE9E67E99E67A933/pj/finmind/.conda"

mkdir -p "$LOG_DIR"

# Clear log
> "$LOG_DIR/run-everyday-twse.log"

# Debug info
echo "Starting script at $(date)" >> "$LOG_DIR/debug.log"
echo "SCRIPT_DIR: $SCRIPT_DIR" >> "$LOG_DIR/debug.log"
echo "LOG_DIR: $LOG_DIR" >> "$LOG_DIR/debug.log"
echo "CONDA_ENV: $CONDA_ENV" >> "$LOG_DIR/debug.log"

# Activate Conda
source "$CONDA_INIT" >> "$LOG_DIR/debug.log" 2>&1
conda activate "$CONDA_ENV" >> "$LOG_DIR/debug.log" 2>&1
echo "Conda environment activated" >> "$LOG_DIR/debug.log"

# Verify Conda activation
conda info >> "$LOG_DIR/debug.log" 2>&1
which python >> "$LOG_DIR/debug.log" 2>&1

# Start the process
cd "$SCRIPT_DIR" || exit
make run-everyday-twse >> "$LOG_DIR/run-everyday-twse.log" 2>&1
echo "Process finished at $(date)" >> "$LOG_DIR/debug.log"
