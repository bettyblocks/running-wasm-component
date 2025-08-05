#!/usr/bin/env python3

import sys
import logging

from src import (
    BettyBlocksRunner,
    ConfigurationError,
    WasmEnvironmentError,
    ExecutionError,
)


def main() -> None:
    try:
        # Create runner with placeholder IDs (replace with actual values)
        runner = BettyBlocksRunner(
            application_id="<YOUR_APPLICATION_ID>",
            action_id="<YOUR_ACTION_ID>",
        )

        # Run with empty input (customize as needed)
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
