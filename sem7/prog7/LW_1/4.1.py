import asyncio
from datetime import datetime


async def show_time():
    while True:
        now = datetime.now().strftime("%H:%M:%S")
        print(f"Текущее время: {now}")
        await asyncio.sleep(1)

if __name__ == "__main__":
    try:
        asyncio.run(show_time())
    except KeyboardInterrupt:
        print("\nПрервано пользователем")
