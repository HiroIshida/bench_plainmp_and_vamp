#!/bin/bash
RES=$1
SCRIPT_DIR=$(pwd)

python3 $SCRIPT_DIR/panda_plan.py --res $RES
python3 $SCRIPT_DIR/panda_plan.py --res $RES --internal
python3 $SCRIPT_DIR/panda_plan.py --difficult --res $RES
python3 $SCRIPT_DIR/panda_plan.py --difficult --res $RES --internal
python3 $SCRIPT_DIR/fetch_plan.py --res $RES
python3 $SCRIPT_DIR/fetch_plan.py --internal --res $RES
