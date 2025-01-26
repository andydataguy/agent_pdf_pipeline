import logfire  # Import the Logfire library
import logging # Import the standard logging library for level number constants

class LogfireLogger:
    """
    A generic, copy-paste ready template for Logfire logging in any Python project.
    Provides structured and configurable logging with sensible defaults.

    To use this in your project:
    1. Copy this logfire.py file to a 'Logger' subdirectory within your 'Utils' directory (or similar).
    2. Ensure you have the 'logfire' library installed (pip install logfire).
    3. Obtain your Logfire WRITE_TOKEN from the Logfire dashboard (create a project if needed).
    4. Set the LOGFIRE_TOKEN environment variable in your system or .env file.
    5. In your Python modules, import LogfireLogger:
       `from src.Utils.Logger.logfire import LogfireLogger`
    6. Initialize the logger with your configuration:
       `logger = LogfireLogger(config=config, service_name=__name__)`
       (Pass the loaded YAML config dictionary and a unique service_name for each module)
    7. Use logger methods for logging:
       `logger.log_info("Informational message", module="MyModule", operation="start")`
       `logger.log_debug("Detailed debug info", variable_value=variable)`
       `logger.log_warning("Potential issue detected", file_path=file)`
       `logger.log_error("Critical error occurred", error_details=error, exc_info=True)`
    8. Customize logging levels and Logfire behavior via the 'logging_module' section in your YAML config file.
    """

    def __init__(self, project_name="default-project", service_name="generic-service", environment="development", config=None):
        """
        Initializes the LogfireLogger with project details and configuration.

        Args:
            project_name (str, optional): Your Logfire project name. Defaults to "default-project".
            service_name (str, optional): The name of this service/application. Defaults to "generic-service".
            environment (str, optional): The environment (development, staging, production). Defaults to "development".
            config (dict, optional): Configuration dictionary loaded from YAML. Defaults to None.
        """
        console_log_level_name = "INFO"  # Default console log level name (string representation)
        console_log_level_number = logging.INFO # Default console log level number (integer representation from logging)


        if config and 'logging_module' in config:
            logging_config = config['logging_module']
            console_log_level_config = logging_config.get('console_log_level')
            if console_log_level_config:
                console_log_level_name = console_log_level_config.upper() # Ensure uppercase for level name
                try:
                    console_log_level_number = getattr(logging, console_log_level_name) # Get integer level from logging
                except AttributeError:
                    print(f"Warning: Invalid console_log_level '{console_log_level_config}' in YAML, defaulting to INFO.")
                    console_log_level_number = logging.INFO # Fallback to INFO if invalid level name


        console_options = logfire.ConsoleOptions(min_log_level=console_log_level_number, colors=True) # Use integer level, enable colors

        logfire.configure(
            project_name=project_name,
            service_name=service_name,
            environment=environment,
            console=console_options,
            send_to_logfire=config and config['logging_module'].get('logfire_enabled', True) if config and 'logging_module' in config else True # Control sending to Logfire via YAML
        )

        self.logger = logfire  # Assign logfire to self.logger for easy access

    def log_info(self, message, **kwargs):
        """Logs an informational message."""
        self.logger.info(message, **kwargs)

    def log_debug(self, message, **kwargs):
        """Logs a debug message (for detailed development info)."""
        self.logger.debug(message, **kwargs)

    def log_warning(self, message, **kwargs):
        """Logs a warning message (for potential issues)."""
        self.logger.warn(message, **kwargs)

    def log_error(self, message, exc_info=True, **kwargs):
        """Logs an error message (for errors and exceptions)."""
        self.logger.error(message, exc_info=exc_info, **kwargs)

# Example usage (in your application modules):
# from src.Utils.Logger.logfire import LogfireLogger
# logger = LogfireLogger(config=config, service_name=__name__) # Pass config and module name
# logger.log_info("Starting processing...", module="MyModule", operation="start")