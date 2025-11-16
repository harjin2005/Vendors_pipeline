import os
import sys
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def test_env_file():
    """
    Complete .env file validation and testing
    Run this from your Django project root
    """
    
    logger.info("=" * 70)
    logger.info("ENV FILE VALIDATION TEST")
    logger.info("=" * 70)
    
    # ===== TEST 1: Check if .env exists =====
    logger.info("\n[TEST 1] Checking if .env file exists...")
    env_path = Path(".env")
    if not env_path.exists():
        logger.error("ERROR: .env file not found in current directory!")
        logger.info("Please create .env file in: " + str(Path.cwd()))
        return False
    logger.info("OK: .env file found at " + str(env_path.absolute()))
    
    # ===== TEST 2: Load .env variables =====
    logger.info("\n[TEST 2] Loading .env variables...")
    try:
        from dotenv import load_dotenv
        load_dotenv()
        logger.info("OK: Successfully loaded .env file")
    except ImportError:
        logger.error("ERROR: python-dotenv not installed!")
        logger.info("Install: pip install python-dotenv")
        return False
    
    # ===== TEST 3: Check Azure OpenAI variables =====
    logger.info("\n[TEST 3] Checking Azure OpenAI configuration...")
    
    azure_vars = {
        'AZURE_OPENAI_ENDPOINT': os.getenv('AZURE_OPENAI_ENDPOINT'),
        'AZURE_OPENAI_API_KEY': os.getenv('AZURE_OPENAI_API_KEY'),
        'AZURE_OPENAI_DEPLOYMENT': os.getenv('AZURE_OPENAI_DEPLOYMENT'),
        'AZURE_API_VERSION': os.getenv('AZURE_API_VERSION'),
    }
    
    all_present = True
    for key, value in azure_vars.items():
        if value:
            # Mask sensitive data
            if 'KEY' in key:
                display = value[:10] + "***" + value[-5:]
            else:
                display = value
            logger.info(f"  OK: {key} = {display}")
        else:
            logger.error(f"  ERROR: {key} is missing!")
            all_present = False
    
    if not all_present:
        logger.error("ERROR: Missing Azure OpenAI configuration!")
        return False
    
    # ===== TEST 4: Validate Azure OpenAI Endpoint Format =====
    logger.info("\n[TEST 4] Validating Azure OpenAI Endpoint format...")
    endpoint = azure_vars['AZURE_OPENAI_ENDPOINT']
    
    if not endpoint.startswith('https://'):
        logger.error(f"  ERROR: Endpoint must start with 'https://'")
        logger.error(f"  Current: {endpoint}")
        return False
    logger.info(f"  OK: Endpoint format is correct")
    
    # Check for common issues
    if '/api/projects/' in endpoint:
        logger.error(f"  ERROR: Endpoint contains '/api/projects/' path!")
        logger.error(f"  Current: {endpoint}")
        logger.info("  FIX: Remove '/api/projects/...' suffix")
        logger.info(f"  Should be: https://attack-dev-resource.services.ai.azure.com")
        return False
    
    if endpoint.endswith('/'):
        logger.warning(f"  WARNING: Endpoint ends with '/' - might cause issues")
        logger.info(f"  Consider removing: {endpoint[:-1]}")
    
    logger.info(f"  OK: Endpoint format is valid")
    
    # ===== TEST 5: Check Database variables =====
    logger.info("\n[TEST 5] Checking Database configuration...")
    
    db_url = os.getenv('DATABASE_URL')
    use_sqlite = os.getenv('USE_SQLITE', 'false').lower() == 'true'
    
    if use_sqlite:
        logger.info("  OK: Using SQLite")
    else:
        if not db_url:
            logger.error("  ERROR: DATABASE_URL not set while USE_SQLITE=false")
            return False
        logger.info(f"  OK: Using PostgreSQL")
        
        # Validate PostgreSQL connection string
        if not db_url.startswith('postgresql://'):
            logger.error(f"  ERROR: Invalid DATABASE_URL format")
            logger.error(f"  Current: {db_url}")
            logger.info(f"  Format: postgresql://user:password@localhost/database")
            return False
        
        # Check for placeholder password
        if ':replace@' in db_url:
            logger.error(f"  ERROR: Database password is 'replace' (placeholder)!")
            logger.info(f"  Update with actual password in .env file")
            return False
        
        logger.info(f"  OK: Database URL format is valid")
    
    # ===== TEST 6: Test LLM Service Initialization =====
    logger.info("\n[TEST 6] Testing LLM Service initialization...")
    
    try:
        # Import after loading .env
        from pipeline.services.llm_service import llm_service
        
        if llm_service is None:
            logger.warning("  WARNING: LLM service is None")
            logger.warning("  This might be due to:")
            logger.warning("    - Missing Azure credentials")
            logger.warning("    - Missing 'openai' or 'azure-ai-openai' packages")
            logger.info("  Install: pip install openai azure-ai-openai")
        else:
            logger.info("  OK: LLM service initialized successfully")
            logger.info(f"  SDK: {llm_service.sdk}")
            logger.info(f"  Endpoint: {llm_service.endpoint}")
            logger.info(f"  Deployment: {llm_service.deployment}")
    except ImportError as e:
        logger.error(f"  ERROR: Could not import LLM service: {e}")
        return False
    except Exception as e:
        logger.error(f"  ERROR: LLM service initialization failed: {e}")
        return False
    
    # ===== TEST 7: Test Database Connection =====
    logger.info("\n[TEST 7] Testing Database connection...")
    
    try:
        import django
        django.setup()
        
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        logger.info("  OK: Database connection successful")
    except Exception as e:
        logger.error(f"  ERROR: Database connection failed: {e}")
        logger.info("  Check your DATABASE_URL and PostgreSQL/SQLite setup")
        return False
    
    # ===== TEST 8: Django Settings Check =====
    logger.info("\n[TEST 8] Checking Django settings...")
    
    try:
        from django.conf import settings
        logger.info(f"  Environment: {os.getenv('ENVIRONMENT', 'development')}")
        logger.info(f"  Log Level: {os.getenv('LOG_LEVEL', 'INFO')}")
        logger.info(f"  Debug: {settings.DEBUG}")
        logger.info("  OK: Django settings loaded")
    except Exception as e:
        logger.error(f"  ERROR: Django settings failed: {e}")
        return False
    
    # ===== FINAL SUMMARY =====
    logger.info("\n" + "=" * 70)
    logger.info("ENV FILE VALIDATION COMPLETE")
    logger.info("=" * 70)
    
    logger.info("\nCHECKLIST:")
    logger.info("  [✓] .env file exists")
    logger.info("  [✓] Azure OpenAI variables configured")
    logger.info("  [✓] Endpoint format valid")
    logger.info("  [✓] Database configured")
    if llm_service:
        logger.info("  [✓] LLM service initialized")
    else:
        logger.info("  [!] LLM service not initialized (optional)")
    logger.info("  [✓] Database connection working")
    logger.info("  [✓] Django settings loaded")
    
    logger.info("\nSTATUS: All checks passed! Your .env file is working correctly.")
    return True


if __name__ == '__main__':
    # Make sure we're in the right directory
    if not Path('manage.py').exists():
        logger.error("ERROR: Please run this script from your Django project root")
        logger.error("Current directory: " + str(Path.cwd()))
        sys.exit(1)
    
    success = test_env_file()
    sys.exit(0 if success else 1)