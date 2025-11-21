import platform
import os
import sys

def run():
    print("\n=== Информация о системе ===")
    
    система = platform.system()
    версия_python = sys.version.split()[0]
    
    print(f"\nОперационная система: {система}")
    print(f"Версия Python: {версия_python}")
    
    if система == "Linux":
        print("\nПРЕДУПРЕЖДЕНИЕ: Вы используете Linux!")
    
    версия_major = int(версия_python.split('.')[0])
    версия_minor = int(версия_python.split('.')[1])
    
    if версия_major < 3 or (версия_major == 3 and версия_minor < 8):
        print("ПРЕДУПРЕЖДЕНИЕ: Используется старая версия Python!")
    
    print("\n=== Выберите информацию для просмотра ===")
    print("1. Информация о процессоре")
    print("2. Информация об операционной системе")
    print("3. Информация о Python")
    print("4. Полная информация")
    print("5. Назад")
    
    выбор = input("\nВыберите действие: ").strip()
    
    if выбор == "1":
        print("\n--- Процессор ---")
        print(f"Архитектура: {platform.machine()}")
        print(f"Процессор: {platform.processor()}")
        
    elif выбор == "2":
        print("\n--- Операционная система ---")
        print(f"Система: {platform.system()}")
        print(f"Релиз: {platform.release()}")
        print(f"Версия: {platform.version()}")
        print(f"Платформа: {platform.platform()}")
        
    elif выбор == "3":
        print("\n--- Python ---")
        print(f"Версия: {sys.version}")
        print(f"Путь к исполняемому файлу: {sys.executable}")
        print(f"Платформа: {sys.platform}")
        
    elif выбор == "4":
        print("\n--- Процессор ---")
        print(f"Архитектура: {platform.machine()}")
        print(f"Процессор: {platform.processor()}")
        
        print("\n--- Операционная система ---")
        print(f"Система: {platform.system()}")
        print(f"Релиз: {platform.release()}")
        print(f"Версия: {platform.version()}")
        print(f"Платформа: {platform.platform()}")
        
        print("\n--- Python ---")
        print(f"Версия: {sys.version}")
        print(f"Путь к исполняемому файлу: {sys.executable}")
        print(f"Платформа: {sys.platform}")
        
    elif выбор == "5":
        return
    else:
        print("Неверный выбор!")

