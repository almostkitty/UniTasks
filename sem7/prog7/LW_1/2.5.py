import threading


def quicksort(arr):
    if len(arr) <= 1:
        return arr

    pivot = arr[0]
    left = []
    right = []

    for x in arr[1:]:
        if x < pivot:
            left.append(x)
        else:
            right.append(x)

    left_sorted, right_sorted = [], []

    # Сортировка подмассивов в отдельных потоках
    def sort_left():
        nonlocal left_sorted
        left_sorted = quicksort(left)

    def sort_right():
        nonlocal right_sorted
        right_sorted = quicksort(right)

    t1 = threading.Thread(target=sort_left)
    t2 = threading.Thread(target=sort_right)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    return left_sorted + [pivot] + right_sorted

arr = [5, 3, 8, 1, 2, 23, 6, 11, 22, 7, 6, 4]
sorted_arr = quicksort(arr)
print("Отсортированный массив:", sorted_arr)
