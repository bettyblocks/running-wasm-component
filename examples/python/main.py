import subprocess
import json
import sys
import shutil
import logging
import re
import time
from typing import Dict, Any, Tuple, Optional
from dataclasses import dataclass
from pathlib import Path
from contextlib import contextmanager


class WasmRunnerError(Exception):
    """Base exception for WASM runner errors."""


class WasmEnvironmentError(WasmRunnerError):
    """Raised when environment requirements are not met."""


class ConfigurationError(WasmRunnerError):
    """Raised when configuration is invalid."""


class ExecutionError(WasmRunnerError):
    """Raised when WASM execution fails."""


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
    wasm_file: str = "app.wasm"
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


@dataclass(frozen=True)
class ExecutionResult:
    """Immutable result of WASM component execution."""

    success: bool
    output: str
    exit_code: Optional[int] = None
    execution_time: Optional[float] = None
    error_type: Optional[str] = None


class WasmRunner:
    """Robust runner for executing WASM components using wasmtime CLI.

    This class provides a secure and reliable interface for executing
    WASM components with comprehensive error handling and validation.
    """

    # Constants
    CLI_TOOL = "wasmtime"
    CLI_FLAGS = ["-S", "http"]
    MAX_OUTPUT_SIZE = 1024 * 1024  # 1MB

    def __init__(self, log_level: str = "INFO") -> None:
        """Initialize the WASM runner.

        Args:
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

        Raises:
            WasmEnvironmentError: If required tools are not available
        """
        self._setup_logging(log_level)
        self._validate_environment()

    def _setup_logging(self, level: str) -> None:
        """Configure structured logging."""
        try:
            log_level = getattr(logging, level.upper())
        except AttributeError:
            raise ConfigurationError(f"Invalid log level: {level}")

        logging.basicConfig(
            level=log_level,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[
                logging.StreamHandler(sys.stdout),
            ],
        )
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info("WASM runner initialized", extra={"log_level": level})

    def _validate_environment(self) -> None:
        """Validate that required tools are available.

        Raises:
            WasmEnvironmentError: If wasmtime CLI is not found
        """
        if not shutil.which(self.CLI_TOOL):
            raise WasmEnvironmentError(
                f"{self.CLI_TOOL} CLI not found. "
                f"Install with: brew install {self.CLI_TOOL}"
            )

        self.logger.info("Environment validated", extra={"cli_tool": self.CLI_TOOL})

    def _build_invoke_expression(self, config: ComponentConfig) -> str:
        """Build the WAVE invoke expression for the component call.

        Args:
            config: Component configuration

        Returns:
            Properly formatted invoke expression
        """
        # Sanitize payload input to prevent injection
        payload_input = json.dumps(config.payload.get("input", "{}"))

        return (
            f"call({{"
            f'application-id: "{config.application_id}", '
            f'action-id: "{config.action_id}", '
            f"payload: {{input: {payload_input}}}"
            f"}})"
        )

    def _build_command(self, config: ComponentConfig) -> list[str]:
        """Build the wasmtime command with security considerations.

        Args:
            config: Component configuration

        Returns:
            List of command arguments

        Raises:
            ConfigurationError: If WASM file doesn't exist
        """
        wasm_path = Path(config.wasm_file)
        if not wasm_path.exists():
            raise ConfigurationError(f"WASM file not found: {config.wasm_file}")

        # Ensure absolute path for security
        wasm_path = wasm_path.resolve()

        invoke_expr = self._build_invoke_expression(config)

        return [
            self.CLI_TOOL,
            "run",
            "--invoke",
            invoke_expr,
            *self.CLI_FLAGS,
            str(wasm_path),
        ]

    @contextmanager
    def _execution_context(self, config: ComponentConfig):
        """Context manager for safe execution tracking."""

        start_time = time.time()
        self.logger.info(
            "Starting component execution",
            extra={
                "application_id": config.application_id,
                "action_id": config.action_id,
                "timeout": config.timeout,
            },
        )

        try:
            yield start_time
        finally:
            execution_time = time.time() - start_time
            self.logger.info(
                "Execution completed",
                extra={
                    "execution_time": f"{execution_time:.3f}s",
                    "action_id": config.action_id,
                },
            )

    def execute_component(self, config: ComponentConfig) -> ExecutionResult:
        """Execute a WASM component with comprehensive error handling.

        Args:
            config: Component configuration

        Returns:
            ExecutionResult with success status and output

        Raises:
            ExecutionError: If execution fails unexpectedly
        """
        with self._execution_context(config) as start_time:
            try:
                cmd = self._build_command(config)

                # Log command (sanitized for security)
                safe_cmd = cmd.copy()
                safe_cmd[3] = "call({...})"  # Hide sensitive data
                self.logger.debug("Executing command", extra={"command": safe_cmd})

                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=config.timeout,
                    check=False,  # Don't raise on non-zero exit
                )

                execution_time = time.time() - start_time

                # Validate output size
                if len(result.stdout) > self.MAX_OUTPUT_SIZE:
                    self.logger.warning("Output truncated due to size limit")
                    output = result.stdout[: self.MAX_OUTPUT_SIZE] + "... (truncated)"
                else:
                    output = result.stdout.strip()

                if result.returncode == 0:
                    final_output = output if output else "Success (no output)"
                    self.logger.info(
                        "Component executed successfully",
                        extra={
                            "action_id": config.action_id,
                            "execution_time": f"{execution_time:.3f}s",
                        },
                    )
                    return ExecutionResult(
                        success=True,
                        output=final_output,
                        exit_code=result.returncode,
                        execution_time=execution_time,
                    )
                else:
                    error_msg = (
                        result.stderr.strip() if result.stderr else "Unknown error"
                    )
                    self.logger.error(
                        "Component execution failed",
                        extra={
                            "action_id": config.action_id,
                            "exit_code": result.returncode,
                            "error": error_msg,
                        },
                    )
                    return ExecutionResult(
                        success=False,
                        output=f"Execution failed: {error_msg}",
                        exit_code=result.returncode,
                        execution_time=execution_time,
                        error_type="execution_failure",
                    )

            except subprocess.TimeoutExpired:
                execution_time = time.time() - start_time
                error_msg = f"Execution timed out after {config.timeout}s"
                self.logger.error(
                    "Component execution timeout",
                    extra={"action_id": config.action_id, "timeout": config.timeout},
                )
                return ExecutionResult(
                    success=False,
                    output=error_msg,
                    execution_time=execution_time,
                    error_type="timeout",
                )

            except (OSError, PermissionError) as e:
                execution_time = time.time() - start_time
                error_msg = f"System error: {str(e)}"
                self.logger.error(
                    "System error during execution",
                    extra={
                        "action_id": config.action_id,
                        "error": str(e),
                        "error_type": type(e).__name__,
                    },
                )
                return ExecutionResult(
                    success=False,
                    output=error_msg,
                    execution_time=execution_time,
                    error_type="system_error",
                )

            except Exception as e:
                execution_time = time.time() - start_time
                error_msg = f"Unexpected error: {str(e)}"
                self.logger.exception(
                    "Unexpected error during execution",
                    extra={"action_id": config.action_id},
                )
                raise ExecutionError(error_msg) from e


