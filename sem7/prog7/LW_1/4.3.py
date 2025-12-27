import asyncio
import random


async def task1():
    await asyncio.sleep(random.uniform(1, 3))
    result = "Результат task1"
    print("task1 завершена")
    return result

async def task2():
    await asyncio.sleep(random.uniform(1, 3))
    result = "Результат task2"
    print("task2 завершена")
    return result

def process_results(results):
    for i, res in enumerate(results, 1):
        print(f"Обработка результата {i}: {res}")

async def main():
    results = await asyncio.gather(task1(), task2())
    process_results(results)

if __name__ == "__main__":
    asyncio.run(main())
