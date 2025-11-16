"""
Global exception handler for REST API errors.

Provides consistent error responses across all endpoints,
with proper logging and sanitization of sensitive information.
"""

import logging
import traceback
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Custom exception handler that wraps DRF's default handler.
    
    Features:
    - Consistent error response format
    - Detailed logging with traceback for server errors
    - Sanitization of sensitive information
    - Proper HTTP status codes
    """
    
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if response is None:
        # If DRF's handler returns None, handle unhandled exceptions
        logger.error(
            f"Unhandled exception: {type(exc).__name__}: {str(exc)}",
            exc_info=True,
            extra={'traceback': traceback.format_exc()}
        )
        return Response(
            {
                'error': 'Internal server error',
                'detail': 'An unexpected error occurred. Please try again later.',
                'type': type(exc).__name__,
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    # Log validation errors (4xx)
    if 400 <= response.status_code < 500:
        logger.warning(
            f"{type(exc).__name__} at {context.get('request').path}",
            extra={'status': response.status_code, 'detail': response.data}
        )

    # Log server errors (5xx)
    if 500 <= response.status_code < 600:
        logger.error(
            f"Server error: {type(exc).__name__}",
            exc_info=True,
            extra={'traceback': traceback.format_exc()}
        )

    # Sanitize response to remove sensitive information
    response.data = sanitize_error_response(response.data)

    return response


def sanitize_error_response(data):
    """
    Sanitize error response to remove or mask sensitive information.
    
    Masks:
    - File paths
    - SQL queries
    - API keys / secrets
    - Internal stack traces (in production)
    """
    if not isinstance(data, dict):
        return data

    sanitized = {}
    
    for key, value in data.items():
        # Don't expose internal details in production
        if key in ('traceback', 'exc_info', 'internal_error'):
            continue
        
        # Sanitize string values
        if isinstance(value, str):
            # Mask file paths
            if '/' in value or '\\' in value:
                value = mask_file_paths(value)
            # Mask SQL
            if value.upper().startswith(('SELECT', 'INSERT', 'UPDATE', 'DELETE')):
                value = '[SQL Query Redacted]'
            # Mask common secrets
            if any(secret in value.lower() for secret in ['password', 'token', 'secret', 'key', 'api']):
                value = '[Sensitive Data Redacted]'
        
        # Recursively sanitize nested dicts
        elif isinstance(value, dict):
            value = sanitize_error_response(value)
        
        # Sanitize lists
        elif isinstance(value, list):
            value = [sanitize_error_response(item) if isinstance(item, dict) else item for item in value]
        
        sanitized[key] = value
    
    return sanitized


def mask_file_paths(text):
    """
    Replace file paths in error messages with generic placeholders.
    """
    import re
    
    # Windows paths: C:\path\to\file
    text = re.sub(r'[a-zA-Z]:\\[^\s"\']+', '[file path]', text)
    
    # Unix paths: /path/to/file
    text = re.sub(r'/[^\s"\']+(?:/|\.py)', '[file path]', text)
    
    return text


class BadRequestException(Exception):
    """Custom bad request exception with default message."""
    def __init__(self, detail='Invalid request', code='bad_request'):
        self.detail = detail
        self.code = code
        super().__init__(self.detail)


class ValidationException(Exception):
    """Custom validation exception for domain logic."""
    def __init__(self, detail='Validation failed', field=None):
        self.detail = detail
        self.field = field
        super().__init__(self.detail)


class PhaseExecutionException(Exception):
    """Exception raised during phase execution."""
    def __init__(self, phase, detail, step=None):
        self.phase = phase
        self.detail = detail
        self.step = step
        super().__init__(f"Phase {phase} failed at step {step}: {detail}")


class LLMException(Exception):
    """Exception raised when LLM service fails."""
    def __init__(self, detail, retries=0):
        self.detail = detail
        self.retries = retries
        super().__init__(f"LLM Error (retries: {retries}): {detail}")
