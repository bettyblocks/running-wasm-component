import re
from dataclasses import dataclass
from typing import Dict, Any

from .exceptions import ConfigurationError


@dataclass(frozen=True)
class ComponentConfig:
    """Immutable configuration for a WASM component execution.

    Args:
        application_id: Unique identifier for the application
        action_id: Unique identifier for the action
        payload: Input data for the component
        wasm_file: Path to the WASM file
        timeout: Maximum execution time in seconds

    Raises:
        ConfigurationError: If any configuration parameter is invalid
    """

    application_id: str
    action_id: str
    payload: Dict[str, Any]
    wasm_file: str = "actions.wasm"
    timeout: int = 30

    def __post_init__(self) -> None:
        """Validate configuration after initialization."""
        self._validate_ids()
        self._validate_timeout()
        self._validate_payload()

    def _validate_ids(self) -> None:
        """Validate application and action IDs."""
        # UUID-like pattern validation (32 hex chars)
        id_pattern = re.compile(r"^[a-f0-9]{32}$")

        if not self.application_id or not isinstance(self.application_id, str):
            raise ConfigurationError("application_id must be a non-empty string")

        if not id_pattern.match(self.application_id):
            raise ConfigurationError("application_id must be a 32-character hex string")

        if not self.action_id or not isinstance(self.action_id, str):
            raise ConfigurationError("action_id must be a non-empty string")

        if not id_pattern.match(self.action_id):
            raise ConfigurationError("action_id must be a 32-character hex string")

    def _validate_timeout(self) -> None:
        """Validate timeout value."""
        if not isinstance(self.timeout, int) or self.timeout <= 0:
            raise ConfigurationError("timeout must be a positive integer")

        if self.timeout > 300:  # 5 minutes max
            raise ConfigurationError("timeout cannot exceed 300 seconds")

    def _validate_payload(self) -> None:
        """Validate payload structure."""
        if not isinstance(self.payload, dict):
            raise ConfigurationError("payload must be a dictionary")
