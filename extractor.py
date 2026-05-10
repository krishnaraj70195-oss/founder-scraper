from crawl4ai import AsyncWebCrawler

LEADERSHIP_KEYWORDS = [
    "founder",
    "co-founder",
    "ceo",
    "owner",
    "co-owner",
]


class WebsiteExtractor:

    def __init__(self, timeout=45000, proxy=None):
        self.timeout = timeout
        self.proxy = proxy
        self.crawler = None

    async def start(self):
        self.crawler = AsyncWebCrawler()

    async def close(self):
        if self.crawler:
            await self.crawler.close()

    async def scrape_website(self, url, proxy=None):
        """Extract text from website using crawl4ai"""
        try:
            # Use provided proxy or fall back to default
            active_proxy = proxy if proxy is not None else self.proxy

            result = await self.crawler.arun(
                url,
                proxy=active_proxy,
                bypass_cache=True,
                timeout=self.timeout,
            )

            text = result.markdown if result.markdown else ""

            return {
                "text": text,
                "title": result.metadata.get("title", "")
            }

        except Exception as e:
            print(f"[EXTRACT ERROR] {url}: {str(e)[:50]}")
            return {"text": "", "title": ""}

    def extract_leadership_lines(self, text):
        """Extract lines mentioning leadership keywords"""
        lines = text.splitlines()
        matched = []
        seen = set()

        for i, line in enumerate(lines):
            lower = line.lower()

            if any(keyword in lower for keyword in LEADERSHIP_KEYWORDS):
                # Get context around the match
                start = max(0, i - 5)
                end = min(len(lines), i + 6)
                context_block = lines[start:end]

                for context_line in context_block:
                    context_line = context_line.strip()

                    if not context_line or len(context_line) < 2:
                        continue

                    if context_line in seen:
                        continue

                    matched.append(context_line)
                    seen.add(context_line)

        return "\n".join(matched)
