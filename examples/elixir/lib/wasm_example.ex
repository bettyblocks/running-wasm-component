defmodule WasmExample do
  @moduledoc """
  Wasm Example is a simple example of how to call a wasm function from Elixir.
  """

  @type action_result :: {:ok, any()} | {:error, any()}

  @spec call_action(binary, binary, map) :: {:ok, action_result} | {:error, any}
  def call_action(application_id, action_id, input) do
    Wasmex.Components.call_function(
      :wasm_example,
      {"betty-blocks:custom/actions@0.1.0", "call"},
      [
        %{
          "application-id": application_id,
          "action-id": action_id,
          payload: %{input: Jason.encode!(input)}
        }
      ]
    )
  end
end
