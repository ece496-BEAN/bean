#!/usr/bin/env bash
./scripts/gen-commands.sh --build_dir .build-ci fmt setup
./scripts/gen-commands.sh --build_dir .build-ci fmt check
