defmodule WasmExample.MixProject do
  use Mix.Project

  def project do
    [
      app: :wasm_example,
      version: "0.1.0",
      elixir: "~> 1.17",
      start_permanent: Mix.env() == :prod,
      deps: deps()
    ]
  end

  # Run "mix help compile.app" to learn about applications.
  def application do
    [
      extra_applications: [:logger],
      mod: {WasmExample.Application, []}
    ]
  end

  # Run "mix help deps" to learn about dependencies.
  defp deps do
    [
      {:wasmex, "~> 0.12"},
      {:styler, "~> 1.4", only: [:dev, :test], runtime: false},
      {:jason, "~> 1.4"}
    ]
  end
end
