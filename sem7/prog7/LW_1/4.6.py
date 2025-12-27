import asyncio
import aiohttp
import ssl
import certifi

WEB_SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())

class AsyncScraper:
    def __init__(self, urls):
        self.urls = urls
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=WEB_SSL_CONTEXT))
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def fetch(self, url):
        try:
            async with self.session.get(url) as response:
                text = await response.text()
                print(f"[OK] {url} загружен, длина контента: {len(text)} символов")
                return url, text
        except Exception as e:
            print(f"[ERROR] {url} не удалось загрузить: {e}")
            return url, None

    async def scrape_all(self):
        tasks = [self.fetch(url) for url in self.urls]
        results = await asyncio.gather(*tasks)
        return results


async def main():
    with open("urls.txt", "r") as f:
        urls = [line.strip() for line in f if line.strip()]

    async with AsyncScraper(urls) as scraper:
        results = await scraper.scrape_all()

    for url, content in results:
        if content:
            print(f"{url} загружен успешно, первые 100 символов: {content[:100]}")
        else:
            print(f"{url} не удалось загрузить")

if __name__ == "__main__":
    asyncio.run(main())
