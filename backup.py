import argparse
import sys

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
if __name__ == "__main__":
    main()





















