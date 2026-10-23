import sys
import logstats

def main():
    # 1. Читаем имя файла из первой строки ввода
    try:
        filename = input().strip()
    except EOFError:
        return 

    # 2. Первый проход: считаем уровни
    with open(filename, 'r', encoding='utf-8') as f:
        counts = logstats.count_levels(f)

    # 3. Второй проход: ищем частые ошибки
    with open(filename, 'r', encoding='utf-8') as f:
        top_errs = logstats.top_errors(f, 3)

    # 4. Считаем общую статистику для вывода
    total_lines = sum(counts.values())
    error_count = counts.get("ERROR", 0)
    broken_count = counts.get("BROKEN", 0)

    # 5. Печатаем три числа
    print(total_lines)
    print(error_count)
    print(broken_count)

    # 6. Формируем и записываем отчет
    report_text = logstats.format_report(counts, top_errs)
    
    with open("report.txt", "w", encoding="utf-8") as out_f:
        out_f.write(report_text)

if __name__ == "__main__":
    main()
