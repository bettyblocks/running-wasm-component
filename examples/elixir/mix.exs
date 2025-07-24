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
      {:wasmex,
       git: "https://github.com/tessi/wasmex.git", rev: "e8d2f63cdf278ced11720cc58d93f96f72cb9872"},
      {:styler, "~> 1.4", only: [:dev, :test], runtime: false}
    ]
  end
end
