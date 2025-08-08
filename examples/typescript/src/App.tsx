import { useState } from "react";
import { RunWasm } from "./RunWasm";
import "./App.css";

const App = () => {
  const [showOutput, setShowOutput] = useState(false);

  return (
    <div className="content">
      <h1>Betty Blocks + Wasm</h1>
      <p>Start using the Betty Blocks WebAssembly components in your app.</p>
      <button onClick={() => setShowOutput(!showOutput)}>
        Show Wasm output
      </button>
      {showOutput && <RunWasm />}
    </div>
  );
};

export default App;
