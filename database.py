import sqlite3
from bs4 import BeautifulSoup
import requests

# Имя базы данных
DB_NAME = "games.db"

# URL страницы с играми
BASE_URL = "https://www.oldgames.sk/en/pc-games.php"

def initialize_db():
    """
    Инициализирует базу данных, создавая таблицу, если её ещё нет.
    """
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS games (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                year TEXT,
                category TEXT,
                rating TEXT,
                image_url TEXT
            )
        ''')
        conn.commit()
        print("База данных успешно инициализирована.")
    except sqlite3.Error as e:
        print(f"Ошибка инициализации базы данных: {e}")
    finally:
        conn.close()

def save_game_data(game_data):
    """
    Сохраняет данные игры в базу данных.
    """
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO games (title, year, category, rating, image_url)
            VALUES (?, ?, ?, ?, ?)
        ''', (game_data['title'], game_data['year'], game_data['category'], game_data['rating'], game_data['image_url']))
        conn.commit()
        print(f"Данные сохранены: {game_data['title']}")
    except sqlite3.Error as e:
        print(f"Ошибка сохранения данных: {e}")
    finally:
        conn.close()

def fetch_game_links():
    """
    Получает ссылки на страницы игр с основной страницы.
    """
    response = requests.get(BASE_URL)
    if response.status_code != 200:
        raise Exception(f"Ошибка при запросе страницы {BASE_URL}, код {response.status_code}")

    soup = BeautifulSoup(response.text, 'html.parser')
    links = []

    # Найти все ссылки на игры
    for link in soup.find_all('a', href=True):
        if "/en/game/" in link['href']:
            game_url = "https://www.oldgames.sk" + link['href']
            links.append(game_url)

    return links

def fetch_game_details(url):
    """
    Собирает детали игры с указанной страницы.
    """
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Ошибка при запросе страницы {url}, код {response.status_code}")

    soup = BeautifulSoup(response.text, 'html.parser')

    # Название игры
    title = soup.find('h1').text.strip() if soup.find('h1') else "Не указано"
    title = title.replace("download", "").strip()

    # Год выпуска
    year_label = soup.find('b')
    year = year_label.find('a').text.strip() if year_label and year_label.find('a') else "Не указано"

    # Категория
    category_label = soup.find('div', class_='labelDark', string="category")
    category_td = category_label.find_parent('td').find_next_sibling('td') if category_label else None
    category = category_td.find('a').text.strip() if category_td and category_td.find('a') else "Не указано"

    # Рейтинг
    rating_label = soup.find(string="rating (OldGames): ")
    rating = rating_label.find_next('b').text.strip() if rating_label and rating_label.find_next('b') else "Не указано"

    # URL изображения
    image_anchor = soup.find('a', href=lambda x: x and "/pictures/" in x)
    image_element = image_anchor.find('img') if image_anchor else None
    image_url = "https://www.oldgames.sk" + image_element['src'] if image_element else "Не указано"

    return {
        "title": title,
        "year": year,
        "category": category,
        "rating": rating,
        "image_url": image_url,
    }

def main():
    # Инициализация базы данных
    initialize_db()

    # Получение ссылок на игры
    print("Собираю ссылки на игры...")
    game_links = fetch_game_links()

    print(f"Найдено {len(game_links)} игр. Обработка начата...")
    for idx, link in enumerate(game_links, start=1):  # Ограничимся 10 играми для теста
        print(f"[{idx}/{len(game_links)}] Обработка: {link}")
        try:
            game_data = fetch_game_details(link)
            print(f"Собрано: {game_data}")

            # Сохранение данных в базу
            save_game_data(game_data)
        except Exception as e:
            print(f"Ошибка для {link}: {e}")

if __name__ == "__main__":
    main()


def get_all_monitors():
    return None