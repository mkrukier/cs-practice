import numpy as np

# Задание 1
hours = np.arange(0, 22, 3)
line = np.linspace(0, 1, 5)
zeros = np.zeros(6, dtype=int)
unknown_table = np.full((2, 3), -1)
identity = np.eye(3)

print("hours:", hours)
print("shape:", hours.shape, "ndim:", hours.ndim, "size:", hours.size, "dtype:", hours.dtype)

# Задание 2
print("Третий элемент:", hours[2])
print("Последний элемент:", hours[-1])
print("Элементы с индексами 2-5:", hours[2:6])
print("Каждый второй элемент:", hours[::2])
print("В обратном порядке:", hours[::-1])

# Задание 3
temperatures = np.array([
    [12, 14, 13, 15],
    [11, 13, 16, 17],
    [10, 12, 15, 18],
])

print("Форма:", temperatures.shape)
print("Число измерений:", temperatures.ndim)
print("Число элементов:", temperatures.size)
print("Элемент [1, 2]:", temperatures[1, 2])
print("Первая строка:", temperatures[0, :])
print("Последний столбец:", temperatures[:, -1])
print("Первые две строки без первого столбца:\n", temperatures[:2, 1:])
central_fragment = temperatures[:2, 1:3]
print("Центральный фрагмент 2x2:\n", central_fragment)
print("Форма центрального фрагмента:", central_fragment.shape)

# Задание 4
matrix = np.arange(1, 26).reshape(5, 5)

print("Первые три строки:\n", matrix[:3, :])
print("Последние две строки:\n", matrix[-2:, :])
print("Первые два столбца:\n", matrix[:, :2])

fragment = matrix[1:4, 2:5]
print("Фрагмент (строки 1-3, столбцы 2-4):\n", fragment)
print("Форма фрагмента:", fragment.shape)

corner = matrix[-2:, -2:]
print("Угловой блок 2x2:\n", corner)
print("Форма углового блока:", corner.shape)

# Задание 5
changed_hours = hours.copy()
changed_hours[2:5] = 99
changed_hours[::2] = -1

print("Исходный hours:", hours)
print("Измененный changed_hours:", changed_hours)
# .copy() нужен, чтобы создать независимую копию. Без него срез изменил бы и исходный массив hours.

changed_matrix = matrix.copy()
changed_matrix[1, :] = 0
changed_matrix[:, -1] = -1
changed_matrix[1:4, 1:4] = 100

print("Измененная матрица:\n", changed_matrix)
print("Исходная матрица (не изменилась):\n", matrix)

# Задание 6
numbers = np.arange(12)
table = numbers.reshape(3, 4)
transposed = table.T

print("numbers shape:", numbers.shape)
print("table shape:", table.shape)
print("transposed shape:", transposed.shape)
# reshape(3, 4) работает, так как 3 * 4 = 12. reshape(5, 3) вызовет ошибку, так как 5 * 3 = 15, а элементов всего 12.
