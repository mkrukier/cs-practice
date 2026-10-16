def parse_record(line: str) -> dict:
    """
    Разбирает строку 'город;температура;дата' в словарь.
    Вызывает ValueError при неверном формате.
    """
    parts = line.split(";")
    
    if len(parts) != 3:
        raise ValueError(f"Ожидалось 3 поля, получено {len(parts)}")
    
    city, temp_str, date = parts
    
    # Убираем пробелы у города и даты
    city = city.strip()
    date = date.strip()
    
    # Проверка на пустые поля
    if not city or not date:
        raise ValueError("Город или дата не могут быть пустыми")
    
    try:
        # Убираем пробелы, заменяем запятую на точку и преобразуем в число
        temp_clean = temp_str.strip().replace(',', '.')
        temperature = float(temp_clean)
    except ValueError:
        raise ValueError(f"Температура '{temp_str}' не является числом")
        
    return {
        "city": city,
        "temperature": temperature,
        "date": date
    }

def read_valid(lines: list) -> list:
    """
    Читает список строк, игнорирует некорректные (мусор, пустые строки).
    """
    valid_records = []
    for line in lines:
        try:
            record = parse_record(line)
            valid_records.append(record)
        except (ValueError, IndexError):
            # Пропускаем "мусор" и пустые строки
            continue
    return valid_records


def average_by_city(records: list) -> dict:
    """
    Считает среднюю температуру по каждому городу.
    Возвращает словарь вида {"Азов": 24.5, "Таганрог": 30.0}
    """
    if not records:
        return {}
        
    city_sums = {}
    city_counts = {}
    
    for rec in records:
        city = rec["city"]
        # ИСПРАВЛЕНИЕ 3: используем правильный ключ "temperature"
        temp = rec["temperature"] 
        
        if city not in city_sums:
            city_sums[city] = 0.0
            city_counts[city] = 0
            
        city_sums[city] += temp
        city_counts[city] += 1
        
    result = {}
    for city in city_sums:
        result[city] = city_sums[city] / city_counts[city]
        
    return result


def warmest_city(records: list[dict]) -> str:
    """
    Возвращает город с наибольшей средней температурой.
    При равенстве — первый по алфавиту.
    """
    avg_temps = average_by_city(records)
    
    if not avg_temps:
        return ""
        
    # Сортируем: сначала по температуре (по убыванию), 
    # при равенстве — по названию города (по возрастанию)
    sorted_cities = sorted(
        avg_temps.items(), 
        key=lambda item: (-item[1], item[0])
    )
    
    return sorted_cities[0][0]
