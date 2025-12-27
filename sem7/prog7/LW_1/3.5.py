import threading
import time


event = threading.Event()

def trigger_event():
    time.sleep(3)
    event.set()
    print("Событие установлено")

def wait_for_event():
    event.wait()
    print("Событие произошло")

def monitor_event():
    while not event.is_set():
        print("Событие не произошло")
        time.sleep(1)

if __name__ == "__main__":
    t1 = threading.Thread(target=trigger_event)
    t2 = threading.Thread(target=wait_for_event)
    t3 = threading.Thread(target=monitor_event)

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()
