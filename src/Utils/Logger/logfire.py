# src/Utils/Logger/logfire.py

import logfire
import os
from pathlib import Path
from typing import Optional, Any
from contextlib import contextmanager

class LogfireManager:
    """Centralized Logfire management with production-ready defaults"""
    
    _configured = False

    def __init__(self):
        if not self._configured:
            raise RuntimeError("Must call configure() before instantiation")

    @classmethod
    def configure(cls,
                 token: Optional[str] = None,
                 project_name: Optional[str] = None,
                 environment: Optional[str] = None):
        """One-time configuration for Logfire"""
        if cls._configured:
            return

        # Environment-based defaults
        base_config = {
            'token': token or os.getenv('LOGFIRE_TOKEN'),
            'project_name': project_name or Path.cwd().name,
            'environment': environment or os.getenv('LOGFIRE_ENVIRONMENT', 'development'),
            'send_to_logfire': 'if-token-present',
            'inspect_arguments': True,
            'scrubbing': os.getenv('LOGFIRE_SCRUBBING', 'true').lower() == 'true',
            'console': os.getenv('LOGFIRE_CONSOLE', 'true').lower() == 'true',
            'auto_trace': os.getenv('LOGFIRE_AUTO_TRACE', 'true').lower() == 'true'
        }

        # Configure core Logfire settings
        logfire.configure(**base_config)

        # Auto-instrument common packages
        if base_config['auto_trace']:
            self._auto_instrument()

        cls._configured = True

    @staticmethod
    def _auto_instrument():
        """Automatically instrument common libraries"""
        try:
            # Web frameworks
            logfire.instrument_fastapi()
            logfire.instrument_django()
            
            # Databases
            logfire.instrument_sqlalchemy()
            logfire.instrument_redis()
            
            # HTTP clients
            logfire.instrument_httpx()
            logfire.instrument_requests()
            
            logfire.info("Auto-instrumentation complete")
        except ImportError as e:
            logfire.warning(f"Auto-instrumentation skipped: {str(e)}")

    @classmethod
    @contextmanager
    def traced_operation(cls, name: str, **kwargs: Any):
        """Context manager for rich span creation"""
        with logfire.span(name, **kwargs) as span:
            yield span

    @classmethod
    def instrument_function(cls, func=None, *, name: Optional[str] = None):
        """Decorator for automatic function instrumentation"""
        def decorator(f):
            wrapped = logfire.instrument(
                name or f"{f.__module__}.{f.__name__}",
                extract_args=True
            )(f)
            return wrapped
        return decorator(func) if func else decorator

# Configuration (automatically uses environment variables)
LogfireManager.configure()

# Export core functionality
configure = LogfireManager.configure
traced_operation = LogfireManager.traced_operation
instrument_function = LogfireManager.instrument_function
log = logfire  # Direct access to logfire API