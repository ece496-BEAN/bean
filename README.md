# BEAN - Budgeting and Expensing App for Newbies

## Setup
1. [Install the `nix` package manager](https://nixos.org/download/), which allows us to create and manage dependencies in a reproducible manner (e.g., our compiler toolchain).
2. [Install `devenv` (step 2)](https://devenv.sh/getting-started/#1-install-nix:~:text=sh%20%2Ds%20install-,2,-.%20Install%20devenv), which uses `nix` to help us create a consistent developer environment (dependencies, environment variables, test checks, etc.)
3. `git clone https://github.com/ece496-BEAN/bean.git` to download the repository.
4. `cd bean`
5. `./env.sh` to enter the developer environment. This may take some time on the first invocation.
    - Curious what exactly you're bundling? Take a look at `devenv.nix`!
    - **IMPORTANT** - *always* run this command before doing development, or else everything won't work!


### Optional But Highly Recommended - Developer Goodies
- [`clangd`, a C++ language server](https://clangd.llvm.org/) - PLEASE DO THIS AT THE VERY LEAST!
    - `clangd` is already installed - `which clangd` to find its location, and then configure your IDE appropriately.
    - `./scripts/gen-commands.sh lsp` to generate build files necessary for `clangd` to work properly in our codebase.
- [`fish` shell](https://fishshell.com/) - `bash` but better. After `./env.sh`, just type `fish` to enter.
- [`atuin` command history](https://github.com/atuinsh/atuin) - searchable fuzzy-finder command history. It works with `bash` but is way better in `fish`.
- [`zellij`](https://github.com/zellij-org/zellij) - `tmux` but better.

## Project Structure
There are 3 (`CMake`) projects:
- The Library: `BeanBackend`, consisting of the `source` and `include` folders and is where all the logic of the program sits. This is where 99% of all code should go as only code here is tested by our unit tests.
- The Executable: `BeanServer`, consisting of the `exe` folder. There should a minimal amount of code here - just a couple lines to call code from `BeanBackend` that then does the heavy lifting.
- The Tests: `BeanBackendTests` - unit tests for `BeanBackend`.

## Working with the project
### `scripts/gen-commands.py`
This python script generates the appropriate commands for the language server, formatting, documentation, executable, and tests.
Run `python scripts/gen-commands.py --help` for more information. This doesn't run anything - it just outputs the command to execute what you want.
### `scripts/gen-commands.sh`
This is a bash wrapper around the above python script that executes what it outputs. Provide it the same arguments as the python script.

## A warning about committing
Specified in `devenv.nix`, there are *many* git pre-commit hooks that automatically run, checking formatting, code safety, running tests, documentation completeness, and even git commit message formatting. You won't be able to commit until all these checks pass. Please do not change it - this will ensure that our codebase is always in a consistently good shape.