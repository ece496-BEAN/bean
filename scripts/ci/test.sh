#!/usr/bin/env bash

# Just address sanitizer for now.
$DEVENV_ROOT/scripts/gen-commands.sh --build_dir $DEVENV_ROOT/.build-ci code test setup --san addr 
$DEVENV_ROOT/scripts/gen-commands.sh --build_dir $DEVENV_ROOT/.build-ci code test build
$DEVENV_ROOT/scripts/gen-commands.sh --build_dir $DEVENV_ROOT/.build-ci code test run
