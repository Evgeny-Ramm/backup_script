import argparse
import sys
import os

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

    # Пока просто выведем полученные аргументы, чтобы убедиться, что всё работает
    print("Источники:", args.sources)
    print("Папка назначения:", args.dest)
    print("Имя архива:", args.name)
    print("Формат:", args.format)
    print("Подробный режим:", args.verbose)
        # Проверка существования источников
    valid_sources = []
    for src in args.sources:
        if os.path.exists(src):
            valid_sources.append(src)
        else:
            print(f"Предупреждение: источник {src} не существует, пропускаем.")

    if not valid_sources:
        print("Ошибка: нет ни одного существующего источника для бэкапа.")
        sys.exit(1)

    # Создание папки назначения
    dest_dir = os.path.expanduser(args.dest)  # заменяет ~ на /home/ev
    os.makedirs(dest_dir, exist_ok=True)
    print(f"Папка назначения: {dest_dir}")
if __name__ == "__main__":
    main()





















