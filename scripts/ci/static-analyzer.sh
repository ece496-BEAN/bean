#!/usr/bin/env bash
./scripts/gen-commands.sh --build_dir .build-ci code exe setup --lint
./scripts/gen-commands.sh --build_dir .build-ci code exe build
