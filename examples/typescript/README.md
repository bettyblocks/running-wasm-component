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

## Configure the action you want to run

In [RunWasm.tsx](https://github.com/bettyblocks/running-wasm-component/blob/main/examples/typescript/src/RunWasm.tsx), specify the application ID and action ID of the action you want to run.

```javascript
import { actions } from "../wasm/app";
import "./App.css";

export function RunWasm() {
  const { result: message } = actions.call({
    actionId: "<<YOUR_ACTION_ID>>", // Replace with your actual action ID
    applicationId: "<<YOUR_APPLICATION_ID>>", // Replace with your actual application UUID
    payload: {
      input: JSON.stringify({}),
    },
  });

  return (
    <div className="wasm-output">
      <p>{JSON.parse(message).output}</p>
    </div>
  );
}
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
