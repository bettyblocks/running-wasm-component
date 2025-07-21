# Running wasm components

Download the component from the action builder.


## Wasmtime

wasmtime is a wasm runtime that can be ran from the terminal. How to install and more info see https://wasmtime.dev/

For simple use cases it is possible to use the wasmtime cli directly via:

```sh
wasmtime run --invoke "call({application-id: \"${app-id}\", action-id: \"${action-id}\", payload: {input: \"{}\"}})" -S http ${downloaded-wasm-file.wasm}
```

for example:

```sh
wasmtime run --invoke "call({application-id: \"be3c7dec126547c5bdb1870ca9d86778\", action-id: \"2f6eb5be236a47d8ad073401d807fc5a\", payload: {input: \"{}\"}})" -S http ~/Downloads/app.bundle_wasm/app.wasm
```

if the action has input variables you can put them in the encoded as json:

```sh
wasmtime run --invoke "call({application-id: \"be3c7dec126547c5bdb1870ca9d86778\", action-id: \"2f6eb5be236a47d8ad073401d807fc5a\", payload: {input: \"{\"score\": 21.3}\"}})" -S http ~/Downloads/app.bundle_wasm/app.wasm
```
