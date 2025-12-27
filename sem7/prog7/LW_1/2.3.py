import threading
import requests


urls = [
    "https://httpbin.org/get",
    "https://api.github.com",
    "https://jsonplaceholder.typicode.com/todos/1"
]

def make_request(url):
    r = requests.get(url)
    print(f"{url} -> статус {r.status_code}")

threads = []

for url in urls:
    t = threading.Thread(target=make_request, args=(url,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
