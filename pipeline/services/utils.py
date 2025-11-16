 
import os
import json
import re
import logging

logger = logging.getLogger(__name__)

def safe_json_extract(response_text: str) -> dict:
    """Robust JSON extraction with multiple fallback strategies"""
    if not response_text or not isinstance(response_text, str):
        logger.error(f"Invalid type: {type(response_text)}")
        return {}
    
    logger.debug(f"Response length: {len(response_text)}")
    
    # Strategy 1: Direct parse
    try:
        result = json.loads(response_text)
        logger.info("✅ Direct parse succeeded")
        return result
    except json.JSONDecodeError:
        pass
    
    # Strategy 2: Code block
    try:
        match = re.search(r'```(?:json)?\s*(\{.*?\}|\[.*?\])\s*```', response_text, re.DOTALL)
        if match:
            result = json.loads(match.group(1))
            logger.info("✅ Code block extraction")
            return result
    except (json.JSONDecodeError, AttributeError):
        pass
    
    # Strategy 3: JSON object
    try:
        match = re.search(r'\{(?:[^{}]|(?:\{[^{}]*\}))*\}', response_text)
        if match:
            result = json.loads(match.group(0))
            logger.info("✅ JSON object extraction")
            return result
    except json.JSONDecodeError:
        pass
    
    # Strategy 4: JSON array
    try:
        match = re.search(r'\[(?:[^\[\]]|(?:\[[^\[\]]*\]))*\]', response_text)
        if match:
            data = json.loads(match.group(0))
            result = {'results': data} if isinstance(data, list) else data
            logger.info("✅ JSON array extraction")
            return result
    except json.JSONDecodeError:
        pass
    
    logger.error(f"❌ Failed all strategies")
    return {}

def sanitize_error_message(error: Exception) -> str:
    """Sanitize error messages before sending to client"""
    error_str = str(error)
    
    if any(secret in error_str for secret in ['password', 'secret', 'key', 'token', 'api_key']):
        return "Connection error"
    
    if any(path in error_str for path in ['/', '\\', '.py']):
        return "Internal error"
    
    safe_errors = {
        'timeout': 'Request timeout',
        'connection': 'Connection error',
        'json': 'Invalid data format',
        'value': 'Invalid value',
        'azure': 'Azure service error',
    }
    
    for key, safe_msg in safe_errors.items():
        if key.lower() in error_str.lower():
            return safe_msg
    
    return "An error occurred"

def validate_aps_score(score):
    """Validate APS score is between 0-1"""
    try:
        if isinstance(score, (int, float)):
            return max(0.0, min(1.0, float(score)))
    except (ValueError, TypeError):
        pass
    return 0.5

def get_years():
    """Get past, present, future years"""
    from datetime import datetime
    current = datetime.now().year
    return {
        'past': current - 1,
        'present': current,
        'future': current + 1
    }