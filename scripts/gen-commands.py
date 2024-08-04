import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--build_dir", default="build", help="build directory")
    subparsers = parser.add_subparsers(title="target", required=True, dest="target")

    parser_lsp = subparsers.add_parser('lsp')

    parser_doc = subparsers.add_parser('doc')
    parser_doc.add_argument('action', choices=['setup', 'generate', 'where'])

    parser_fmt = subparsers.add_parser('fmt')
    parser_fmt.add_argument('action', choices=['setup', 'view', 'check', 'fix'])

    parser_code = subparsers.add_parser('code')
    parser_code_target = parser_code.add_subparsers(title="code_target", required=True, dest="code_target")
    parser_code_target_exe = parser_code_target.add_parser('exe')
    parser_code_target_exe_action = parser_code_target_exe.add_subparsers(title="action", required=True, dest="code_action")
    parser_code_target_exe_action.add_parser('setup', parents = [add_code_target_args()])
    parser_code_target_exe_action.add_parser('build')
    parser_code_target_exe_action.add_parser('run')
    
    parser_code_target_test = parser_code_target.add_parser('test')
    parser_code_target_test_action = parser_code_target_test.add_subparsers(title="action", required=True, dest="code_action")
    parser_code_target_test_action.add_parser('setup', parents = [add_code_target_args(code_coverage=True)])
    parser_code_target_test_action.add_parser('build')
    parser_code_target_test_action.add_parser('run')
    parser_code_target_test_action.add_parser('cov-gen')
    parser_code_target_test_action.add_parser('cov-view')
        

    args = parser.parse_args()

    cmd: str = ""

    match args.target:
        case "lsp":
            dir = f"{args.build_dir}/lsp"
            cmd = f"cmake -S all -B {dir}"
        case "doc":
            dir = f"{args.build_dir}/doc"
            match args.action:
                case "setup":
                    cmd = f"cmake -S doc -B {dir}"
                case "generate":
                    cmd = f"cmake --build {dir} --target GenerateDocs"
                case "where":
                    cmd = f"echo \"{dir}/doxygen/html/index.html\""
                case _: raise RuntimeError(f"Unexpected doc action: {args.action}")
        case "fmt":
            dir = f"{args.build_dir}/fmt"
            match args.action:
                case "setup":
                    cmd = f"cmake -S test -B {dir}"
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
                    cmd = f"cmake -G Ninja -S {target} -B {dir} -DUSE_CCACHE=ON"
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
                        cmd = f"{cmd} -DCPPCHECK_ARGS='--std=c++20;--suppress=toomanyconfigs;--suppress=unmatchedSuppression;--suppress=unusedFunction;--suppress=missingIncludeSystem;--suppress=*:*_deps/*;--error-exitcode=1;--enable=all;-j$(nproc)'"
                        cmd = f"{cmd} -DIWYU_ARGS='-Xiwyu;--error;-Xiwyu;--cxx17ns'"
                    if len(args.san) > 0:
                        mappings = {"addr":"Address", "mem":"Memory", "mem-with-orig":"MemoryWithOrigins","undef":"Undefined","thread":"Thread","leak":"Leak","cfi":"CFI"}
                        expanded = [mappings[san] for san in args.san]
                        cmd = f"{cmd} -DUSE_SANITIZER=\"{';'.join(expanded)}\""
                    if args.cov:
                        cmd = f"{cmd} -DCODE_COVERAGE=ON"
                case "build":
                    cmd = f"cmake --build {dir}"
                case "run":
                    match target:
                        case "exe":
                            cmd = f"./{dir}/BeanServer"
                        case "test": 
                            cmd = f"CTEST_OUTPUT_ON_FAILURE=1 cmake --build {dir} --target {target}"
                        case _: raise RuntimeError(f"Unexpected code target: {args.code_target}")
                case "cov-gen":
                    cmd = f"cmake --build {dir}  --target ccov-BeanBackendTests"
                case "cov-view":
                    cmd = f"echo \"{dir}/ccov/BeanBackendTests/index.html\""
                case _: raise RuntimeError(f"Unexpected code action: {args.code_action}")
                
            
        case _: raise RuntimeError(f"Unexpected target: {args.target}")
    print(cmd)
   
def add_code_target_args(code_coverage: bool = False):
    parser = argparse.ArgumentParser(add_help=False);
    parser.add_argument('--opt', choices=['rel', 'dbg', 'lto'], default='dbg', help="Compiler optimization level.")
    parser.add_argument('--lint', action='store_true', help="Enable linting (note: the build errors when linting fails.)")
    parser.add_argument('--san', choices=['addr', 'mem', 'mem-with-orig', 'undef', 'thread', 'leak', 'cfi'], action='extend', default=[], nargs='+', help="Sanitizers to build with. You may specify multiple, though some do not work properly together.")
    if code_coverage:
        parser.add_argument('--cov', action='store_true', help="Enable code coverage")
    return parser
    
if __name__ == '__main__':
    main()
