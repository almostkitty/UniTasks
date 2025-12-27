import asyncio
import aiohttp
import asyncpg
import json
import ssl
import certifi

WEB_SERVER_URL = "https://rnacentral.org/api/v1/rna/URS000075C19D"
DB_CONNECTION_STRING = "postgres://reader:NWDMCE5xdipIjRrp@hh-pgsql-public.ebi.ac.uk:5432/pfmegrnargs"

ssl_context = ssl.create_default_context(cafile=certifi.where())

async def fetch_web_data(session):
    async with session.get(WEB_SERVER_URL) as resp:
        data = await resp.json()
        print("\nРезультат запроса к веб-серверу:")
        print(json.dumps(data, indent=2))
        return data


async def fetch_db_data():
    conn = await asyncpg.connect(DB_CONNECTION_STRING, timeout=10)
    query = "SELECT accession, sequence FROM rna LIMIT 5;"
    rows = await conn.fetch(query)
    await conn.close()
    print("\nРезультат запроса к базе данных:")
    for row in rows:
        print(dict(row))
    return rows

async def main():
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context)) as session:
        results = await asyncio.gather(
            fetch_web_data(session),
            fetch_db_data()
        )
        web_result, db_result = results
        print(f"\nВсего записей из базы: {len(db_result)}")
        print(f"Ключи из веб-запроса: {list(web_result.keys())}")

if __name__ == "__main__":
    asyncio.run(main())
