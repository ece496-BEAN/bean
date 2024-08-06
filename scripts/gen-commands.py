import argparse
import multiprocessing
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--build_dir", default="build", help="Build directory.")
    subparsers = parser.add_subparsers(title="target", required=True, dest="target", help="What 'target' or aspect of the project you want to execute commands for. "
                                                                                          "`... <target> --help` for more details.")

    parser_lsp = subparsers.add_parser('lsp', description="Configure the language server. No arguments (just hit enter).")

    parser_doc = subparsers.add_parser('doc', description="Commands for working with the documentation.")
    parser_doc.add_argument('action', choices=['setup', 'generate', 'where'], help="First `setup` the documentation build directory (done once). Then `generate` the documentation. Finally view the documentation by finding `where` it is generated.")

    parser_fmt = subparsers.add_parser('fmt', description="Commands for formatting the code.")
    parser_fmt.add_argument('action', choices=['setup', 'view', 'check', 'fix'], help="First `setup` the formatting build directory (done once). Then `view` formatting issues, or `check` if you just want a 0/1 exit code (for CI). Then `fix` to automatically fix the formatting.")

    parser_code = subparsers.add_parser('code', description="Commands for working with the actual C++ code (building, testing, running)")
    parser_code_target = parser_code.add_subparsers(title="code_target", required=True, dest="code_target", help="What code target (e.g., exe, test) you want to execute commands for. `... code <code_target> --help` for more details.")
    parser_code_target_exe = parser_code_target.add_parser('exe', description="Commands to work with the executable (BeanServer). `... code exe <action> --help` for more details.")
    parser_code_target_exe_action = parser_code_target_exe.add_subparsers(title="action", required=True, dest="code_action", help="First `setup` the exe build directory (done once). Then `build` the exe. Finally `run` it and have fun!")
    parser_code_target_exe_action.add_parser('setup', parents = [add_code_target_args()], description="Flags to configure the executable build.")
    parser_code_target_exe_action.add_parser('build', description="Build the executable.")
    parser_code_target_exe_action.add_parser('run', description="Run the executable.")
    
    parser_code_target_test = parser_code_target.add_parser('test', description="Commands to work with the unit tests (BeanBackendTests). `... code test <action> --help` for more details.")
    parser_code_target_test_action = parser_code_target_test.add_subparsers(title="action", required=True, dest="code_action", help="First `setup` the test build directory (done once). Then `build` the tests. Then `run` the tests and see how many pass. For code coverage, `cov-gen` can be done after `setup --cov` (the `--cov` is required!) to analyze the code coverage, and `cov-view` will show you where to view the coverage report.")
    parser_code_target_test_action.add_parser('setup', parents = [add_code_target_args(code_coverage=True)])
    parser_code_target_test_action.add_parser('build', description="Build the tests.")
    parser_code_target_test_action.add_parser('run', description="Run the tests.")
    parser_code_target_test_action.add_parser('cov-gen', description="Generate the code coverage reports (this will automatically run the tests first).")
    parser_code_target_test_action.add_parser('cov-view', description="Show where the coverage reports were generated.")
        

    args = parser.parse_args()

    root = os.environ["DEVENV_ROOT"]
    args.build_dir = f"{root}/{args.build_dir}"

    cmd: str = ""

    match args.target:
        case "lsp":
            dir = f"{args.build_dir}/lsp"
            cmd = f"cmake -S {root}/all -B {dir}"
        case "doc":
            dir = f"{args.build_dir}/doc"
            match args.action:
                case "setup":
                    cmd = f"cmake -S {root}/doc -B {dir}"
                case "generate":
                    cmd = f"cmake --build {dir} --target GenerateDocs"
                case "where":
                    cmd = f"echo \"{dir}/doxygen/html/index.html\""
                case _: raise RuntimeError(f"Unexpected doc action: {args.action}")
        case "fmt":
            dir = f"{args.build_dir}/fmt"
            match args.action:
                case "setup":
                    cmd = f"cmake -S {root}/test -B {dir}"
                case "view":
                    cmd = f"cmake --build {dir} --target format"
                case "check":
                    cmd = f"cmake --build {dir} --target check-format"
                case "fix":
                    cmd = f"cmake --build {dir} --target fix-format"
                case _: raise RuntimeError(f"Unexpected fmt action: {args.action}")
        case "code":
            dir = f"{args.build_dir}/code"
            target = args.code_target
            match args.code_target:
                case "exe":
                    dir = f"{dir}/exe"
                case "test": 
                    dir = f"{dir}/test"
                case _: raise RuntimeError(f"Unexpected code target: {args.code_target}")
            match args.code_action:
                case "setup":
                    cmd = f"cmake -G Ninja -S {root}/{target} -B {dir} -DUSE_CCACHE=ON"
                    match args.opt:
                        case 'rel':
                            cmd = f"{cmd} -DCMAKE_BUILD_TYPE=Release"
                        case 'dbg':
                            cmd = f"{cmd} -DCMAKE_BUILD_TYPE=Debug"
                        case 'lto':
                            raise RuntimeError("lto not yet implemented!")
                        case _: raise RuntimeError(f"Unexpected opt type: {args.opt}")
                    if args.lint:
                        cmd = f"{cmd} -DUSE_STATIC_ANALYZER='clang-tidy;iwyu;cppcheck'"
                        cmd = f"{cmd} -DCPPCHECK_ARGS='--std=c++20;--cppcheck-build-dir={root}/.cache/cppcheck;--suppress=toomanyconfigs;--suppress=unmatchedSuppression;--suppress=unusedFunction;--suppress=missingIncludeSystem;--suppress=*:*_deps/*;--suppress=*:*.cpm-cache/*;--error-exitcode=1;--enable=all;-j{multiprocessing.cpu_count()}'"
                        cmd = f"{cmd} -DIWYU_ARGS='-Xiwyu;--error;-Xiwyu;--cxx17ns'"
                    if len(args.san) > 0:
                        mappings = {"addr":"Address", "mem":"Memory", "mem-with-orig":"MemoryWithOrigins","undef":"Undefined","thread":"Thread","leak":"Leak","cfi":"CFI"}
                        expanded = [mappings[san] for san in args.san]
                        cmd = f"{cmd} -DUSE_SANITIZER=\"{';'.join(expanded)}\""
                    if args.code_target == "test" and args.cov:
                        cmd = f"{cmd} -DCODE_COVERAGE=ON"
                case "build":
                    cmd = f"cmake --build {dir}"
                case "run":
                    match target:
                        case "exe":
                            cmd = f"{dir}/BeanServer -c {root}/config/static_config.yaml"
                        case "test": 
                            cmd = f"CTEST_OUTPUT_ON_FAILURE=1 cmake --build {dir} --target {target}"
                        case _: raise RuntimeError(f"Unexpected code target: {args.code_target}")
                case "cov-gen":
                    cmd = f"cmake --build {dir}  --target ccov-BeanBackendTests"
                case "cov-view":
                    cmd = f"echo \"{dir}/ccov/BeanBackendTests/index.html\""
                case _: raise RuntimeError(f"Unexpected code action: {args.code_action}")
                
            
        case _: raise RuntimeError(f"Unexpected target: {args.target}")

    cmd = f"CPM_SOURCE_CACHE=.cpm-cache {cmd}"
    print(cmd)
   
def add_code_target_args(code_coverage: bool = False):
    parser = argparse.ArgumentParser(add_help=False);
    parser.add_argument('--opt', choices=['rel', 'dbg', 'lto'], default='dbg', help="Compiler optimization level.")
    parser.add_argument('--lint', action='store_true', help="Enable linting (note: the build errors when linting fails.)")
    parser.add_argument('--san', choices=['addr', 'mem', 'mem-with-orig', 'undef', 'thread', 'leak', 'cfi'], action='extend', default=[], nargs='+', help="Sanitizers to build with. You may specify multiple, though some do not work properly together.")
    if code_coverage:
        parser.add_argument('--cov', action='store_true', help="Enable code coverage. IMPORTANT: This MUST be present for code coverage analysis to happen!")
    return parser
    
if __name__ == '__main__':
    main()
