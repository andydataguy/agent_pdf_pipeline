import logfire
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class LogfireLogger:
    """
    Centralized Logfire logging class with configuration in this file.
    """

    def __init__(self, config=None):
        """
        Initializes LogfireLogger. Configuration is now primarily within this file,
        with console log level defaulting to DEBUG for detailed output.
        """
        # Get Logfire token from environment variables
        self.logfire_token = os.getenv('LOGFIRE_TOKEN')
        self.logfire_enabled = True  # Logfire platform logging enabled by default

        # Centralized console log level configuration - DEBUG for detailed output
        self.console_log_level = "debug"

        # YAML config can still override Logfire platform enablement
        if config and 'logging_module' in config:
            logging_config = config['logging_module']
            self.logfire_enabled = logging_config.get('logfire_enabled', True)

        try:
            # Configure console logging - always DEBUG level
            console_options = logfire.ConsoleOptions(
                min_log_level=self.console_log_level,
                colors=True
            )

            # Configure Logfire platform if enabled and token available
            if self.logfire_enabled and self.logfire_token:
                logfire.configure(
                    token=self.logfire_token,
                    console=console_options
                )
            else:
                # Console-only logging if Logfire platform is disabled or token missing
                logfire.configure(console=console_options)
        except Exception as e:
            print(f"Warning: Failed to configure Logfire: {e}")
            # Fallback to basic console configuration
            logfire.configure(
                console=logfire.ConsoleOptions(
                    min_log_level='debug', # Fallback to DEBUG level
                    colors=True
                )
            )
        logfire.debug(f"LogfireLogger initialized with console_log_level: {self.console_log_level}")


    def log_debug(self, message, **kwargs):
        """Log debug message."""
        logfire.debug(message, **kwargs)

    def log_info(self, message, **kwargs):
        """Log info message."""
        logfire.info(message, **kwargs)

    def log_warning(self, message, **kwargs):
        """Log warning message."""
        logfire.warning(message, **kwargs)

    def log_error(self, message, **kwargs):
        """Log error message."""
        logfire.error(message, **kwargs)

    def log_critical(self, message, **kwargs):
        """Log critical message."""
        logfire.fatal(message, **kwargs)