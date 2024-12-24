import numpy as np
import math as m


def to_homogeneous(x, y):
    """Преобразует координаты (x, y) в однородные координаты"""
    return np.array([x, y, 1])

def apply_transformation(point, matrix):
    """Применяет матрицу преобразования к точке в однородных координатах"""
    homogeneous_point = to_homogeneous(point[0], point[1])  # Преобразуем точку в однородные координаты
    transformed_point = np.dot(matrix, homogeneous_point)    # Применяем преобразование
    return transformed_point[:2]  # Возвращаем только x и y координаты

def translation_matrix(dx, dy):
    """Возвращает матрицу трансляции для перемещения на (dx, dy)"""
    return np.array([[1, 0, dx],
                     [0, 1, dy],
                     [0, 0, 1]])

def scaling_matrix(sx, sy):
    """Возвращает матрицу масштабирования для растяжения или сжатия"""
    return np.array([[sx, 0, 0],
                     [0, sy, 0],
                     [0, 0, 1]])

def rotate(angle: float):
    """Создает матрицу вращения на угол angle (в радианах)"""
    cs = m.cos(angle)
    sn = m.sin(angle)
    return np.matrix([
        [cs, sn, 0],
        [-sn, cs, 0],
        [0, 0, 1]
    ])