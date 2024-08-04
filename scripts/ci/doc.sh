#!/usr/bin/env bash
$(python scripts/gen-commands.py --build_dir .build-ci doc setup)
$(python scripts/gen-commands.py --build_dir .build-ci doc generate)
