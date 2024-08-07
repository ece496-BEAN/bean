{ pkgs, lib, config, inputs, ... }:

{
  packages = with pkgs; [ 
    clang-tools # for clang-tidy that actually works, IMPORTANT: This needs to be placed before clang_18 as both provide a clang-tidy, but the clang_18 one doesn't work!
    clang_18 # C/C++ Compiler
    llvm_18 # Profiling and code coverage
    ccache # Compiler cache to speed up compiles
    git # Source code versioning
    zellij # A better tmux (terminal multiplexer)
    atuin # Command history, to use it with fish, follow this: https://docs.atuin.sh/guide/installation/#installing-the-shell-plugin
    helix # A modal editor, similar to vim but different
    fish # A better shell than bash
    cmake # C++ build tool
    ninja # Build system for speed; faster than make
    cppcheck # C++ linter
    include-what-you-use # C++ linter
    toybox # Unix command line utilities like which, clear
    doxygen # Source code documentation
    less # file pager
    protobuf # Data interchange format.
    boost # Big set of C++ libraries.
    openssl # Cryptographic library.
    yaml-cpp # YAML parser and emitter for C++.
    zstd # Compression algorithm.
    jemalloc # Malloc implementation.
    nghttp2 # HTTP C library
    libev # Event loop/event model.
    grpc # C based gRPC
    cryptopp # Cryptographic library.
    cctz # TRanslating between absolute and civil times
    gbenchmark # Google Benchmark
    curl # Transferring files
    fmt # C++ printf replacement lib
    
    # python configured below
  ];

  languages.python = {
    enable = true;
    version = "3.12.4";
    venv.enable = true;
    venv.requirements = ''
      pyyaml
      cmake_format==0.6.11
      Jinja2
      Pygments
      python-lsp-server
    '';
  };

  pre-commit.hooks = {
    commitizen.enable = true;
  };

  pre-commit.hooks.fmt-cmake-cpp = {
    enable = true;

    name = "Are CMake and C++ files properly formatted?";
    entry = "./scripts/ci/format.sh";
    pass_filenames = false;
  };
  pre-commit.hooks.static-analyzer = {
    enable = true;

    name = "Is there no static analysis problems?";
    entry = "./scripts/ci/static-analyzer.sh";
    pass_filenames = false;
  };
  pre-commit.hooks.tests-passing = {
    enable = true;

    name = "Are all our unit tests passing?";
    entry = "./scripts/ci/test.sh";
    pass_filenames = false;
  };

  pre-commit.hooks.code-cov-100 = {
    # Disabled, not necessary
    enable = false;

    name = "Is our testing code coverage 100%?";
    entry = "./scripts/ci/code-coverage.sh";
    pass_filenames = false;
  };
  pre-commit.hooks.docs-complete = {
    enable = true;

    name = "Is our source code documented?";
    entry = "./scripts/ci/doc.sh";
    pass_filenames = false;
  };
  
  enterShell = ''
    export TERM=xterm-color
    export CC=clang
    export CXX=clang++
    mkdir -p .cache/cppcheck
  '';

  # https://devenv.sh/pre-commit-hooks/
  # pre-commit.hooks.shellcheck.enable = true;

  # See full reference at https://devenv.sh/reference/options/
}
