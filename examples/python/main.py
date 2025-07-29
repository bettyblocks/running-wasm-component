import subprocess
import json
import sys
import os
import shutil
import logging
from typing import Dict, Any, Tuple
from dataclasses import dataclass


@dataclass
class ComponentConfig:
    """Configuration for a WASM component execution."""

    application_id: str
    action_id: str
    payload: Dict[str, Any]
    wasm_file: str = "app.wasm"
    timeout: int = 30


class WasmRunner:
    """Runner for executing WASM components using wasmtime CLI."""

    def __init__(self, log_level: str = "INFO"):
        """Initialize the WASM runner."""
        self.setup_logging(log_level)
        self.validate_environment()

    def setup_logging(self, level: str) -> None:
        """Configure logging."""
        logging.basicConfig(
            level=getattr(logging, level.upper()),
            format="%(asctime)s - %(levelname)s - %(message)s",
        )
        self.logger = logging.getLogger(__name__)

    def validate_environment(self) -> None:
        """Validate that required tools are available."""
        if not shutil.which("wasmtime"):
            raise RuntimeError(
                "wasmtime CLI not found. Install with: brew install wasmtime"
            )
        else:
            self.logger.info("wasmtime CLI found")

    def build_invoke_expression(self, config: ComponentConfig) -> str:
        """Build the WAVE invoke expression for the component call."""
        payload_input = config.payload.get("input", "{}")
        return f'call({{application-id: "{config.application_id}", action-id: "{config.action_id}", payload: {{input: "{payload_input}"}}}})'

    def build_command(self, config: ComponentConfig) -> list[str]:
        """Build the wasmtime command."""
        invoke_expr = self.build_invoke_expression(config)
        return [
            "wasmtime",
            "run",
            "--invoke",
            invoke_expr,
            "-S",
            "http",
            config.wasm_file,
        ]

    def execute_component(self, config: ComponentConfig) -> Tuple[bool, str]:
        """Execute a single WASM component."""
        try:
            if not os.path.exists(config.wasm_file):
                error_msg = f"WASM file not found: {config.wasm_file}"
                self.logger.error(error_msg)
                return False, error_msg

            cmd = self.build_command(config)
            self.logger.info(
                f"Executing: {' '.join(cmd[:4])} \"{cmd[4]}\" {' '.join(cmd[5:])}"
            )

            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=config.timeout
            )

            if result.returncode == 0:
                output = (
                    result.stdout.strip()
                    if result.stdout.strip()
                    else "Success (no output)"
                )
                self.logger.info(f"Component executed successfully: {config.action_id}")
                return True, output
            else:
                error_msg = f"Component execution failed: {result.stderr}"
                self.logger.error(error_msg)
                return False, error_msg

        except subprocess.TimeoutExpired:
            error_msg = f"Component execution timed out after {config.timeout}s"
            self.logger.error(error_msg)
            return False, error_msg
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            self.logger.error(error_msg)
            return False, error_msg


class BettyBlocksRunner:
    """High-level interface for running Betty Blocks WASM components."""

    def __init__(self, application_id: str = None, action_id: str = None):
        """Initialize the Betty Blocks runner."""
        self.wasm_runner = WasmRunner()
        self.application_id = application_id
        self.action_id = action_id

    def __call__(self, input_data: Dict = None) -> Tuple[bool, str]:
        if self.application_id is None or self.action_id is None:
            raise ValueError(
                "application_id and action_id must be set in constructor to use callable interface"
            )

        return self.run_single(self.application_id, self.action_id, input_data)

    def create_config(
        self, application_id: str, action_id: str, input_data: Dict = None
    ) -> ComponentConfig:
        """Create a component configuration."""
        if input_data is None:
            input_data = {}

        return ComponentConfig(
            application_id=application_id,
            action_id=action_id,
            payload={"input": json.dumps(input_data)},
        )

    def run_single(
        self, application_id: str, action_id: str, input_data: Dict = None
    ) -> Tuple[bool, str]:
        """Run a single Betty Blocks component."""
        config = self.create_config(application_id, action_id, input_data)
        return self.wasm_runner.execute_component(config)


def main():
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

    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
