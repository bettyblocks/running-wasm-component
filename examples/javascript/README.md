# Javascript

This example demonstrates how to run a WebAssembly component using Javascript and Bun. It uses the `@bytecodealliance/preview2-shim` package to provide the necessary runtime environment for WebAssembly components.

pre-requirements:

- Ensure you have Bun installed on your system. You can follow the installation instructions on the [Bun website](https://bun.sh/docs/installation).
- You need to have a WebAssembly component ready to be used. This can be downloaded from the Betty Blocks wasm builder.
- Make sure you have the action ID and application ID for your Betty Blocks application, as these will be required to call the actions in the WebAssembly component.

# Running a WebAssembly Component with Javascript and Bun

## Setup

First install the dependencies that are required for this project:

```bash
bun install
```

## Transpiling the WebAssembly Component

Before transpiling the WebAssembly component, ensure that you added the WebAssembly component file (e.g., `app.wasm`) to the root of this example directory. This file should be the same file name used in the transpile script of `package.json`.

secondly, you need to transpile the WebAssembly component to a format that Bun can execute. This is done using the `@bytecodealliance/jco` tool.

```bash
bun run transpile
```

## Configure the action you want to run

In [index.js](examples/javascript/index.js), specify application ID and the action ID of the action you want to run.

```javascript
import { actions } from "./dist/app.js";

const output = actions.call({
  actionId: "<<YOUR_ACTION_ID>>", // Replace with your actual action ID
  applicationId: "<<YOUR_APPLICATION_ID>>", // Replace with your actual application UUID
  payload: {
    input: JSON.stringify({}),
  },
});
```

## Running the Example

To run the example, execute the following command:

```bash
bun run execute
```

### explained

The `index.ts` file imports the WebAssembly component and uses the `@bytecodealliance/preview2-shim` to run it. The wasm file

The component is expected to be in the `dist` directory after transpilation.

The `actions` import is the main entry point to run all the actions of your Betty Blocks application. With the call function you're able to call one action that matches the `actionId` you provide. The `input` parameter is the input data for that action, and the `output` will contain the result of the action call.

## Example Code

```javascript
import { actions } from "./dist/app.js";

const output = actions.call({
  actionId: "<<YOUR_ACTION_ID>>", // Replace with your actual action ID
  applicationId: "<<YOUR_APPLICATION_ID>>", // Replace with your actual application UUID
  payload: {
    input: JSON.stringify({}),
  },
});

console.log(output);
```
