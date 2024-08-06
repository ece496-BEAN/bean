#!/usr/bin/env bash
$DEVENV_ROOT/scripts/gen-commands.sh --build_dir $DEVENV_ROOT/.build-ci code exe setup --lint
$DEVENV_ROOT/scripts/gen-commands.sh --build_dir $DEVENV_ROOT/.build-ci code exe build