class BettyBlocksRunner:
    """High-level, type-safe interface for running Betty Blocks WASM components.

    This class provides a clean, callable interface for executing WASM components
    with built-in validation, error handling, and logging.

    Example:
        >>> runner = BettyBlocksRunner(
        ...     application_id="be3c7dec126547c5bdb1870ca9d86778",
        ...     action_id="7c33a2b6355545338b536a4863486d97"
        ... )
        >>> success, result = runner({"key": "value"})
    """

    def __init__(
        self,
        application_id: Optional[str] = None,
        action_id: Optional[str] = None,
        wasm_file: str = "app.wasm",
        timeout: int = 30,
        log_level: str = "INFO",
    ) -> None:
        """Initialize the Betty Blocks runner.

        Args:
            application_id: Unique identifier for the application
            action_id: Unique identifier for the action
            wasm_file: Path to the WASM file
            timeout: Maximum execution time in seconds
            log_level: Logging level

        Raises:
            WasmEnvironmentError: If required tools are not available
        """
        self._wasm_runner = WasmRunner(log_level)
        self._application_id = application_id
        self._action_id = action_id
        self._wasm_file = wasm_file
        self._timeout = timeout

        self.logger = logging.getLogger(self.__class__.__name__)

    def __call__(self, input_data: Optional[Dict[str, Any]] = None) -> Tuple[bool, str]:
        """Make the runner callable directly with input data.

        Args:
            input_data: Input data for the component

        Returns:
            Tuple of (success, result_message)

        Raises:
            ConfigurationError: If application_id or action_id not set
        """
        if self._application_id is None or self._action_id is None:
            raise ConfigurationError(
                "application_id and action_id must be set in constructor "
                "to use callable interface"
            )

        return self.run_single(self._application_id, self._action_id, input_data)

    def create_config(
        self,
        application_id: str,
        action_id: str,
        input_data: Optional[Dict[str, Any]] = None,
    ) -> ComponentConfig:
        """Create a validated component configuration.

        Args:
            application_id: Unique identifier for the application
            action_id: Unique identifier for the action
            input_data: Input data for the component

        Returns:
            Validated ComponentConfig instance

        Raises:
            ConfigurationError: If configuration is invalid
        """
        if input_data is None:
            input_data = {}

        # Validate input data structure
        if not isinstance(input_data, dict):
            raise ConfigurationError("input_data must be a valid dictionary")

        # Sanitize input data (remove None values, validate types)
        sanitized_input = {
            k: v for k, v in input_data.items() if v is not None and isinstance(k, str)
        }

        return ComponentConfig(
            application_id=application_id,
            action_id=action_id,
            payload={"input": json.dumps(sanitized_input)},
            wasm_file=self._wasm_file,
            timeout=self._timeout,
        )

    def run_single(
        self,
        application_id: str,
        action_id: str,
        input_data: Optional[Dict[str, Any]] = None,
    ) -> Tuple[bool, str]:
        """Run a single Betty Blocks component.

        Args:
            application_id: Unique identifier for the application
            action_id: Unique identifier for the action
            input_data: Input data for the component

        Returns:
            Tuple of (success, result_message)

        Raises:
            ConfigurationError: If configuration is invalid
            ExecutionError: If execution fails unexpectedly
        """
        try:
            config = self.create_config(application_id, action_id, input_data)
            result = self._wasm_runner.execute_component(config)
            return result.success, result.output

        except (ConfigurationError, ExecutionError):
            # Re-raise configuration and execution errors
            raise
        except Exception as e:
            self.logger.exception("Unexpected error in run_single")
            raise ExecutionError(f"Unexpected error: {str(e)}") from e


def main() -> None:
    try:
        runner = BettyBlocksRunner(
            application_id="be3c7dec126547c5bdb1870ca9d86778",
            action_id="7c33a2b6355545338b536a4863486d97",
        )

        success, result = runner({})

        if success:
            print(f"Result: {result}")
        else:
            print(f"Error: {result}")
            sys.exit(1)

    except ConfigurationError as e:
        print(f"Configuration error: {e}")
        sys.exit(2)
    except WasmEnvironmentError as e:
        print(f"Environment error: {e}")
        sys.exit(3)
    except ExecutionError as e:
        print(f"Execution error: {e}")
        sys.exit(4)
    except KeyboardInterrupt:
        print(" Execution interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"Fatal error: {e}")
        logging.getLogger(__name__).exception("Fatal error in main")
        sys.exit(1)


if __name__ == "__main__":
    main()
