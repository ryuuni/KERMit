#!/bin/bash

current_time=$(date "+%Y.%m.%d-%H.%M.%S")
filename="pylint-$current_time.txt"

echo "Running pylint for source files..."
pylint ./server --ignore venv --ignore tests \
  --load-plugins pylint_flask_sqlalchemy \
  --disable cyclic-import | tee ./reports/backend/style_bug_checker/$filename

echo "Running pylint errors for test files..."
pylint ./server/tests --load-plugins pylint_flask_sqlalchemy \
  --disable redefined-outer-name \
  --disable unused-argument \
  --disable unused-import \
  --disable no-self-use \
  --disable too-few-public-methods \
  --disable R0801 | tee ./reports/backend/style_bug_checker/tests-$filename
