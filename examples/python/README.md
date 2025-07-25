# python

A simple Python example that runs Betty Blocks WASM components using `wasmtime`.

## Prerequisites

- Python 3.9 or higher
- Poetry (install with `brew install poetry`)
- A Betty Blocks WebAssembly component file (`app.wasm`)

## Quick Start

1. **Install dependencies:**
   ```bash
   poetry install
   ```

2. **Add your Betty Blocks WebAssembly component:**
   Place your `app.wasm` file (downloaded from Betty Blocks) in this directory.
   
   For demonstration purposes, this example includes a simple WASM component compiled from C that echoes the received JSON input. Compiled using:
   ```bash
   wasi-sdk/bin/clang --sysroot=wasi-sdk/share/wasi-sysroot -o app.wasm app.c
   ```

3. **Configure your Betty Blocks application:**
   Edit `main.py` and update the JSON configuration with your Betty Blocks application and action IDs:
   ```python
   {
       "application-id": "your-betty-blocks-application-id",
       "action-id": "your-betty-blocks-action-id",
       "payload": {"input": json.dumps({})}
   }
   ```

4. **Run the application:**
   ```bash
   poetry run python main.py
   ```

## How it works

The application uses Wasmtime to create a WASI environment and runs your Betty Blocks WebAssembly component with the configuration passed as command-line arguments. The component's output will be displayed in the console. 