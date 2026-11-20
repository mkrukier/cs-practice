import numpy as np

def make_hours() -> list[int]:
    # arange(0, 22, 3): 21 не включается, поэтому 22
    return np.arange(0, 22, 3).tolist()


def vector_report(values: list[float]) -> dict:
    arr = np.array(values)
    return {
        "third": float(arr[2]),              # индекс 2 = третий элемент
        "last": float(arr[-1]),              # -1 = последний
        "middle": arr[2:6].tolist(),         # индексы 2,3,4,5 (6 не входит)
        "every_second": arr[::2].tolist(),   # шаг 2 от начала
        "reversed": arr[::-1].tolist()       # шаг -1 = разворот
    }


def change_vector(values: list[float]) -> list[float]:
    arr = np.array(values).copy()  # copy() — не менять исходный список
    arr[2:5] = 99                  # индексы 2,3,4
    arr[1::2] = -1                 # каждый второй (с индекса 1)
    return arr.tolist()


def cap_above(values: list[float], limit: float) -> list[float]:
    arr = np.array(values).copy()
    mask = arr > limit             # логическая маска
    arr[mask] = limit              # замена по маске
    return arr.tolist()


def celsius_to_fahrenheit(values: list[float]) -> list[float]:
    arr = np.array(values)
    return (arr * 9 / 5 + 32).tolist()  # операция сразу ко всему массиву
