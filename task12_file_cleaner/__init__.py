import os
import shutil
import time
import datetime

def safe_remove_file(file_path):
    if not os.path.exists(file_path):
        return False, f"Файл не существует: {file_path}"
    
    if not os.path.isfile(file_path):
        return False, f"{file_path} - это не файл!"
    
    try:
        os.remove(file_path)
        return True, f"Файл удален: {file_path}"
    except Exception as e:
        return False, f"Ошибка при удалении: {str(e)}"

def safe_remove_folder(folder_path):
    if not os.path.exists(folder_path):
        return False, f"Папка не существует: {folder_path}"
    
    if not os.path.isdir(folder_path):
        return False, f"{folder_path} - это не папка!"
    
    try:
        shutil.rmtree(folder_path)
        return True, f"Папка удалена: {folder_path}"
    except Exception as e:
        return False, f"Ошибка при удалении: {str(e)}"

def remove_old_files(folder, days=30):
    if not os.path.exists(folder):
        return False, f"Папка не существует: {folder}"
    
    if not os.path.isdir(folder):
        return False, f"{folder} - это не папка!"
    
    try:
        cutoff_time = time.time() - (days * 24 * 60 * 60)
        removed_count = 0
        
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            
            if os.path.isfile(file_path):
                file_time = os.path.getmtime(file_path)
                
                if file_time < cutoff_time:
                    try:
                        os.remove(file_path)
                        removed_count += 1
                    except Exception as e:
                        pass
        
        return True, f"Удалено старых файлов: {removed_count}"
    except Exception as e:
        return False, f"Ошибка при удалении: {str(e)}"

def safe_clean_folder(folder_path):
    if not os.path.exists(folder_path):
        return False, f"Папка не существует: {folder_path}"
    
    if not os.path.isdir(folder_path):
        return False, f"{folder_path} - это не папка!"
    
    try:
        removed_count = 0
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    removed_count += 1
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                    removed_count += 1
            except Exception as e:
                pass
        
        return True, f"Папка очищена. Удалено объектов: {removed_count}"
    except Exception as e:
        return False, f"Ошибка при очистке: {str(e)}"

def move_to_trash(file_path, trash_folder="trash"):
    if not os.path.exists(file_path):
        return False, f"Файл не существует: {file_path}"
    
    try:
        os.makedirs(trash_folder, exist_ok=True)
        filename = os.path.basename(file_path)
        name, ext = os.path.splitext(filename)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        trash_name = f"{name}_{timestamp}{ext}"
        trash_path = os.path.join(trash_folder, trash_name)
        
        shutil.move(file_path, trash_path)
        return True, f"Файл перемещен в корзину: {filename}"
    except Exception as e:
        return False, f"Ошибка перемещения: {str(e)}"

def remove_by_extension(folder, extension):
    if not os.path.exists(folder):
        return False, f"Папка не существует: {folder}"
    
    if not os.path.isdir(folder):
        return False, f"{folder} - это не папка!"
    
    try:
        removed_count = 0
        for filename in os.listdir(folder):
            if filename.endswith(extension):
                file_path = os.path.join(folder, filename)
                if os.path.isfile(file_path):
                    try:
                        os.remove(file_path)
                        removed_count += 1
                    except Exception as e:
                        pass
        
        return True, f"Удалено файлов с расширением {extension}: {removed_count}"
    except Exception as e:
        return False, f"Ошибка при удалении: {str(e)}"

def list_files_in_folder(folder_path):
    if not os.path.exists(folder_path):
        return []
    
    if not os.path.isdir(folder_path):
        return []
    
    files = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            size = os.path.getsize(file_path)
            mtime = os.path.getmtime(file_path)
            date_str = datetime.datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
            files.append({
                'name': filename,
                'path': file_path,
                'size': size,
                'date': date_str
            })
    
    return files

def format_size(size_bytes):
    for unit in ['Б', 'КБ', 'МБ', 'ГБ']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} ТБ"

