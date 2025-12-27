import threading


def print_name():
    print(f"Имя потока: {threading.current_thread().name}")

threads = []

for i in range(8):
    t = threading.Thread(target=print_name, name=f"Thread-{i+1}")
    threads.append(t)
    t.start()

for t in threads:
    t.join()
