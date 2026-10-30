def count_by_extension(paths: list[str]) -> dict[str, int]:
    result = {}
    for path in paths:
        # Отделяем имя файла от пути к папке (если папка есть)
        filename = path.split('/')[-1]
        
        # Находим индекс последней точки
        last_dot_index = filename.rfind('.')
        
        if last_dot_index != -1:
            # Берем всё, что идет после последней точки, и приводим к нижнему регистру
            ext = filename[last_dot_index + 1:].lower()
        else:
            # Если точки нет вообще (например, Makefile)
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
