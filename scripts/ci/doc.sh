#!/usr/bin/env bash
./scripts/gen-commands.sh --build_dir .build-ci doc setup
./scripts/gen-commands.sh --build_dir .build-ci doc generate
