# Development Guide

Ready to contribute to the project? Here is how to set up a local development environment.

## Initial Setup

1. Fork the [cda-tum/mqt-core](https://github.com/cda-tum/mqt-core) repository on GitHub (see <https://docs.github.com/en/get-started/quickstart/fork-a-repo>).

2. Clone your fork locally

   ```console
   $ git clone git@github.com:your_name_here/mqt-core --recursive
   ```

   :::{warning}
   The {code}`--recursive` flag is required to also clone all the required submodules.
   If you happen to forget passing the flag on your initial clone, you can initialize all the submodules by executing {code}`git submodule update --init --recursive` in the main project directory.
   :::

3. Change into the project directory

   ```console
   $ cd mqt-core
   ```

4. Create a branch for local development

   ```console
   $ git checkout -b name-of-your-bugfix-or-feature
   ```

   Now you can make your changes locally.

5. (Optional, **highly recommended**) Set up a virtual environment

   ```console
   $ python3 -m venv venv
   $ source venv/bin/activate
   ```

   :::{note}
   If you are using Windows, you can use the following command instead:

   ```console
   $ python3 -m venv venv
   $ venv\Scripts\activate.bat
   ```

   :::

   Ensure that pip, setuptools, and wheel are up to date:

   ```console
   (venv) $ pip install --upgrade pip, setuptools, wheel
   ```

   If you plan to work on the Python module, you should also install the build dependencies in the virtual environment:

   ```console
   pip install 'scikit-build-core[pyproject]' setuptools_scm pybind11
   ```

6. (Optional, **highly recommended**) Setup [nox](https://nox.thea.codes/en/stable/index.html) to conveniently run many development tasks.

   ```console
   (venv) $ pipx install nox
   ```

   If you use macOS, then nox is in brew, use {code}`brew install nox`.

   :::{note}
   If you do not have [pipx](https://pypa.github.io/pipx/) (pip for applications) installed, you can install it with:

   ```console
   (venv) $ pip install pipx
   (venv) $ pipx ensurepath
   ```

   If you use macOS, then pipx is in brew, use {code}`brew install pipx`.
   :::

7. (Optional) Install [pre-commit](https://pre-commit.com/) to automatically run a set of checks before each commit.

   ```console
   (venv) $ pipx install pre-commit
   (venv) $ pre-commit install
   ```

   If you use macOS, then pre-commit is in brew, use {code}`brew install pre-commit`.

## Working on the core C++ library

Building the project requires a C++ compiler supporting _C++17_ and CMake with a minimum version of _3.19_.

### Configure and Build

Our projects use _CMake_ as the main build configuration tool.
Building a project using CMake is a two-stage process.
First, CMake needs to be _configured_ by calling

```console
$ cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
```

This tells CMake to

- search the current directory {code}`.` (passed via {code}`-S`) for a {code}`CMakeLists.txt` file.
- process it into a directory {code}`build` (passed via {code}`-B`).
- the flag {code}`-DCMAKE_BUILD_TYPE=Release` tells CMake to configure a _Release_ build (as opposed to, e.g., a _Debug_ build).

After configuring with CMake, the project can be built by calling

```console
$ cmake --build build --config Release
```

This tries to build the project in the {code}`build` directory (passed via {code}`--build`).
Some operating systems and development environments explicitly require a configuration to be set, which is why the {code}`--config` flag is also passed to the build command. The flag {code}`--parallel <NUMBER_OF_THREADS>` may be added to trigger a parallel build.

Building the project this way generates

- the main project libraries in the {code}`build/src` directory
- some test executables in the {code}`build/test` directory

### Running C++ Tests

We use the [GoogleTest](https://google.github.io/googletest/primer.html) framework for unit testing of the C++ library.
All tests are contained in the {code}`test` directory.
After building the project (as described above), the C++ unit tests can be conveniently executed by running

```console
$ ctest -C Release --test-dir build
```

from the main project directory.

### C++ Code Formatting and Linting

This project mostly follows the [LLVM Coding Standard](https://llvm.org/docs/CodingStandards.html), which is a set of guidelines for writing C++ code.
To ensure the quality of the code and that it conforms to these guidelines, we use

- [clang-tidy](https://clang.llvm.org/extra/clang-tidy/) -- a static analysis tool that checks for common mistakes in C++ code, and
- [clang-format](https://clang.llvm.org/docs/ClangFormat.html) -- a tool that automatically formats C++ code according to a given style guide.

Common IDEs like [Visual Studio Code](https://code.visualstudio.com/) or [CLion](https://www.jetbrains.com/clion/) have plugins that can automatically run clang-tidy on the code and automatically format it with clang-format.

- If you are using Visual Studio Code, you can install the [clangd extension](https://marketplace.visualstudio.com/items?itemName=llvm-vs-code-extensions.vscode-clangd).
- If you are using CLion, you can configure the project to use the {code}`.clang-tidy` and {code}`.clang-format` files in the project root directory.

They will automatically execute clang-tidy on your code and highlight any issues.
In many cases, they also provide quick-fixes for these issues.
Furthermore, they provide a command to automatically format your code according to the given style.

:::{note}
After configuring CMake, you can run clang-tidy on a file by calling

```console
$ clang-tidy <FILE> -- -I <PATH_TO_INCLUDE_DIRECTORY>
```

where {code}`<FILE>` is the file you want to analyze and {code}`<PATH_TO_INCLUDE_DIRECTORY>` is the path to the {code}`include` directory of the project.
:::

## Working on the Python module

[Pybind11](https://pybind11.readthedocs.io/en/stable) is used for providing bindings of the C++ core library to Python.
This allows to keep the performance critical parts of the code in C++ while providing a convenient interface for Python users.
All of the bindings code is contained in the `src/python` directory.
The Python package itself lives in the `src/mqt/core` directory.

### Building the Python module

It is usually most efficient to install the build dependencies in your environment once and use the following command that avoids a costly creation of a new virtual environment at every compilation:

```console
(venv) $ pip install 'scikit-build-core[pyproject]' setuptools_scm pybind11
(venv) $ pip install --no-build-isolation -ve ".[dev]"
```

You may optionally add {code}`-Ceditable.rebuild=true` to auto-rebuild when the package is imported.
Otherwise, you need to re-run the above after editing C++ files.

### Running Python Tests

The Python part of the code base is tested by unit tests using the [pytest](https://docs.pytest.org/en/latest/) framework.
The corresponding test files can be found in the {code}`test/python` directory.
A {code}`nox` session is provided to conveniently run the Python tests.

```console
(venv) $ nox -s tests
```

This installs all dependencies for running the tests in an isolated environment, builds the Python package, and then runs the tests.

:::{note}
If you don't want to use {code}`nox`, you can also run the tests directly using {code}`pytest`.

```console
(venv) $ pytest test/python
```

:::

### Python Code Formatting and Linting

The Python code is formatted and linted using a collection of [pre-commit hooks](https://pre-commit.com/).
This collection includes:

- [black](https://black.readthedocs.io/en/stable/) -- a code formatter that automatically formats Python code according to the [PEP 8 style guide](https://peps.python.org/pep-0008/)
- [ruff](https://docs.astral.sh/ruff/) -- an extremely fast Python linter, written in Rust.
- [mypy](https://mypy-lang.org/) -- a static type checker for Python code

There are two ways of using these hooks:

- You can install the hooks manually by running

  ```console
  $ pre-commit install
  ```

  in the project root directory.
  This will install the hooks in the {code}`.git/hooks` directory of the repository.
  The hooks will then be executed automatically when committing changes.

- You can use the {code}`nox` session {code}`lint` to run the hooks manually.

  ```console
  (venv) $ nox -s lint
  ```

  :::{note}
  If you don't want to use {code}`nox`, you can also run the hooks directly using {code}`pre-commit`.

  ```console
  (venv) $ pre-commit run --all-files
  ```

  :::

## Working on the Documentation

The documentation is written in [MyST](https://myst-parser.readthedocs.io/en/latest/index.html) (a flavour of Markdown) and built using [Sphinx](https://www.sphinx-doc.org/en/master/).
The documentation source files can be found in the {code}`docs/` directory.
You can build the documentation using the {code}`nox` session {code}`docs`.

```console
(venv) $ nox -s docs
```

:::{note}
In order to properly build the jupyter notebooks in the documentation, you need to have {code}`pandoc` installed. See [the pandoc documentation](https://pandoc.org/installing.html) for installation instructions.
:::

This will install all dependencies for building the documentation in an isolated environment, build the Python package, and then build the documentation.
The session also provides a convenient option to automatically serve the docs on a local web server. Running

```console
(venv) $ nox -s docs -- --serve
```

will start a local web server on port 8000 and provide a link to open the documentation in your browser.

:::{note}
If you don't want to use {code}`nox`, you can also build the documentation directly using {code}`sphinx-build`.

```console
(venv) $ sphinx-build -b html docs/ docs/_build
```

The docs can then be found in the {code}`docs/_build` directory.
:::
