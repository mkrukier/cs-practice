def parse_settings(lines: list[str]) -> dict:
    result = {}
    current_key = None
    
    for line in lines:
        # 1. Убираем комментарии (всё после #)
        if '#' in line:
            line = line.split('#')[0]
            
        # 2. Убираем пробелы по краям
        line = line.strip()
        
        # 3. Пропускаем пустые строки (например, если строка была только комментарием)
        if not line:
            continue
            
        # 4. Обработка элементов списка (начинаются с "- ")
        if line.startswith('- '):
            item_str = line[2:].strip()
            if current_key is not None:
                result[current_key].append(_convert_value(item_str))
                
        # 5. Обработка пар "ключ: значение"
        elif ':' in line:
            # Делим ровно по первому двоеточию
            key, val = line.split(':', 1)
            key = key.strip()
            val = val.strip()
            
            if not val:
                # Если значения нет, значит дальше пойдет список
                current_key = key
                result[current_key] = []
            else:
                # Если значение есть, сбрасываем текущий ключ списка
                current_key = None
                result[key] = _convert_value(val)
                
    return result

def _convert_value(val: str):
    # Вспомогательная функция. В задании четко сказано: "3.5 - дробным" (через точку!)
    # Значит "3,5" (через запятую) должно остаться строкой.
    
    # Проверка на булевы значения
    if val.lower() in ('true', 'yes'):
        return True
    if val.lower() in ('false', 'no'):
        return False
        
    # Проверка на целое число
    try:
        return int(val)
    except ValueError:
        pass
        
    # Проверка на дробное число (float понимает только точку)
    try:
        return float(val)
    except ValueError:
        pass
        
    # Если ничего не подошло — это строка
    return val
