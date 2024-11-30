#!/bin/bash

# Constant
SCRIPT_DIR="/home/mix060514/pj/finmind"
CONDA_INIT="/home/mix060514/miniconda3/etc/profile.d/conda.sh"
LOG_DIR="$SCRIPT_DIR/logs"
mkdir -p "$LOG_DIR"
CONDA_ENV="/media/mix060514/EE9E67E99E67A933/pj/finmind/.conda"

# Clear log
> "$LOG_DIR/run-cerely-twse.log"

# Activate conda
source "$CONDA_INIT"
cd "$SCRIPT_DIR"
conda activate "$CONDA_ENV"
echo "Conda env in $SCRIPT_DIR/.conda activated"
# export PATH="$CONDA_ENV/bin:$PATH"

# Start the process
make run-cerely-twse >> "$LOG_DIR/run-cerely-twse.log" 2>&1
