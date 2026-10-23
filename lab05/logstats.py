def parse_event(line):
   
    #Превращает строку лога в словарь.
    #Формат: "время уровень сообщение"
    
    # Убираем лишние пробелы по краям и пустые строки
    line = line.strip()
    if not line:
        raise ValueError("Пустая строка")

    # Разделяем строку максимум на 3 части (split с параметром maxsplit)
    # Это важно, так как сообщение само может содержать пробелы
    parts = line.split(maxsplit=2)
    
    # Если частей меньше 3, значит строка битая (нет уровня или сообщения)
    if len(parts) < 3:
        raise ValueError("Неверный формат строки")
    
    # Достаем части
    time_str = parts[0]
    level = parts[1].upper() # Приводим к верхнему регистру на всякий случай
    message = parts[2]
    
    # Проверяем, что уровень валидный (по условию задачи)
    valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR"}
    if level not in valid_levels:
        raise ValueError("Неизвестный уровень лога")
        
    return {
        "time": time_str,
        "level": level,
        "message": message
    }

def count_levels(lines):
    
    #Считает количество строк каждого уровня.
    #Испорченные строки идут в ключ BROKEN.

   counts = {} # Начинаем с пустого словаря!
    
    for line in lines:
        try:
            event = parse_event(line)
            level = event["level"]
            # Если уровень встречается впервые, создаем его с нулем и прибавляем 1
            counts[level] = counts.get(level, 0) + 1
        except ValueError:
            # Если строка испорчена, считаем её в BROKEN
            counts["BROKEN"] = counts.get("BROKEN", 0) + 1
            
    return counts


def top_errors(lines, n):
    
    #Возвращает n самых частых сообщений уровня ERROR.
    #Формат: список пар [сообщение, количество].
    #При равенстве частоты — сортировка по алфавиту.
    
    error_counts = {}
    
    for line in lines:
        try:
            event = parse_event(line)
            if event["level"] == "ERROR":
                msg = event["message"]
                # Считаем частоту сообщений
                error_counts[msg] = error_counts.get(msg, 0) + 1
        except ValueError:
            # Битую строку просто пропускаем (или можно поспорить, но ТЗ не требует их тут учитывать)
            pass

    # Превращаем словарь в список пар: [[сообщение, кол-во], ...]
    pairs = [[msg, count] for msg, count in error_counts.items()]
    
    # Сортируем: сначала по количеству (по убыванию: reverse=True), 
    # затем по алфавиту (по возрастанию, поэтому для первой части ставим минус)
    pairs.sort(key=lambda x: (-x[1], x[0]))
    
    # Возвращаем первые n элементов
    return pairs[:n]

def format_report(counts, errors):
    
    #Формирует текстовый отчет по готовым подсчетам.
    
    # Начинаем с заголовка
    report_lines = ["отчёт по журналу", ""]
    
    # Уровни должны идти по алфавиту
    # Берем ключи из словаря, сортируем их и выводим
    for level in sorted(counts.keys()):
        report_lines.append(f"{level}: {counts[level]}")
        
    # Добавляем блок с частыми ошибками
    report_lines.append("")
    report_lines.append("частые ошибки:")
    for msg, count in errors:
        report_lines.append(f"- {msg} — {count}")
        
    report_lines.append("") # В конце текста перевод строки (пустая строка)
    
    return "\n".join(report_lines)
