import wasmtime
import json

wasi_config = wasmtime.WasiConfig()
wasi_config.argv = [
    "app.wasm",
    json.dumps(
        {
            "application-id": "d1b2c3a4e5f6g7h8i9j0k1l2m3n4o5p6",
            "action-id": "56dcad84fde34e508a2419f804c4222b",
            "payload": {"input": json.dumps({})},
        }
    ),
]

wasi_config.inherit_stdout()
wasi_config.inherit_stderr()

engine = wasmtime.Engine()
store = wasmtime.Store(engine)
store.set_wasi(wasi_config)

module = wasmtime.Module.from_file(engine, "app.wasm")

linker = wasmtime.Linker(engine)
linker.define_wasi()

instance = linker.instantiate(store, module)

start = instance.exports(store)["_start"]
start(store)
