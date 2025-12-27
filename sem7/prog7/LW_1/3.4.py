from concurrent.futures import ThreadPoolExecutor, Future
import threading
import time


FILENAME = "data.txt"

def write_data():
    with open(FILENAME, "w") as f:
        for i in range(5):
            f.write(f"Строка {i+1}\n")
            print(f"Запись: Строка {i+1}")
            time.sleep(1)

def read_data(future: Future):
    future.result()
    with open(FILENAME, "r") as f:
        lines = f.readlines()
        for line in lines:
            print(f"Чтение: {line.strip()}")

if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=2) as executor:
        future_write = executor.submit(write_data)
        future_read = executor.submit(read_data, future_write)
        future_write.result()
        future_read.result()
