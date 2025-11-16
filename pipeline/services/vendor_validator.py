import asyncio
import logging
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

class VendorValidator:
    """Simple vendor validator used by phase1.
    
    This is intentionally lightweight: it checks for an evidence URL or
    presence of vendor/product names. You can enhance it later to
    perform HTTP HEAD checks or remote validation.
    """
    
    async def validate_vendor(self, vendor: dict) -> dict:
        """Return a dict with at least `is_real` boolean and `reason` string."""
        try:
            # quick heuristics
            name = (vendor.get('vendor_name') or vendor.get('vendor') or '').strip()
            product = (vendor.get('product_name') or vendor.get('product') or '').strip()
            url = (vendor.get('evidence_url') or vendor.get('evidence') or '')
            
            # If there's an evidence URL that looks valid, accept it
            if url:
                try:
                    parsed = urlparse(url)
                    if parsed.scheme in ('http', 'https') and parsed.netloc:
                        return {'is_real': True, 'reason': 'has_evidence_url'}
                except Exception:
                    pass
            
            # If both name and product are non-empty, probably real
            if name and product:
                return {'is_real': True, 'reason': 'has_name_and_product'}
            
            # If at least one is present, give benefit of doubt
            if name or product:
                return {'is_real': True, 'reason': 'has_partial_info'}
            
            return {'is_real': False, 'reason': 'missing_data'}
        except Exception as e:
            logger.error(f"Validation error: {e}")
            return {'is_real': False, 'reason': 'error'}


# ✅ CRITICAL: Create global instance that can be imported
validator = VendorValidator() 
