defmodule WasmExample.Application do
  @moduledoc false
  use Application

  @wasm_path "./app.wasm"

  @impl true
  def start(_type, _args) do
    children = [
      {Wasmex.Components,
       %{
         path: @wasm_path,
         wasi: %Wasmex.Wasi.WasiP2Options{allow_http: true},
         name: :wasm_example
       }}
    ]

    opts = [strategy: :one_for_one, name: WasmExample.Supervisor]
    Supervisor.start_link(children, opts)
  end
end
