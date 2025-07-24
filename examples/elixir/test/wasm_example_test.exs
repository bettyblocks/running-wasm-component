defmodule WasmExampleTest do
  use ExUnit.Case

  doctest WasmExample

  test "greets the world" do
    assert WasmExample.hello() == :world
  end
end
