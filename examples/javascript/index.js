import { actions } from "./dist/app.js";

const output = actions.call({
  actionId: "8fdaccdfdbef4a3b957c533527730554",
  applicationId: "d1b2c3a4e5f6g7h8i9j0k1l2m3n4o5p6",
  payload: {
    input: JSON.stringify({}),
  },
});

console.log(output);
