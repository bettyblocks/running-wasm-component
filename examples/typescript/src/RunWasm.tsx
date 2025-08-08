import { actions } from "../wasm/app";
import "./App.css";

export function RunWasm() {
  const { result: message } = actions.call({
    actionId: "8fdaccdfdbef4a3b957c533527730554",
    applicationId: "bba78376a21846e683078d7a9019c8eb",
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
