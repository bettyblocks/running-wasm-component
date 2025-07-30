import React from "react";
import { actions } from "./dist/app.js";

export function Component() {
  const {result: message} = actions.call({
    actionId: "bba78376a21846e683078d7a9019c8eb",
    applicationId: "bba78376a21846e683078d7a9019c8eb",
    payload: {
      input: JSON.stringify({}),
    },
  });

  return <p>{JSON.parse(message).output}</p>
}
