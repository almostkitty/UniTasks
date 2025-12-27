import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests


urls = [
    "https://upload.wikimedia.org/wikipedia/commons/4/42/Chicago_ghetto.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/f/f5/An_African_man_in_Karabakh_by_George_Kennan.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/1/19/Toomas_H_Ilves_pro3.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/6/64/Mauritania_regions_numbered.png"
]

# Семафор для ограничения одновременных потоков
semaphore = threading.Semaphore(3)

def download_image(url):
    with semaphore:
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            r = requests.get(url, headers=headers)
            r.raise_for_status()
            filename = url.split("/")[-1] + ".png"
            with open(filename, "wb") as f:
                f.write(r.content)
            print(f"Скачан файл: {filename}")
        except Exception as e:
            print(f"Ошибка при скачивании {url}: {e}")


if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(download_image, url) for url in urls]
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Ошибка: {e}")
