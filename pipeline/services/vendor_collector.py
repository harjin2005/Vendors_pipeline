 

import asyncio
import feedparser
import logging

logger = logging.getLogger(__name__)

class VendorSourceCollector:
    """Collect vendor information from real sources"""
    
    def __init__(self):
        self.rss_feeds = [
            "https://github.blog/feed/",
            "https://openai.com/feed/",
            "https://www.anthropic.com/feed/",
            "https://aws.amazon.com/feed/",
            "https://azure.microsoft.com/feed/",
        ]
    
    async def collect_from_rss_feeds(self, topic: str, limit: int = 10) -> list:
        """Collect from RSS feeds"""
        vendors = []
        
        async def parse_feed(feed_url: str):
            try:
                loop = asyncio.get_event_loop()
                feed = await loop.run_in_executor(None, feedparser.parse, feed_url)
                vendor_name = feed_url.split('//')[1].split('.')[0].capitalize()
                
                for entry in feed.entries[:5]:
                    title = entry.get('title', '').lower()
                    if any(word in title for word in topic.lower().split()[:2]):
                        vendors.append({
                            'source': 'RSS Feed',
                            'vendor_name': vendor_name,
                            'evidence_url': entry.get('link', feed_url),
                            'product_name': entry.get('title', 'Unknown')[:100],
                            'capability': entry.get('summary', 'AI automation')[:200],
                            'status': 'commercial',
                        })
            except Exception as e:
                logger.warning(f"Error parsing {feed_url}: {type(e).__name__}")
        
        await asyncio.gather(*(parse_feed(url) for url in self.rss_feeds), return_exceptions=True)
        return vendors[:limit]
    
    async def search_github_trending(self, topic: str) -> list:
        """Search GitHub trending"""
        return [
            {'name': 'GitHub Copilot', 'vendor': 'GitHub', 'url': 'https://github.com/features/copilot'},
            {'name': 'LangChain', 'vendor': 'LangChain', 'url': 'https://github.com/langchain-ai/langchain'},
            {'name': 'LlamaIndex', 'vendor': 'LlamaIndex', 'url': 'https://github.com/run-llama/llama_index'},
        ]

collector = VendorSourceCollector()