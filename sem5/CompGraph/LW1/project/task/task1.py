import pygame
import numpy as np
from squares import Drawer, apply_transformation

def task_1():
    pygame.init()

    # Создаем окно для задачи 1
    width, height = 600, 600
    origin = (300, 300)  # Центр системы координат
    unit_x = unit_y = 50  # Масштаб для координат
    drawer = Drawer(width, height, 32, origin, unit_x, unit_y)
    drawer.initialize("Задача 1: Преобразование точки")

    # Матрица преобразования T
    T = np.array([[1, 3, 0],
                  [4, 1, 0],
                  [0, 0, 1]])

    # Ввод координат точки
    x = float(input("Введите координаты точки (x): "))
    y = float(input("Введите координаты точки (y): "))
    original_point = np.array([x, y])

    # Применение матричного преобразования
    transformed_point = apply_transformation(original_point, T)

    # Вывод на экран
    print(f"Исходная точка: ({original_point[0]}, {original_point[1]})")
    print(f"Преобразованная точка: ({transformed_point[0]}, {transformed_point[1]})")

    # Визуализация
    drawer.screen.fill((0, 0, 0))  # Очистка экрана
    drawer.draw_axes(-5, 5, -5, 5)  # Отображение осей

    # Рисуем исходную точку
    drawer.color = (255, 0, 0)  # Красная точка для исходной
    drawer.draw_point(original_point[0], original_point[1])

    # Рисуем преобразованную точку
    drawer.color = (0, 255, 0)  # Зеленая точка для преобразованной
    drawer.draw_point(transformed_point[0], transformed_point[1])

    pygame.display.update()  # Обновление экрана

    # Главный цикл для задачи 1
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()

# Запуск задачи
if __name__ == "__main__":
    task_1()
