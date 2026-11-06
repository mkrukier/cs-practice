def csv_to_records(text: str) -> list[dict]:
    # Разбирает CSV с заголовком в список словарей.
    if not text.strip():
        return []
        
    lines = text.strip().split('\n')
    headers = [h.strip() for h in lines[0].split(',')]
    
    records = []
    for line in lines[1:]:
        if not line.strip():
            continue
        values = [v.strip() for v in line.split(',')]
        record = dict(zip(headers, values))
        records.append(record)
        
    return records


def parse_settings(lines: list[str]) -> dict:
    # Простой YAML -> словарь.
    result = {}
    current_key = None
    
    for line in lines:
        # Отрезаем всё после # (комментарии)
        if '#' in line:
            line = line.split('#')[0]
            
        line = line.strip()
        if not line:
            continue
            
        # Обработка элементов списка
        if line.startswith('- '):
            item_str = line[2:].strip()
            if current_key is not None:
                result[current_key].append(_parse_yaml_value(item_str))
                
        # Обработка ключей
        elif ':' in line:
            key, val = line.split(':', 1)
            key = key.strip()
            val = val.strip()
            
            if not val:
                current_key = key
                result[current_key] = []
            else:
                current_key = None
                result[key] = _parse_yaml_value(val)
                
    return result


def _parse_yaml_value(val: str):
    # Приводим типы строго по правилам из задания.
    val_lower = val.lower()
    
    if val_lower in ('true', 'yes'):
        return True
    if val_lower in ('false', 'no'):
        return False
        
    # Проверяем на целое число
    try:
        return int(val)
    except ValueError:
        pass
        
    # Проверяем на дробное число (только с точкой, как в задании)
    try:
        return float(val)
    except ValueError:
        pass
        
    # Всё остальное остается строкой (включая "3,5")
    return val


def merge_by_key(rows: list[dict], extra: dict, key: str = "id") -> list[dict]:
    # Дополняет записи сведениями из JSON-справочника по ключу.
    result = []
    
    for row in rows:
        new_row = row.copy()
        key_val = row.get(key)
        
        if key_val in extra:
            extra_data = extra[key_val]
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
