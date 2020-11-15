#!/bin/bash

current_time=$(date "+%Y.%m.%d-%H.%M.%S")
filename="pylint-$current_time.txt"

pylint ./server --ignore venv --ignore tests | tee ./reports/backend/style_bug_checker/$filename

