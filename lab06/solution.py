def count_by_extension(paths: list[str]) -> dict[str, int]:
    result = {}
    for path in paths:
        # Отделяем имя файла от пути к папке (если папка есть)
        filename = path.split('/')[-1]
        
        # Если в имени файла есть точка, берем всё, что после ПЕРВОЙ точки
        if '.' in filename:
            # split('.', 1) разбивает строку только по первой точке
            ext = filename.split('.', 1)[-1].lower()
        else:
            ext = ""
            
        result[ext] = result.get(ext, 0) + 1
    return result

def deepest_path(paths: list[str]) -> str:
    if not paths:
        return ""
    return max(sorted(paths), key=lambda p: p.count('/'))

def human_size(n_bytes: int) -> str:
    if n_bytes < 1024:
        return f"{n_bytes} Б"
    units = ["КБ", "МБ", "ГБ", "ТБ"]
    size = float(n_bytes)
    for unit in units:
        size /= 1024.0
        if size < 1024.0:
            return f"{size:.1f} {unit}"
    return f"{size:.1f} ТБ"
