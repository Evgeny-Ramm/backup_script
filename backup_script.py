#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# backup.py
# Создание бэкапа с цветным выводом и поддержкой .tar.gz.

import os
import shutil
import tarfile
import zipfile
import argparse
from datetime import datetime
from colorama import init, Fore, Style

init(autoreset=True)

def create_backup(sources, dest_dir, name="backup", fmt="zip", compress_level=6):
    os.makedirs(dest_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    archive_name = f"{name}_{timestamp}.{fmt}"

    if fmt == "zip":
        archive_path = os.path.join(dest_dir, archive_name)
        with zipfile.ZipFile(archive_path, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=compress_level) as zf:
            for src in sources:
                src = os.path.abspath(src)
                if os.path.isfile(src):
                    zf.write(src, os.path.basename(src))
                elif os.path.isdir(src):
                    for root, _, files in os.walk(src):
                        for file in files:
                            full_path = os.path.join(root, file)
                            arcname = os.path.relpath(full_path, start=os.path.dirname(src))
                            zf.write(full_path, arcname)
    elif fmt == "tar.gz":
        archive_path = os.path.join(dest_dir, archive_name)
        with tarfile.open(archive_path, 'w:gz', compresslevel=compress_level) as tar:
            for src in sources:
                src = os.path.abspath(src)
                tar.add(src, arcname=os.path.basename(src))

    print(f"{Fore.GREEN}Бэкап создан: {archive_path}{Style.RESET_ALL}")
    return archive_path

def main():
    parser = argparse.ArgumentParser(description="создание бэкапа")
    parser.add_argument("sources", nargs="+", help="файлы/папки для бэкапа")
    parser.add_argument("-d", "--dest", default="~/Backups", help="папка назначения")
    parser.add_argument("-n", "--name", default="backup", help="имя бэкапа")
    parser.add_argument("-f", "--format", choices=["zip", "tar.gz"], default="zip", help="формат")
    parser.add_argument("--compress-level", type=int, choices=range(1, 10), default=6, help="уровень сжатия (1-9)")
    args = parser.parse_args()

    dest_dir = os.path.expanduser(args.dest)
    valid_sources = []
    for src in args.sources:
        src_exp = os.path.expanduser(src)
        if os.path.exists(src_exp):
            valid_sources.append(src_exp)
        else:
            print(f"{Fore.RED}Предупреждение: {src} не существует{Style.RESET_ALL}")

    if not valid_sources:
        print("Ошибка: нет источников для бэкапа")
        return

    create_backup(valid_sources, dest_dir, args.name, args.format, args.compress_level)

if __name__ == "__main__":
    main()
