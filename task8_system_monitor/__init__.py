import psutil
import time
import os
import platform

def get_cpu_info():
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_count = psutil.cpu_count()
    cpu_freq = psutil.cpu_freq()
    return {
        'percent': cpu_percent,
        'count': cpu_count,
        'freq_current': cpu_freq.current if cpu_freq else None,
        'freq_max': cpu_freq.max if cpu_freq else None
    }

def get_memory_info():
    mem = psutil.virtual_memory()
    return {
        'total': mem.total,
        'available': mem.available,
        'used': mem.used,
        'percent': mem.percent
    }

def get_disk_info():
    disks = []
    partitions = psutil.disk_partitions()
    for partition in partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            disks.append({
                'device': partition.device,
                'mountpoint': partition.mountpoint,
                'fstype': partition.fstype,
                'total': usage.total,
                'used': usage.used,
                'free': usage.free,
                'percent': usage.percent
            })
        except PermissionError:
            continue
    return disks

def get_system_info():
    return {
        'system': platform.system(),
        'release': platform.release(),
        'version': platform.version(),
        'machine': platform.machine(),
        'processor': platform.processor()
    }

def get_all_processes():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return processes

def get_top_processes(by='cpu', count=10):
    processes = get_all_processes()
    if by == 'cpu':
        processes.sort(key=lambda x: x.get('cpu_percent', 0) or 0, reverse=True)
    elif by == 'memory':
        processes.sort(key=lambda x: x.get('memory_percent', 0) or 0, reverse=True)
    return processes[:count]

def find_processes_by_name(name):
    found = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            if name.lower() in proc.info['name'].lower():
                found.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return found

def get_process_details(pid):
    try:
        proc = psutil.Process(pid)
        return {
            'pid': proc.pid,
            'name': proc.name(),
            'status': proc.status(),
            'cpu_percent': proc.cpu_percent(interval=0.1),
            'memory_percent': proc.memory_percent(),
            'memory_info': proc.memory_info()._asdict(),
            'create_time': time.ctime(proc.create_time()),
            'num_threads': proc.num_threads(),
            'exe': proc.exe() if proc.exe() else 'N/A',
            'cwd': proc.cwd() if proc.cwd() else 'N/A'
        }
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return None

def format_bytes(bytes_value):
    for unit in ['Б', 'КБ', 'МБ', 'ГБ', 'ТБ']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f} ПБ"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_system_info():
    system = get_system_info()
    print("\n=== Системная информация ===")
    print(f"ОС: {system['system']} {system['release']}")
    print(f"Версия: {system['version']}")
    print(f"Архитектура: {system['machine']}")
    print(f"Процессор: {system['processor']}")

def display_cpu_info():
    cpu = get_cpu_info()
    print("\n=== CPU ===")
    print(f"Загрузка: {cpu['percent']}%")
    print(f"Ядер: {cpu['count']}")
    if cpu['freq_current']:
        print(f"Частота: {cpu['freq_current']:.2f} МГц")
        if cpu['freq_max']:
            print(f"Макс. частота: {cpu['freq_max']:.2f} МГц")

def display_memory_info():
    mem = get_memory_info()
    print("\n=== Память ===")
    print(f"Всего: {format_bytes(mem['total'])}")
    print(f"Использовано: {format_bytes(mem['used'])} ({mem['percent']}%)")
    print(f"Доступно: {format_bytes(mem['available'])}")

def display_disk_info():
    disks = get_disk_info()
    print("\n=== Диски ===")
    for disk in disks:
        print(f"{disk['device']} ({disk['mountpoint']})")
        print(f"  Тип: {disk['fstype']}")
        print(f"  Всего: {format_bytes(disk['total'])}")
        print(f"  Использовано: {format_bytes(disk['used'])} ({disk['percent']}%)")
        print(f"  Свободно: {format_bytes(disk['free'])}")
        print()

def display_processes(processes, limit=None):
    print(f"\n{'PID':<8} {'Имя':<30} {'CPU %':<10} {'Память %':<12} {'Статус':<10}")
    print("-" * 80)
    for proc in (processes[:limit] if limit else processes):
        pid = proc.get('pid', 'N/A')
        name = proc.get('name', 'N/A')[:28]
        cpu = proc.get('cpu_percent', 0) or 0
        mem = proc.get('memory_percent', 0) or 0
        status = proc.get('status', 'N/A')
        print(f"{pid:<8} {name:<30} {cpu:<10.2f} {mem:<12.2f} {status:<10}")

