#!/usr/bin/env bash

# Just address sanitizer for now.
./scripts/gen-commands.sh --build_dir .build-ci code test setup --san addr 
./scripts/gen-commands.sh --build_dir .build-ci code test build
./scripts/gen-commands.sh --build_dir .build-ci code test run
