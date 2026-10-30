def count_by_extension(paths):
    counts = {}
    for path in paths:
        if "." in path and path.rfind(".") > 0:
            ext = path.rsplit(".", 1)[-1].lower()
        else:
            ext = ""

        counts[ext] = counts.get(ext, 0) + 1

    return counts


def deepest_path(paths):
    if not paths:
        return ""

    sorted_paths = sorted(
        paths,
        key=lambda x: (-x.count('/'), x)
    )

    return sorted_paths[0]


def human_size(n_bytes):
    if n_bytes < 1024:
        return f"{n_bytes} Б"

    units = ["КБ", "МБ", "ГБ", "ТБ"]
    size = n_bytes
    unit_index = -1

    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1

    return f"{size:.1f} {units[unit_index]}"


if name == "main":
    paths_test = ["docs/report.PDF", "notes.txt", "docs/img/logo.png", "Makefile"]

    print(count_by_extension(paths_test))

    print(deepest_path(paths_test))

    print(human_size(900))
    print(human_size(1536))
    print(human_size(5 * 1024 * 1024))
