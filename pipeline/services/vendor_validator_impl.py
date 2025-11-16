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

            # If both name and product are present, accept as likely real (best-effort)
            if name and product:
                return {'is_real': True, 'reason': 'has_name_and_product'}

            # Otherwise mark as unverified
            return {'is_real': False, 'reason': 'insufficient_evidence'}

        except Exception as e:
            logger.debug("validator error: %s", e, exc_info=True)
            return {'is_real': False, 'reason': 'error'}


validator = VendorValidator()