def realtime_mode():
    print("\n=== Режим реального времени ===")
    print("Нажмите Ctrl+C для выхода")
    try:
        while True:
            clear_screen()
            print("=" * 80)
            print("SystemMonitor Pro - Режим реального времени")
            print("=" * 80)
            
            display_system_info()
            display_cpu_info()
            display_memory_info()
            display_disk_info()
            
            top_cpu = get_top_processes('cpu', 5)
            print("\n=== Топ-5 процессов по CPU ===")
            display_processes(top_cpu)
            
            print("\nОбновление через 2 секунды...")
            time.sleep(2)
    except KeyboardInterrupt:
        print("\nВыход из режима реального времени")

def detail_mode():
    print("\n=== Режим детальной информации ===")
    name = input("Введите имя процесса для поиска: ").strip()
    if not name:
        print("Имя процесса не может быть пустым!")
        return
    
    found = find_processes_by_name(name)
    if not found:
        print(f"Процессы с именем '{name}' не найдены")
        return
    
    print(f"\nНайдено процессов: {len(found)}")
    display_processes(found)
    
    try:
        pid = int(input("\nВведите PID процесса для детальной информации: "))
        details = get_process_details(pid)
        if details:
            print("\n=== Детальная информация о процессе ===")
            print(f"PID: {details['pid']}")
            print(f"Имя: {details['name']}")
            print(f"Статус: {details['status']}")
            print(f"CPU: {details['cpu_percent']:.2f}%")
            print(f"Память: {details['memory_percent']:.2f}%")
            print(f"Память (RSS): {format_bytes(details['memory_info']['rss'])}")
            print(f"Память (VMS): {format_bytes(details['memory_info']['vms'])}")
            print(f"Потоков: {details['num_threads']}")
            print(f"Время создания: {details['create_time']}")
            print(f"Исполняемый файл: {details['exe']}")
            print(f"Рабочая директория: {details['cwd']}")
        else:
            print("Процесс не найден или нет доступа")
    except ValueError:
        print("Введите корректный PID (число)")

def search_mode():
    print("\n=== Режим поиска ===")
    name = input("Введите имя процесса для поиска: ").strip()
    if not name:
        print("Имя процесса не может быть пустым!")
        return
    
    found = find_processes_by_name(name)
    if found:
        print(f"\nНайдено процессов: {len(found)}")
        display_processes(found)
    else:
        print(f"Процессы с именем '{name}' не найдены")

def run():
    print("\n=== SystemMonitor Pro ===")
    
    while True:
        print("\nВыберите режим работы:")
        print("1. Мониторинг системы (CPU, память, диски)")
        print("2. Режим реального времени (обновление каждые 2 сек)")
        print("3. Топ процессов по CPU")
        print("4. Топ процессов по памяти")
        print("5. Детальная информация о процессе")
        print("6. Поиск процессов по имени")
        print("7. Все процессы")
        print("0. Назад")
        
        выбор = input("\nВыберите действие: ").strip()
        
        if выбор == "1":
            clear_screen()
            display_system_info()
            display_cpu_info()
            display_memory_info()
            display_disk_info()
            input("\nНажмите Enter для продолжения...")
            
        elif выбор == "2":
            realtime_mode()
            
        elif выбор == "3":
            print("\n=== Топ-10 процессов по CPU ===")
            top = get_top_processes('cpu', 10)
            display_processes(top)
            input("\nНажмите Enter для продолжения...")
            
        elif выбор == "4":
            print("\n=== Топ-10 процессов по памяти ===")
            top = get_top_processes('memory', 10)
            display_processes(top)
            input("\nНажмите Enter для продолжения...")
            
        elif выбор == "5":
            detail_mode()
            input("\nНажмите Enter для продолжения...")
            
        elif выбор == "6":
            search_mode()
            input("\nНажмите Enter для продолжения...")
            
        elif выбор == "7":
            print("\n=== Все процессы ===")
            processes = get_all_processes()
            print(f"Всего процессов: {len(processes)}")
            display_processes(processes, limit=50)
            input("\nНажмите Enter для продолжения...")
            
        elif выбор == "0":
            break
        else:
            print("Неверный выбор!")

