import task1_calculator
import task2_triangle_area
import task3_cylinder_volume
import task4_text_quest
import task5_todo_list
import task6_budget_calculator
import task7_system_info
import task8_system_monitor
import task9_weather_parser
import task10_html_parser

def main():
    print("=" * 50)
    print("Добро пожаловать в сборник задач!")
    print("=" * 50)
    
    while True:
        print("\nВыберите задачу:")
        print("1. Калькулятор")
        print("2. Площадь треугольника")
        print("3. Объём цилиндра")
        print("4. Текстовый квест")
        print("5. Список задач")
        print("6. Калькулятор бюджета")
        print("7. Информация о системе")
        print("8. Системный монитор")
        print("9. Парсер погоды")
        print("10. HTML парсер")
        print("0. Выход")
        
        выбор = input("\nВведите номер задачи: ").strip()
        
        if выбор == "1":
            task1_calculator.run()
        elif выбор == "2":
            task2_triangle_area.run()
        elif выбор == "3":
            task3_cylinder_volume.run()
        elif выбор == "4":
            task4_text_quest.run()
        elif выбор == "5":
            task5_todo_list.run()
        elif выбор == "6":
            task6_budget_calculator.run()
        elif выбор == "7":
            task7_system_info.run()
        elif выбор == "8":
            task8_system_monitor.run()
        elif выбор == "9":
            task9_weather_parser.run()
        elif выбор == "10":
            task10_html_parser.run()
        elif выбор == "0":
            print("\nСпасибо за использование программы!")
            print("До свидания!")
            break
        else:
            print("\nНеверный выбор! Пожалуйста, выберите число от 0 до 10.")

if __name__ == "__main__":
    main()

