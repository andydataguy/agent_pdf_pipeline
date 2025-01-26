import logfire
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class LogfireLogger:
    """
    The ABSOLUTE SIMPLEST, copy-paste ready template for Logfire logging in any Python project.
    Provides basic, configurable console logging and Logfire platform integration.
    """

    def __init__(self, config=None): 
        """
        Initializes the LogfireLogger with configuration from YAML and environment variables.

        Args:
            config (dict, optional): Configuration dictionary loaded from YAML. Defaults to None.
        """
        # Get Logfire token from environment variables
        self.logfire_token = os.getenv('LOGFIRE_TOKEN')
        
        # Default configuration using string log levels
        self.console_log_level = "info"
        self.logfire_enabled = True

        # Override defaults with YAML config if provided
        if config and 'logging_module' in config:
            logging_config = config['logging_module']
            # Map config log levels to Logfire log levels
            level_map = {
                'DEBUG': 'debug',
                'INFO': 'info',
                'WARNING': 'warning',
                'ERROR': 'error',
                'CRITICAL': 'fatal'
            }
            config_level = logging_config.get('console_log_level', 'INFO').upper()
            self.console_log_level = level_map.get(config_level, 'info')
            self.logfire_enabled = logging_config.get('logfire_enabled', True)

        try:
            # Configure console logging
            console_options = logfire.ConsoleOptions(
                min_log_level=self.console_log_level,
                colors=True
            )

            # Configure Logfire if enabled and token is available
            if self.logfire_enabled and self.logfire_token:
                logfire.configure(
                    token=self.logfire_token,
                    console=console_options
                )
            else:
                # Console-only logging
                logfire.configure(console=console_options)
        except Exception as e:
            print(f"Warning: Failed to configure Logfire: {e}")
            # Fallback to basic console configuration
            logfire.configure(
                console=logfire.ConsoleOptions(
                    min_log_level='info',
                    colors=True
                )
            )

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

# Example usage (in your application modules):
# from src.Utils.Logger.logfire import LogfireLogger
# logger = LogfireLogger(config=config) # Simplest initialization - no arguments
# logger.log_info("Starting processing...") # Simple logging calls