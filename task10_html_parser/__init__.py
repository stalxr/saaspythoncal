import requests
from bs4 import BeautifulSoup

def load_page(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup, None
        else:
            return None, f"Ошибка: статус код {response.status_code}"
    except requests.exceptions.Timeout:
        return None, "Ошибка: Превышено время ожидания. Проверьте интернет-соединение."
    except requests.exceptions.ConnectionError:
        return None, "Ошибка: Нет подключения к интернету."
    except requests.exceptions.InvalidURL:
        return None, "Ошибка: Неверный URL адрес."
    except Exception as e:
        return None, f"Ошибка при загрузке страницы: {str(e)}"

def get_page_title(soup):
    try:
        title = soup.find('title')
        if title:
            return title.text.strip()
        return "Заголовок не найден"
    except Exception as e:
        return f"Ошибка: {str(e)}"

def get_all_headings(soup, level=None):
    try:
        if level:
            headings = soup.find_all(f'h{level}')
        else:
            headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        
        result = []
        for heading in headings:
            result.append({
                'tag': heading.name,
                'text': heading.text.strip()
            })
        return result
    except Exception as e:
        return []

def get_all_links(soup):
    try:
        links = soup.find_all('a', href=True)
        result = []
        for link in links:
            text = link.text.strip() if link.text else "Без текста"
            href = link['href']
            result.append({
                'text': text,
                'url': href
            })
        return result
    except Exception as e:
        return []

def find_elements_by_tag(soup, tag):
    try:
        elements = soup.find_all(tag)
        result = []
        for elem in elements:
            text = elem.text.strip()[:100] if elem.text else "Без текста"
            result.append({
                'tag': tag,
                'text': text
            })
        return result
    except Exception as e:
        return []

def find_elements_by_class(soup, class_name):
    try:
        elements = soup.find_all(class_=class_name)
        result = []
        for elem in elements:
            text = elem.text.strip()[:100] if elem.text else "Без текста"
            result.append({
                'tag': elem.name,
                'text': text
            })
        return result
    except Exception as e:
        return []

def get_all_images(soup):
    try:
        images = soup.find_all('img', src=True)
        result = []
        for img in images:
            src = img['src']
            alt = img.get('alt', 'Без описания')
            result.append({
                'src': src,
                'alt': alt
            })
        return result
    except Exception as e:
        return []

def get_all_paragraphs(soup):
    try:
        paragraphs = soup.find_all('p')
        result = []
        for p in paragraphs:
            text = p.text.strip()
            if text:
                result.append(text)
        return result
    except Exception as e:
        return []

def search_text_in_page(soup, search_text):
    try:
        text_content = soup.get_text()
        if search_text.lower() in text_content.lower():
            return True, f"Текст '{search_text}' найден на странице"
        else:
            return False, f"Текст '{search_text}' не найден на странице"
    except Exception as e:
        return False, f"Ошибка при поиске: {str(e)}"

def get_page_info(soup):
    try:
        info = {
            'title': get_page_title(soup),
            'headings_count': len(get_all_headings(soup)),
            'links_count': len(get_all_links(soup)),
            'images_count': len(get_all_images(soup)),
            'paragraphs_count': len(get_all_paragraphs(soup))
        }
        return info
    except Exception as e:
        return None

def run():
    print("\n=== HTML Парсер ===")
    soup = None
    current_url = None
    
    while True:
        print("\nВыберите действие:")
        print("1. Загрузить страницу")
        if soup:
            print("2. Показать заголовок страницы")
            print("3. Найти все заголовки (h1-h6)")
            print("4. Найти заголовки определённого уровня")
            print("5. Найти все ссылки")
            print("6. Найти элементы по тегу")
            print("7. Найти элементы по классу")
            print("8. Найти все изображения")
            print("9. Найти все параграфы")
            print("10. Поиск текста на странице")
            print("11. Общая информация о странице")
        print("0. Назад")
        
        выбор = input("\nВыберите действие: ").strip()
        
        if выбор == "1":
            url = input("Введите URL страницы: ").strip()
            if url:
                if not url.startswith(('http://', 'https://')):
                    url = 'https://' + url
                print("\nЗагрузка страницы...")
                soup, ошибка = load_page(url)
                if soup:
                    current_url = url
                    print(f"Страница успешно загружена: {url}")
                    title = get_page_title(soup)
                    print(f"Заголовок: {title}")
                else:
                    print(ошибка)
            else:
                print("URL не может быть пустым!")
            input("\nНажмите Enter для продолжения...")
            
        elif выбор == "2" and soup:
            title = get_page_title(soup)
            print(f"\n=== Заголовок страницы ===")
            print(title)
            input("\nНажмите Enter для продолжения...")
            
        elif выбор == "3" and soup:
            headings = get_all_headings(soup)
            print(f"\n=== Все заголовки (найдено: {len(headings)}) ===")
            for i, heading in enumerate(headings, 1):
                print(f"{i}. [{heading['tag']}] {heading['text']}")
            input("\nНажмите Enter для продолжения...")
            
        elif выбор == "4" and soup:
            try:
                level = int(input("Введите уровень заголовка (1-6): ").strip())
                if 1 <= level <= 6:
                    headings = get_all_headings(soup, level)
                    print(f"\n=== Заголовки h{level} (найдено: {len(headings)}) ===")
                    for i, heading in enumerate(headings, 1):
                        print(f"{i}. {heading['text']}")
                else:
                    print("Уровень должен быть от 1 до 6!")
            except ValueError:
                print("Введите число от 1 до 6!")
            input("\nНажмите Enter для продолжения...")
            
        elif выбор == "5" and soup:
            links = get_all_links(soup)
            print(f"\n=== Все ссылки (найдено: {len(links)}) ===")
            for i, link in enumerate(links[:50], 1):
                print(f"{i}. {link['text']} -> {link['url']}")
            if len(links) > 50:
                print(f"... и ещё {len(links) - 50} ссылок")
            input("\nНажмите Enter для продолжения...")
            
        elif выбор == "6" and soup:
            tag = input("Введите название тега (например: div, p, span): ").strip().lower()
            if tag:
                elements = find_elements_by_tag(soup, tag)
                print(f"\n=== Элементы с тегом <{tag}> (найдено: {len(elements)}) ===")
                for i, elem in enumerate(elements[:20], 1):
                    print(f"{i}. {elem['text']}")
                if len(elements) > 20:
                    print(f"... и ещё {len(elements) - 20} элементов")
            else:
                print("Название тега не может быть пустым!")
            input("\nНажмите Enter для продолжения...")
            
        elif выбор == "7" and soup:
            class_name = input("Введите название класса: ").strip()
            if class_name:
                elements = find_elements_by_class(soup, class_name)
                print(f"\n=== Элементы с классом '{class_name}' (найдено: {len(elements)}) ===")
                for i, elem in enumerate(elements[:20], 1):
                    print(f"{i}. [{elem['tag']}] {elem['text']}")
                if len(elements) > 20:
                    print(f"... и ещё {len(elements) - 20} элементов")
            else:
                print("Название класса не может быть пустым!")
            input("\nНажмите Enter для продолжения...")
            
        elif выбор == "8" and soup:
            images = get_all_images(soup)
            print(f"\n=== Все изображения (найдено: {len(images)}) ===")
            for i, img in enumerate(images[:20], 1):
                print(f"{i}. {img['alt']}")
                print(f"   URL: {img['src']}")
            if len(images) > 20:
                print(f"... и ещё {len(images) - 20} изображений")
            input("\nНажмите Enter для продолжения...")
            
        elif выбор == "9" and soup:
            paragraphs = get_all_paragraphs(soup)
            print(f"\n=== Все параграфы (найдено: {len(paragraphs)}) ===")
            for i, para in enumerate(paragraphs[:10], 1):
                print(f"{i}. {para[:200]}...")
            if len(paragraphs) > 10:
                print(f"... и ещё {len(paragraphs) - 10} параграфов")
            input("\nНажмите Enter для продолжения...")
            
        elif выбор == "10" and soup:
            search_text = input("Введите текст для поиска: ").strip()
            if search_text:
                found, message = search_text_in_page(soup, search_text)
                print(f"\n=== Результат поиска ===")
                print(message)
            else:
                print("Текст для поиска не может быть пустым!")
            input("\nНажмите Enter для продолжения...")
            
        elif выбор == "11" and soup:
            info = get_page_info(soup)
            if info:
                print("\n=== Общая информация о странице ===")
                print(f"Заголовок: {info['title']}")
                print(f"Заголовков (h1-h6): {info['headings_count']}")
                print(f"Ссылок: {info['links_count']}")
                print(f"Изображений: {info['images_count']}")
                print(f"Параграфов: {info['paragraphs_count']}")
            input("\nНажмите Enter для продолжения...")
            
        elif выбор == "0":
            break
        else:
            if not soup and выбор != "1" and выбор != "0":
                print("Сначала загрузите страницу (выберите пункт 1)!")
            else:
                print("Неверный выбор!")

