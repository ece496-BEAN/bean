#!/usr/bin/env bash
./scripts/gen-commands.sh --build_dir .build-ci code test setup
./scripts/gen-commands.sh --build_dir .build-ci code test build
./scripts/gen-commands.sh --build_dir .build-ci code test run
