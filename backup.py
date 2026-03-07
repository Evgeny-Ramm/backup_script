#!/usr/bin/env python3
import argparse
import sys
import os
from datetime import datetime

def main():
    parser = argparse.ArgumentParser(
        description="Создание резервной копии файлов и папок."
    )
    # Позиционные аргументы: один или несколько источников
    parser.add_argument(
        'sources',
        nargs='+',
        help='Файлы и/или папки для резервного копирования'
    )
    # Опция --dest
    parser.add_argument(
        '-d', '--dest',
        default='~/Backups',
        help='Папка для сохранения архива (по умолчанию ~/Backups)'
    )
    # Опция --name
    parser.add_argument(
        '-n', '--name',
        default='backup',
        help='Базовое имя архива (без даты и расширения)'
    )
    # Опция --format
    parser.add_argument(
        '-f', '--format',
        choices=['zip', 'tar'],
        default='zip',
        help='Формат архива: zip или tar (по умолчанию zip)'
    )
    # Опция --verbose
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Подробный вывод процесса'
    )

    args = parser.parse_args()

    # Отладочный вывод (можно будет убрать позже)
    print("Источники:", args.sources)
    print("Папка назначения (как введено):", args.dest)

    # 1. Проверяем, какие источники существуют
    valid_sources = []
    for src in args.sources:
        if os.path.exists(src):
            valid_sources.append(src)
        else:
            print(f"Предупреждение: источник {src} не существует, пропускаем.")

    if not valid_sources:
        print("Ошибка: нет ни одного существующего источника для бэкапа.")
        sys.exit(1)

    # 2. Создаём папку назначения
    dest_dir = os.path.expanduser(args.dest)   # заменяет ~ на /home/ev
    os.makedirs(dest_dir, exist_ok=True)
    print(f"Папка назначения (полный путь): {dest_dir}")

    # 3. Генерируем имя архива с датой
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d_%H-%M-%S")
    base_name = args.name
    extension = 'zip' if args.format == 'zip' else 'tar'
    archive_filename = f"{base_name}_{date_str}.{extension}"
    archive_path = os.path.join(dest_dir, archive_filename)

    print(f"Имя архива: {archive_filename}")
    print(f"Полный путь к архиву: {archive_path}")

    # 4. Здесь будет создание архива (следующий шаг)
    # Пока только выводим информацию
    print("Базовое имя архива:", args.name)
    print("Формат:", args.format)
    print("Подробный режим:", args.verbose)

if __name__ == "__main__":
    main()
