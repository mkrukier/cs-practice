def parse_event(line):
    # Убираем пробелы и переносы строк по краям
    line = line.strip()
    if not line:
        raise ValueError("Пустая строка")

    # Делим строку максимум на 3 части (время, уровень, сообщение)
    parts = line.split(maxsplit=2)
    
    # Если частей меньше 3, значит строка битая
    if len(parts) < 3:
        raise ValueError("Неверный формат строки")
    
    time_str = parts[0]
    # Уровень переводим в верхний регистр на случай, если он написан строчными
    level = parts[1].upper()
    message = parts[2]
    
    # Проверяем, что уровень входит в список разрешенных
    valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR"}
    if level not in valid_levels:
        raise ValueError("Неизвестный уровень лога")
        
    # Возвращаем готовый словарь
    return {
        "time": time_str,
        "level": level,
        "message": message
    }

def count_levels(lines):
    # Создаем пустой словарь для подсчета
    counts = {}
    
    for line in lines:
        try:
            # Пытаемся распарсить строку
            event = parse_event(line)
            level = event["level"]
            # Если уровень уже есть в словаре, прибавляем 1, если нет — начинаем с 1
            counts[level] = counts.get(level, 0) + 1
        except ValueError:
            # Если словили ошибку, значит строка битая, считаем её в BROKEN
            counts["BROKEN"] = counts.get("BROKEN", 0) + 1
            
    return counts

def top_errors(lines, n):
    # Словарь для подсчета частоты сообщений об ошибках
    error_counts = {}
    
    for line in lines:
        try:
            event = parse_event(line)
            if event["level"] == "ERROR":
                msg = event["message"]
                error_counts[msg] = error_counts.get(msg, 0) + 1
        except ValueError:
            # Битую строку просто пропускаем
            pass

    # Превращаем словарь в список пар вида [[сообщение, количество], ...]
    pairs = [[msg, count] for msg, count in error_counts.items()]
    
    # Сортируем: сначала по количеству (по убыванию, поэтому -x[1]), 
    # при равенстве — по алфавиту (x[0])
    pairs.sort(key=lambda x: (-x[1], x[0]))
    
    # Возвращаем первые n элементов
    return pairs[:n]

def format_report(counts, errors):
    # Начинаем формировать список строк для отчета
    report_lines = ["отчёт по журналу", ""]
    
    # Выводим уровни в алфавитном порядке
    for level in sorted(counts.keys()):
        report_lines.append(f"{level}: {counts[level]}")
        
    # Добавляем блок с ошибками
    report_lines.append("")
    report_lines.append("частые ошибки:")
    for msg, count in errors:
        report_lines.append(f"- {msg} — {count}")
        
    # В конце текста должен быть перевод строки
    report_lines.append("")
    
    # Склеиваем список строк в одну большую строку через символ переноса
    return "\n".join(report_lines)
