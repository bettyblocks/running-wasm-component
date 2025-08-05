from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ExecutionResult:
    """Immutable result of WASM component execution."""

    success: bool
    output: str
    exit_code: Optional[int] = None
    execution_time: Optional[float] = None
    error_type: Optional[str] = None
