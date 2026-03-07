#!/usr/bin/env python3
import os
import sys
import argparse
from datetime import datetime
import zipfile
import tarfile

# ------------------------------------------------------------
# Функция для чтения файла со списком источников
# ------------------------------------------------------------
def read_source_file(file_path):
    """
    Читает файл, возвращает список непустых строк, не начинающихся с '#'.
    """
    sources = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    sources.append(line)
    except FileNotFoundError:
        print(f"Ошибка: файл {file_path} не найден.")
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка при чтении файла {file_path}: {e}")
        sys.exit(1)
    return sources

# ------------------------------------------------------------
# Функция создания архива
# ------------------------------------------------------------
def create_archive(sources, archive_path, archive_format='zip', verbose=False):
    """
    Создаёт архив из переданных источников.
    sources: список путей к файлам/папкам
    archive_path: полный путь к создаваемому архиву
    archive_format: 'zip' или 'tar'
    verbose: если True, выводить добавляемые файлы
    """
    if archive_format == 'zip':
        with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for src in sources:
                src = os.path.abspath(src)
                if os.path.isfile(src):
                    arcname = os.path.basename(src)
                    if verbose:
                        print(f"Добавляю файл: {src} -> {arcname}")
                    zf.write(src, arcname)
                elif os.path.isdir(src):
                    for root, dirs, files in os.walk(src):
                        for file in files:
                            full_path = os.path.join(root, file)
                            # Относительный путь внутри архива: от корня источника
                            rel_path = os.path.relpath(full_path, start=os.path.dirname(src))
                            if verbose:
                                print(f"Добавляю файл: {full_path} -> {rel_path}")
                            zf.write(full_path, rel_path)
    elif archive_format == 'tar':
        with tarfile.open(archive_path, 'w') as tar:
            for src in sources:
                src = os.path.abspath(src)
                if os.path.isfile(src):
                    arcname = os.path.basename(src)
                    if verbose:
                        print(f"Добавляю файл: {src} -> {arcname}")
                    tar.add(src, arcname)
                elif os.path.isdir(src):
                    if verbose:
                        print(f"Добавляю папку: {src}")
                    tar.add(src, arcname=os.path.basename(src))
    else:
        print(f"Неподдерживаемый формат: {archive_format}")
        sys.exit(1)

# ------------------------------------------------------------
# Основная функция
# ------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Создание резервной копии файлов и папок."
    )
    # Теперь sources необязательны (можно указывать через файл)
    parser.add_argument(
        'sources',
        nargs='*',
        default=[],
        help='Файлы и/или папки для резервного копирования (можно комбинировать с --file)'
    )
    parser.add_argument(
        '-d', '--dest',
        default='~/Backups',
        help='Папка для сохранения архива (по умолчанию ~/Backups)'
    )
    parser.add_argument(
        '-n', '--name',
        default='backup',
        help='Базовое имя архива (без даты и расширения)'
    )
    parser.add_argument(
        '-f', '--format',
        choices=['zip', 'tar'],
        default='zip',
        help='Формат архива: zip или tar (по умолчанию zip)'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Подробный вывод процесса'
    )
    parser.add_argument(
        '-l', '--file',
        help='Файл со списком источников (каждый с новой строки)'
    )

    args = parser.parse_args()

    # --------------------------------------------------------
    # 1. Собираем все источники (из командной строки + из файла)
    # --------------------------------------------------------
    all_sources = args.sources[:]  # копируем список из командной строки
    if args.file:
        file_sources = read_source_file(args.file)
        all_sources.extend(file_sources)
        print(f"Добавлено {len(file_sources)} источников из файла {args.file}")

    if not all_sources:
        print("Ошибка: не указано ни одного источника (ни в командной строке, ни в файле).")
        sys.exit(1)

    print("Все источники:", all_sources)

    # --------------------------------------------------------
    # 2. Проверяем, какие источники действительно существуют
    # --------------------------------------------------------
    valid_sources = []
    for src in all_sources:
        src_expanded = os.path.expanduser(src)  # раскрываем ~
        if os.path.exists(src_expanded):
            valid_sources.append(src_expanded)
        else:
            print(f"Предупреждение: источник {src} не существует, пропускаем.")

    if not valid_sources:
        print("Ошибка: нет ни одного существующего источника для бэкапа.")
        sys.exit(1)

    # --------------------------------------------------------
    # 3. Создаём папку назначения (если её нет)
    # --------------------------------------------------------
    dest_dir = os.path.expanduser(args.dest)
    os.makedirs(dest_dir, exist_ok=True)
    print(f"Папка назначения (полный путь): {dest_dir}")

    # --------------------------------------------------------
    # 4. Генерируем имя архива с датой и временем
    # --------------------------------------------------------
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d_%H-%M-%S")
    base_name = args.name
    extension = 'zip' if args.format == 'zip' else 'tar'
    archive_filename = f"{base_name}_{date_str}.{extension}"
    archive_path = os.path.join(dest_dir, archive_filename)

    print(f"Имя архива: {archive_filename}")
    print(f"Полный путь к архиву: {archive_path}")

    # --------------------------------------------------------
    # 5. Создаём архив
    # --------------------------------------------------------
    create_archive(valid_sources, archive_path, args.format, args.verbose)
    print(f"Архив успешно создан: {archive_path}")

if __name__ == "__main__":
    main()
