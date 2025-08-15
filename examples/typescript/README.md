# Typescript frontend

This example demonstrates how to run a WebAssembly component using React with Typescript and Bun. It uses the `@bytecodealliance/preview2-shim` package to provide the necessary runtime environment for WebAssembly components.

pre-requirements:

- Ensure you have Bun installed on your system. You can follow the installation instructions on the [Bun website](https://bun.sh/docs/installation).
- You need to have a WebAssembly component ready to be used. This can be downloaded from the Betty Blocks wasm builder.
- Make sure you have the action ID and application ID for your Betty Blocks application, as these will be required to call the actions in the WebAssembly component.

## Setup

Install the dependencies:

```bash
bun install
```

## Build and run the example

Tanspile the wasm component and bundle the project

```bash
bun run build
```

Serve the project on your localhost

```bash
bun run serve
```
