def csv_to_records(text: str) -> list[dict]:
    # Разбирает CSV с заголовком в список словарей.
    if not text.strip():
        return []
        
    lines = text.strip().split('\n')
    # Первая строка — это заголовки (ключи)
    headers = [h.strip() for h in lines[0].split(',')]
    
    records = []
    # Идем по остальным строкам
    for line in lines[1:]:
        if not line.strip():
            continue
        values = [v.strip() for v in line.split(',')]
        # Собираем словарь, связывая заголовок и значение
        record = dict(zip(headers, values))
        records.append(record)
        
    return records


def _convert_value(val: str):
    # Вспомогательная функция для приведения типов в YAML.
    if val.lower() in ('true', 'yes'):
        return True
    if val.lower() in ('false', 'no'):
        return False
        
    # Заменяем запятую на точку для корректного парсинга дробных чисел (3,5 -> 3.5)
    # Но делаем это только если запятая одна (чтобы не сломать строки с кучей запятых)
    val_for_num = val.replace(',', '.') if val.count(',') == 1 else val
        
    try:
        # Пробуем преобразовать в целое число (используем оригинал, чтобы '1,5' не стало '15')
        if val.isdigit() or (val.startswith('-') and val[1:].isdigit()):
            return int(val)
            
        # Пробуем преобразовать в число с плавающей точкой
        return float(val_for_num)
    except ValueError:
        pass
        
    # Если ничего не подошло, возвращаем как строку
    return val


def parse_settings(lines: list[str]) -> dict:
    # Простой YAML -> словарь.
    result = {}
    current_key = None
    
    for line in lines:
        # Убираем комментарии (все, что после #)
        # Делаем это до strip(), чтобы не потерять случай, когда # стоит сразу после значения
        if '#' in line:
            line = line.split('#')[0]
            
        # Убираем пробелы по краям
        line = line.strip()
        if not line:
            continue
            
        # Если это элемент списка
        if line.startswith('- '):
            item_str = line[2:].strip()
            # На случай, если перед дефисом не было ключа (защита от падения)
            if current_key is not None:
                result[current_key].append(_convert_value(item_str))
        # Если это пара "ключ: значение" или просто "ключ:"
        elif ':' in line:
            key, val = line.split(':', 1)
            key = key.strip()
            val = val.strip()
            
            if not val:
                # Если после двоеточия пусто, значит дальше будет список
                current_key = key
                result[current_key] = []
            else:
                # Обычная пара ключ-значение
                current_key = None
                result[key] = _convert_value(val)
                
    return result


def merge_by_key(rows: list[dict], extra: dict, key: str = "id") -> list[dict]:
    # Дополняет записи сведениями из JSON-справочника по ключу.
    result = []
    
    for row in rows:
        # Создаем копию записи, чтобы не менять исходный список
        new_row = row.copy()
        
        # Ищем значение ключа в текущей строке
        key_val = row.get(key)
        
        # Если такой ключ есть в справочнике
        if key_val in extra:
            extra_data = extra[key_val]
            
            # Поля самой записи важнее. Поэтому обновляем только то, 
            # чего нет в записи, или перезаписываем справочник данными записи
            for k, v in extra_data.items():
                if k not in new_row:
                    new_row[k] = v
                
        result.append(new_row)
        
    return result


def records_to_json(records: list[dict]) -> str:
    # Список словарей -> JSON: ключи по алфавиту, отступ два пробела.
    def format_val(val):
        if isinstance(val, str):
            return f'"{val}"'
        if isinstance(val, bool):
            return 'true' if val else 'false'
        if val is None:
            return 'null'
        return str(val)

    def serialize(obj, indent_level=0):
        indent = "  " * indent_level
        next_indent = "  " * (indent_level + 1)
        
        if isinstance(obj, dict):
            if not obj:
                return "{}"
            items = []
            # Сортируем ключи по алфавиту
            for k in sorted(obj.keys()):
                val_str = serialize(obj[k], indent_level + 1)
                items.append(f'{next_indent}"{k}": {val_str}')
            return "{\n" + ",\n".join(items) + "\n" + indent + "}"
            
        elif isinstance(obj, list):
            if not obj:
                return "[]"
            items = []
            for item in obj:
                items.append(f'{next_indent}{serialize(item, indent_level + 1)}')
            return "[\n" + ",\n".join(items) + "\n" + indent + "]"
            
        else:
            return format_val(obj)

    return serialize(records)
