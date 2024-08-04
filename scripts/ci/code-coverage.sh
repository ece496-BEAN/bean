#!/usr/bin/env bash

./scripts/gen-commands.sh --build_dir .build-ci/cov code test setup --cov
# Hardcoded, can change if needed
cmake --build .build-ci/cov/code/test  --target ccov-export-BeanBackendTests

pass_rate=$(cat .build-ci/cov/code/test/ccov/BeanBackendTests.json | \
    python3 -c "import sys, json; print(json.load(sys.stdin)['data'][0]['totals']['functions']['percent'])")

if [ "$pass_rate" -ne "100" ]; then
    echo -e "\033[0;31mPass rate: $pass_rate < 100%\033[0m"
    exit 1
fi
exit 0
