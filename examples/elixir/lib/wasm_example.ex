defmodule WasmExample do
  @moduledoc """
  Documentation for `WasmExample`.
  """

  def call_action do
    Wasmex.Components.call_function(
      :wasm_example,
      {"betty-blocks:custom/actions@0.1.0", "call"},
      [
        %{
          "application-id": "1234",
          "action-id": "c97afce16ad441fc8c0c597151b9bcf9",
          payload: %{input: "{}"}
        }
      ]
    )
  end
end
