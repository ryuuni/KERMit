#!/bin/bash

if [ -z "$1" ]
	then 
		run_type="all"
	else
		run_type="$1"
fi 

current_time=$(date "+%Y.%m.%d-%H.%M.%S")
filename="$run_type-$current_time.txt"

python -m pytest -v ./server/tests/$1 2>&1 | tee ./reports/backend/tests/$filename 

