import os
import shutil
import datetime

def backup_file(file_path):
    if not os.path.exists(file_path):
        return False, f"Файл {file_path} не существует!"
    
    if not os.path.isfile(file_path):
        return False, f"{file_path} - это не файл!"
    
    try:
        date_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{file_path}.backup.{date_str}"
        shutil.copy2(file_path, backup_name)
        return True, f"Создана резервная копия: {backup_name}"
    except Exception as e:
        return False, f"Ошибка при создании копии: {str(e)}"

def backup_folder(folder_path, backup_base="backups"):
    if not os.path.exists(folder_path):
        return False, f"Папка {folder_path} не существует!"
    
    if not os.path.isdir(folder_path):
        return False, f"{folder_path} - это не папка!"
    
    try:
        os.makedirs(backup_base, exist_ok=True)
        folder_name = os.path.basename(folder_path)
        date_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{folder_name}_backup_{date_str}"
        backup_path = os.path.join(backup_base, backup_name)
        
        if os.path.exists(backup_path):
            shutil.rmtree(backup_path)
        
        shutil.copytree(folder_path, backup_path)
        return True, f"Создана резервная копия папки: {backup_path}"
    except Exception as e:
        return False, f"Ошибка при создании копии папки: {str(e)}"

def backup_by_extension(folder, extension=".txt", backup_folder="auto_backups"):
    if not os.path.exists(folder):
        return False, f"Папка {folder} не существует!"
    
    if not os.path.isdir(folder):
        return False, f"{folder} - это не папка!"
    
    try:
        os.makedirs(backup_folder, exist_ok=True)
        copied_count = 0
        
        for filename in os.listdir(folder):
            if filename.endswith(extension):
                file_path = os.path.join(folder, filename)
                if os.path.isfile(file_path):
                    backup_path = os.path.join(backup_folder, filename)
                    shutil.copy2(file_path, backup_path)
                    copied_count += 1
        
        return True, f"Скопировано файлов: {copied_count}"
    except Exception as e:
        return False, f"Ошибка при копировании: {str(e)}"

def list_backups(backup_folder="backups"):
    if not os.path.exists(backup_folder):
        return []
    
    backups = []
    for item in os.listdir(backup_folder):
        item_path = os.path.join(backup_folder, item)
        if os.path.isdir(item_path):
            size = sum(
                os.path.getsize(os.path.join(dirpath, filename))
                for dirpath, dirnames, filenames in os.walk(item_path)
                for filename in filenames
            )
            mtime = os.path.getmtime(item_path)
            date_str = datetime.datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
            backups.append({
                'name': item,
                'path': item_path,
                'type': 'folder',
                'size': size,
                'date': date_str
            })
        elif os.path.isfile(item_path):
            size = os.path.getsize(item_path)
            mtime = os.path.getmtime(item_path)
            date_str = datetime.datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
            backups.append({
                'name': item,
                'path': item_path,
                'type': 'file',
                'size': size,
                'date': date_str
            })
    
    return backups

def format_size(size_bytes):
    for unit in ['Б', 'КБ', 'МБ', 'ГБ']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} ТБ"

def run():
    print("\n=== Система резервного копирования ===")
    
    while True:
        print("\nВыберите действие:")
        print("1. Создать резервную копию файла")
        print("2. Создать резервную копию папки")
        print("3. Автоматическое копирование по расширению")
        print("4. Показать список резервных копий")
        print("5. Указать папку для резервных копий")
        print("0. Назад")
        
        выбор = input("\nВыберите действие: ").strip()
        
        if выбор == "1":
            file_path = input("Введите путь к файлу: ").strip()
            if file_path:
                success, message = backup_file(file_path)
                if success:
                    print(f"✅ {message}")
                else:
                    print(f"❌ {message}")
            else:
                print("Путь к файлу не может быть пустым!")
            input("\nНажмите Enter для продолжения...")
            
        elif выбор == "2":
            folder_path = input("Введите путь к папке: ").strip()
            backup_base = input("Введите папку для сохранения (по умолчанию 'backups'): ").strip()
            if not backup_base:
                backup_base = "backups"
            
            if folder_path:
                success, message = backup_folder(folder_path, backup_base)
                if success:
                    print(f"✅ {message}")
                else:
                    print(f"❌ {message}")
            else:
                print("Путь к папке не может быть пустым!")
            input("\nНажмите Enter для продолжения...")
            
        elif выбор == "3":
            folder_path = input("Введите путь к папке: ").strip()
            extension = input("Введите расширение файлов (например .txt): ").strip()
            if not extension:
                extension = ".txt"
            
            backup_folder_name = input("Введите папку для сохранения (по умолчанию 'auto_backups'): ").strip()
            if not backup_folder_name:
                backup_folder_name = "auto_backups"
            
            if folder_path:
                success, message = backup_by_extension(folder_path, extension, backup_folder_name)
                if success:
                    print(f"✅ {message}")
                else:
                    print(f"❌ {message}")
            else:
                print("Путь к папке не может быть пустым!")
            input("\nНажмите Enter для продолжения...")
            
        elif выбор == "4":
            backup_folder_name = input("Введите папку с резервными копиями (по умолчанию 'backups'): ").strip()
            if not backup_folder_name:
                backup_folder_name = "backups"
            
            backups = list_backups(backup_folder_name)
            if backups:
                print(f"\n=== Резервные копии в '{backup_folder_name}' ===")
                print(f"{'Тип':<10} {'Имя':<40} {'Размер':<15} {'Дата':<20}")
                print("-" * 90)
                for backup in backups:
                    print(f"{backup['type']:<10} {backup['name']:<40} {format_size(backup['size']):<15} {backup['date']:<20}")
            else:
                print(f"Резервные копии в папке '{backup_folder_name}' не найдены")
            input("\nНажмите Enter для продолжения...")
            
        elif выбор == "5":
            backup_folder_name = input("Введите путь к папке для резервных копий: ").strip()
            if backup_folder_name:
                try:
                    os.makedirs(backup_folder_name, exist_ok=True)
                    print(f"✅ Папка '{backup_folder_name}' готова для резервных копий")
                except Exception as e:
                    print(f"❌ Ошибка при создании папки: {str(e)}")
            else:
                print("Путь к папке не может быть пустым!")
            input("\nНажмите Enter для продолжения...")
            
        elif выбор == "0":
            break
        else:
            print("Неверный выбор!")

