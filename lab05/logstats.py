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
    counts = {}
    for line in lines:
        # Пропускаем пустые строки и строки из одних пробелов
        if not line.strip():
            continue
            
        try:
            event = parse_event(line)
            level = event["level"]
            counts[level] = counts.get(level, 0) + 1
        except ValueError:
            counts["BROKEN"] = counts.get("BROKEN", 0) + 1
            
    return counts

def top_errors(lines, n):
    # Словарь для подсчета частоты сообщений об ошибках
    error_counts = {}
    for line in lines:
        # Тоже пропускаем пустые строки
        if not line.strip():
            continue
          
        try:
            event = parse_event(line)
            if event["level"] == "ERROR":
                msg = event["message"]
                error_counts[msg] = error_counts.get(msg, 0) + 1
        except ValueError:
            pass

    pairs = [[msg, count] for msg, count in error_counts.items()]
    pairs.sort(key=lambda x: (-x[1], x[0]))
    return pairs[:n]
    
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
    # Начинаем с заголовка
    text = "отчёт по журналу\n\n"
    
    # Выводим уровни по алфавиту
    for level in sorted(counts.keys()):
        text += f"{level}: {counts[level]}\n"
        
    # Добавляем блок с ошибками
    text += "\nчастые ошибки:\n"
    for msg, count in errors:
        text += f"- {msg} — {count}\n"
        
    return text
