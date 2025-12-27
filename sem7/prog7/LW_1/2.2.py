import threading
import requests


urls = [
    "https://upload.wikimedia.org/wikipedia/commons/4/47/PNG_transparency_demonstration_1.png",
    "https://upload.wikimedia.org/wikipedia/commons/3/3f/Placeholder_view_vector.svg",
    "https://upload.wikimedia.org/wikipedia/commons/6/66/Example_image.png"
]


def download_file(url):
    r = requests.get(url)
    filename = url.split("/")[-1] + ".png"
    with open(filename, "wb") as f:
        f.write(r.content)
    print(f"Скачан файл: {filename}")

threads = []

for url in urls:
    t = threading.Thread(target=download_file, args=(url,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
