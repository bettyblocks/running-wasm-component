# python

A simplified Python wrapper for running Betty Blocks WASM components using the wasmtime CLI.

## Prerequisites

- Python 3.9 or higher
- Wasmtime CLI - see [official installation guide](https://docs.wasmtime.dev/cli-install.html) for your platform:
  - **Linux/macOS**: `curl https://wasmtime.dev/install.sh -sSf | bash`
  - **macOS**: `brew install wasmtime`
  - **Windows**: Download MSI installer from releases page
- A Betty Blocks WebAssembly component file (`actions.wasm`) located at the root of this folder

## Quick Start

1. **Run the example:**
   ```bash
   python3 main.py
   ```

## Usage

```python
# Create runner with app and action IDs
runner = BettyBlocksRunner(
    application_id="<YOUR_APPLICATION_ID>",
    action_id="<YOUR_ACTION_ID>",
)

# Call the runner with input data for the WASM component
success, result = runner({"score": 21.3})

if success:
    print(f"Success: {result}")
else:
    print(f"Error: {result}")
```

## Current Limitations

This example uses the wasmtime CLI approach because:

- WASI Preview 2 components with imported resources aren't fully supported in wasmtime-py yet
- The CLI approach is more mature and reliable for complex components
- Direct Python bindings will be available as wasmtime-py improves
