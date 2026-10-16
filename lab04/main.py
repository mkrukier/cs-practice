import sys
from stats import average_by_city, read_valid, warmest_city

def main():
    # Читаем весь ввод из stdin
    lines = sys.stdin.read().splitlines()
    
    # Получаем список валидных записей
    records = read_valid(lines)
    
    # 1. Сколько записей разобрано
    valid_count = len(records)
    print(valid_count)
    
    # 2. Сколько строк пропущено из-за ошибок
    # Всего строк минус валидные минус пустые строки
    total_lines = len(lines)
    empty_lines_count = sum(1 for line in lines if not line.strip())
    errors_count = total_lines - valid_count - empty_lines_count
    print(errors_count)
    
    # 3. Средняя температура самого тёплого города
    if valid_count > 0:
        best_city = warmest_city(records)
        avg_temps = average_by_city(records)
        # Форматируем с одним знаком после точки
        print(f"{avg_temps[best_city]:.1f}")

if __name__ == "__main__":
    main()
