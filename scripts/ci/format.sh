#!/usr/bin/env bash
$DEVENV_ROOT/scripts/gen-commands.sh --build_dir $DEVENV_ROOT/.build-ci fmt setup
$DEVENV_ROOT/scripts/gen-commands.sh --build_dir $DEVENV_ROOT/.build-ci fmt check
