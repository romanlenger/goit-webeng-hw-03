import os
import shutil
import sys

from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


def ensure_directory_exists(path):
    """gеревіряє, чи існує директорія і створює її"""
    if not os.path.exists(path):
        os.makedirs(path)


def copy_file(file_path, target_dir):
    """копіює файл до вказаної директорї"""
    if not os.path.isfile(file_path):
        return
    
    extension = Path(file_path).suffix[1:]  # отримуємо розширення файлу без крапки
    if not extension:
        extension = 'no_extension'  # Якщо файл не має розширення
    
    target_dir = os.path.join(target_dir, extension)
    ensure_directory_exists(target_dir)
    
    try:
        shutil.copy(file_path, target_dir)
    except Exception as e:
        print(f"Не вдалося скопіювати {file_path} в {target_dir}: {e}")


def process_directory(source_dir, target_dir, executor):
    """Рекурсивно обробляє директорію, копіюючи файли до цільової директорії"""
    futures = []
    
    for entry in os.scandir(source_dir):
        if entry.is_file():
            futures.append(executor.submit(copy_file, entry.path, target_dir))
        elif entry.is_dir():
            futures.append(executor.submit(process_directory, entry.path, target_dir, executor))
    
    # очікуємо завершення всіх задач
    for future in as_completed(futures):
        future.result()


def main():
    if len(sys.argv) < 2:
        print("Використання: python script.py <source_directory> [target_directory]")
        sys.exit(1)
    
    source_directory = sys.argv[1]
    target_directory = sys.argv[2] if len(sys.argv) > 2 else 'dist'
    
    if not os.path.isdir(source_directory):
        print(f"Джерельна директорія {source_directory} не існує.")
        sys.exit(1)
    
    ensure_directory_exists(target_directory)
    
    with ThreadPoolExecutor() as executor:
        process_directory(source_directory, target_directory, executor)
    
    print(f"Обробка завершена. Файли скопійовано до {target_directory}")


if __name__ == "__main__":
    main()