def run():
    print("\n=== Удаление файлов и очистка папок ===")
    print("⚠️  ВНИМАНИЕ: Удаление файлов необратимо!")
    
    while True:
        print("\nВыберите действие:")
        print("1. Удалить файл")
        print("2. Удалить папку")
        print("3. Удалить старые файлы (по дате)")
        print("4. Очистить папку от содержимого")
        print("5. Переместить файл в корзину")
        print("6. Удалить файлы по расширению")
        print("7. Показать файлы в папке")
        print("0. Назад")
        
        выбор = input("\nВыберите действие: ").strip()
        
        if выбор == "1":
            file_path = input("Введите путь к файлу для удаления: ").strip()
            if file_path:
                confirm = input(f"Вы уверены, что хотите удалить '{file_path}'? (да/нет): ").strip().lower()
                if confirm == "да":
                    success, message = safe_remove_file(file_path)
                    if success:
                        print(f"✅ {message}")
                    else:
                        print(f"❌ {message}")
                else:
                    print("Удаление отменено")
            else:
                print("Путь к файлу не может быть пустым!")
            input("\nНажмите Enter для продолжения...")
            
        elif выбор == "2":
            folder_path = input("Введите путь к папке для удаления: ").strip()
            if folder_path:
                confirm = input(f"Вы уверены, что хотите удалить папку '{folder_path}'? (да/нет): ").strip().lower()
                if confirm == "да":
                    success, message = safe_remove_folder(folder_path)
                    if success:
                        print(f"✅ {message}")
                    else:
                        print(f"❌ {message}")
                else:
                    print("Удаление отменено")
            else:
                print("Путь к папке не может быть пустым!")
            input("\nНажмите Enter для продолжения...")
            
        elif выбор == "3":
            folder_path = input("Введите путь к папке: ").strip()
            try:
                days = int(input("Удалить файлы старше (дней): ").strip())
                if days > 0:
                    success, message = remove_old_files(folder_path, days)
                    if success:
                        print(f"✅ {message}")
                    else:
                        print(f"❌ {message}")
                else:
                    print("Количество дней должно быть положительным числом!")
            except ValueError:
                print("Введите корректное число!")
            input("\nНажмите Enter для продолжения...")
            
        elif выбор == "4":
            folder_path = input("Введите путь к папке для очистки: ").strip()
            if folder_path:
                confirm = input(f"Вы уверены, что хотите очистить папку '{folder_path}'? (да/нет): ").strip().lower()
                if confirm == "да":
                    success, message = safe_clean_folder(folder_path)
                    if success:
                        print(f"✅ {message}")
                    else:
                        print(f"❌ {message}")
                else:
                    print("Очистка отменена")
            else:
                print("Путь к папке не может быть пустым!")
            input("\nНажмите Enter для продолжения...")
            
        elif выбор == "5":
            file_path = input("Введите путь к файлу: ").strip()
            trash_folder = input("Введите папку корзины (по умолчанию 'trash'): ").strip()
            if not trash_folder:
                trash_folder = "trash"
            
            if file_path:
                success, message = move_to_trash(file_path, trash_folder)
                if success:
                    print(f"✅ {message}")
                else:
                    print(f"❌ {message}")
            else:
                print("Путь к файлу не может быть пустым!")
            input("\nНажмите Enter для продолжения...")
            
        elif выбор == "6":
            folder_path = input("Введите путь к папке: ").strip()
            extension = input("Введите расширение файлов для удаления (например .tmp): ").strip()
            if folder_path and extension:
                confirm = input(f"Удалить все файлы с расширением '{extension}' в '{folder_path}'? (да/нет): ").strip().lower()
                if confirm == "да":
                    success, message = remove_by_extension(folder_path, extension)
                    if success:
                        print(f"✅ {message}")
                    else:
                        print(f"❌ {message}")
                else:
                    print("Удаление отменено")
            else:
                print("Путь к папке и расширение не могут быть пустыми!")
            input("\nНажмите Enter для продолжения...")
            
        elif выбор == "7":
            folder_path = input("Введите путь к папке: ").strip()
            if folder_path:
                files = list_files_in_folder(folder_path)
                if files:
                    print(f"\n=== Файлы в папке '{folder_path}' ===")
                    print(f"{'Имя':<40} {'Размер':<15} {'Дата изменения':<20}")
                    print("-" * 80)
                    for file_info in files:
                        print(f"{file_info['name']:<40} {format_size(file_info['size']):<15} {file_info['date']:<20}")
                else:
                    print("Файлы не найдены или папка пуста")
            else:
                print("Путь к папке не может быть пустым!")
            input("\nНажмите Enter для продолжения...")
            
        elif выбор == "0":
            break
        else:
            print("Неверный выбор!")

