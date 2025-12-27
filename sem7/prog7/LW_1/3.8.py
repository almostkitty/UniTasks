import threading
import os
import random
import string


search_dir = "./test_dir"
search_filename = "target_file.txt"
num_files = 20
num_random_chars = 5

file_found_event = threading.Event()

def create_test_directory():
    if not os.path.exists(search_dir):
        os.makedirs(search_dir)
    for i in range(num_files):
        name = ''.join(random.choices(string.ascii_lowercase, k=num_random_chars)) + ".txt"
        path = os.path.join(search_dir, name)
        with open(path, "w") as f:
            f.write(f"Содержимое файла {name}\n")
    target_path = os.path.join(search_dir, search_filename)
    with open(target_path, "w") as f:
        f.write("Целевой файл\n")
    print(f"Директория '{search_dir}' создана и заполнена {num_files} файлами + целевой файл.")


def search_files(file_list):
    for f in file_list:
        if file_found_event.is_set():
            return
        if f == search_filename:
            print(f"Файл найден: {os.path.join(search_dir, f)}")
            file_found_event.set()
            return


if __name__ == "__main__":
    create_test_directory()
    all_files = os.listdir(search_dir)

    chunk_size = len(all_files) // 3
    file_chunks = [all_files[i*chunk_size : (i+1)*chunk_size] for i in range(3)]
    if len(all_files) % 3 != 0:
        file_chunks[-1].extend(all_files[3*chunk_size:])

    threads = []
    for chunk in file_chunks:
        t = threading.Thread(target=search_files, args=(chunk,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    if not file_found_event.is_set():
        print("Файл не найден")
