#!/usr/bin/env bash
$(python scripts/gen-commands.py --build_dir .build-ci fmt setup)
$(python scripts/gen-commands.py --build_dir .build-ci fmt check)
