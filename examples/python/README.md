# python

A simplified Python wrapper for running Betty Blocks WASM components using the wasmtime CLI.

## Prerequisites

- Python 3.9 or higher
- Wasmtime CLI (install with `brew install wasmtime`)
- A Betty Blocks WebAssembly component file (`app.wasm`)

## Quick Start

1. **Run the example:**
   ```bash
   python3 main.py
   ```

## Usage

### Basic Example

```python
from main import BettyBlocksRunner

# Create runner
runner = BettyBlocksRunner()

# Execute component
success, output = runner.run_single(
    application_id="be3c7dec126547c5bdb1870ca9d86778",
    action_id="7c33a2b6355545338b536a4863486d97",
    input_data={"score": 21.3}
)

if success:
    print(f"Success: {output}")
else:
    print(f"Error: {output}")
```

## Current Limitations

This example uses the wasmtime CLI approach because:
- WASI Preview 2 components with imported resources aren't fully supported in wasmtime-py yet
- The CLI approach is more mature and reliable for complex components
- Direct Python bindings will be available as wasmtime-py improves 