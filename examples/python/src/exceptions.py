class WasmRunnerError(Exception):
    """Base exception for WASM runner errors."""


class WasmEnvironmentError(WasmRunnerError):
    """Raised when environment requirements are not met."""


class ConfigurationError(WasmRunnerError):
    """Raised when configuration is invalid."""


class ExecutionError(WasmRunnerError):
    """Raised when WASM execution fails."""
