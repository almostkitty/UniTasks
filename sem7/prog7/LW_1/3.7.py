import threading
import time

barrier = threading.Barrier(2)

def server():
    print("Сервер запускается")
    time.sleep(3)
    print("Сервер готов к работе")
    barrier.wait()
    print("Сервер получил запрос от клиента")

def client():
    print("Клиент ожидает готовности сервера")
    barrier.wait()
    print("Клиент отправляет запрос серверу")

if __name__ == "__main__":
    t_server = threading.Thread(target=server)
    t_client = threading.Thread(target=client)

    t_server.start()
    t_client.start()

    t_server.join()
    t_client.join()
