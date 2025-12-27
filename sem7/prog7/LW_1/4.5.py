import asyncio
import aiohttp
import ssl
import certifi

ssl_context = ssl.create_default_context(cafile=certifi.where())

class AsyncScraper:
    def __init__(self, urls):
        self.urls = urls

    async def fetch(self, session, url):
        try:
            async with session.get(url) as response:
                text = await response.text()
                print(f"[OK] {url} загружен, длина контента: {len(text)} символов")
                return url, text
        except Exception as e:
            print(f"[ERROR] {url} не удалось загрузить: {e}")
            return url, None

    async def scrape_all(self):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context)) as session:
            tasks = [self.fetch(session, url) for url in self.urls]
            results = await asyncio.gather(*tasks)
            return results


if __name__ == "__main__":
    with open("urls.txt", "r") as f:
        urls = [line.strip() for line in f if line.strip()]

    scraper = AsyncScraper(urls)

    results = asyncio.run(scraper.scrape_all())

    for url, content in results:
        if content:
            print(f"{url} загружен успешно, первые 100 символов: {content[:100]}")
        else:
            print(f"{url} не удалось загрузить")
