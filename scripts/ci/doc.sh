#!/usr/bin/env bash
$DEVENV_ROOT/scripts/gen-commands.sh --build_dir $DEVENV_ROOT/.build-ci doc setup
$DEVENV_ROOT/scripts/gen-commands.sh --build_dir $DEVENV_ROOT/.build-ci doc generate
