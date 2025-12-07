import requests

def get_weather(city, format_type='full'):
    try:
        if format_type == 'short':
            url = f"https://wttr.in/{city}?format=3"
        elif format_type == 'minimal':
            url = f"https://wttr.in/{city}?format=1"
        else:
            url = f"https://wttr.in/{city}?lang=ru"
        
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            return response.text
        else:
            return None
            
    except requests.exceptions.Timeout:
        return "Ошибка: Превышено время ожидания. Проверьте интернет-соединение."
    except requests.exceptions.ConnectionError:
        return "Ошибка: Нет подключения к интернету."
    except requests.exceptions.RequestException as e:
        return f"Ошибка при запросе: {str(e)}"
    except Exception as e:
        return f"Неожиданная ошибка: {str(e)}"

def get_weather_multiple_cities(cities):
    results = []
    for city in cities:
        weather = get_weather(city, 'short')
        if weather:
            results.append(f"{city}: {weather}")
        else:
            results.append(f"{city}: Не удалось получить данные")
    return results

def run():
    print("\n=== Парсер погоды ===")
    
    while True:
        print("\nВыберите действие:")
        print("1. Погода для одного города (полный формат)")
        print("2. Погода для одного города (короткий формат)")
        print("3. Погода для одного города (минимальный формат)")
        print("4. Погода для нескольких городов")
        print("5. Погода для города (с выбором формата)")
        print("0. Назад")
        
        выбор = input("\nВыберите действие: ").strip()
        
        if выбор == "1":
            город = input("Введите название города: ").strip()
            if город:
                print("\nЗагрузка данных...")
                погода = get_weather(город, 'full')
                if погода:
                    print(f"\n=== Погода в {город} ===")
                    print(погода)
                else:
                    print(f"Не удалось получить данные о погоде для города {город}")
            else:
                print("Название города не может быть пустым!")
            input("\nНажмите Enter для продолжения...")
            
        elif выбор == "2":
            город = input("Введите название города: ").strip()
            if город:
                print("\nЗагрузка данных...")
                погода = get_weather(город, 'short')
                if погода:
                    print(f"\n=== Погода в {город} ===")
                    print(погода)
                else:
                    print(f"Не удалось получить данные о погоде для города {город}")
            else:
                print("Название города не может быть пустым!")
            input("\nНажмите Enter для продолжения...")
            
        elif выбор == "3":
            город = input("Введите название города: ").strip()
            if город:
                print("\nЗагрузка данных...")
                погода = get_weather(город, 'minimal')
                if погода:
                    print(f"\n=== Погода в {город} ===")
                    print(погода)
                else:
                    print(f"Не удалось получить данные о погоде для города {город}")
            else:
                print("Название города не может быть пустым!")
            input("\nНажмите Enter для продолжения...")
            
        elif выбор == "4":
            города_строка = input("Введите названия городов через запятую: ").strip()
            if города_строка:
                города = [г.strip() for г in города_строка.split(',') if г.strip()]
                if города:
                    print("\nЗагрузка данных...")
                    результаты = get_weather_multiple_cities(города)
                    print("\n=== Погода для нескольких городов ===")
                    for результат in результаты:
                        print(результат)
                else:
                    print("Не указаны города!")
            else:
                print("Введите хотя бы один город!")
            input("\nНажмите Enter для продолжения...")
            
        elif выбор == "5":
            город = input("Введите название города: ").strip()
            if город:
                print("\nВыберите формат:")
                print("1. Полный")
                print("2. Короткий")
                print("3. Минимальный")
                формат_выбор = input("Формат: ").strip()
                
                формат_тип = 'full'
                if формат_выбор == "2":
                    формат_тип = 'short'
                elif формат_выбор == "3":
                    формат_тип = 'minimal'
                
                print("\nЗагрузка данных...")
                погода = get_weather(город, формат_тип)
                if погода:
                    print(f"\n=== Погода в {город} ===")
                    print(погода)
                else:
                    print(f"Не удалось получить данные о погоде для города {город}")
            else:
                print("Название города не может быть пустым!")
            input("\nНажмите Enter для продолжения...")
            
        elif выбор == "0":
            break
        else:
            print("Неверный выбор!")

