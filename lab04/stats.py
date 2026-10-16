import sys

def parse_record(line: str) -> dict:
    """
    Разбирает строку 'город;температура;дата' в словарь.
    Вызывает ValueError при неверном формате.
    """
    parts = line.split(";")
    
    # Проверка 1: полей ровно три
    if len(parts) != 3:
        raise ValueError(f"Ожидалось 3 поля, получено {len(parts)}")
    
    city, temp_str, date = parts
    
    # Проверка 2: город и дата не пустые
    if not city.strip() or not date.strip():
        raise ValueError("Город или дата не могут быть пустыми")
    
    # Проверка 3: температура — число
    try:
        temp = float(temp_str)
    except ValueError:
        # Перехватываем ошибку float и возбуждаем свою с понятным сообщением
        raise ValueError(f"Температура '{temp_str}' не является числом")
        
    return {
        "city": city.strip(),
        "temp": temp,
        "date": date.strip()
    }

def read_valid(lines: list[str]) -> list[dict]:
    """
    Разбирает строки журнала, пропуская пустые и негодные строки.
    """
    records = []
    for line in lines:
        # Пропускаем пустые строки молча
        if not line.strip():
            continue
        
        try:
            record = parse_record(line)
            records.append(record)
        except ValueError:
            # Пропускаем негодные строки (ошибки формата)
            continue
            
    return records

def average_by_city(records: list[dict]) -> dict:
    """
    Считает среднюю температуру по каждому городу, округляя до десятых.
    """
    total = {}
    count = {}
    
    for rec in records:
        city = rec["city"]
        temp = rec["temp"]
        
        total[city] = total.get(city, 0.0) + temp
        count[city] = count.get(city, 0) + 1
        
    result = {}
    for city in total:
        # Округляем до десятых (1 знак после запятой)
        result[city] = round(total[city] / count[city], 1)
        
    return result

def warmest_city(records: list[dict]) -> str:
    """
    Возвращает город с наибольшей средней температурой.
    При равенстве — первый по алфавиту.
    """
    avg_temps = average_by_city(records)
    
    if not avg_temps:
        return ""
        
    # Сортируем города: сначала по температуре (по убыванию), потом по имени (по возрастанию)
    # Используем lambda для сортировки
    sorted_cities = sorted(
        avg_temps.items(), 
        key=lambda item: (-item[1], item[0])
    )
    
    return sorted_cities[0][0]
