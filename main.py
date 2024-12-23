from database import initialize_db, save_game_data, fetch_game_links, fetch_game_details


def main():
    """
    Основная функция для выполнения скрапинга данных о играх
    и их сохранения в базу данных.
    """
    print("Инициализация базы данных...")
    initialize_db()

    print("Получение ссылок на игры...")
    try:
        game_links = fetch_game_links()
        print(f"Найдено {len(game_links)} игр.")
    except Exception as e:
        print(f"Ошибка при получении ссылок: {e}")
        return

    print("Начало обработки игр...")
    for idx, link in enumerate(game_links[:10], start=1):  # Ограничение на 10 игр для теста
        print(f"[{idx}/{len(game_links)}] Обработка: {link}")
        try:
            game_data = fetch_game_details(link)
            print(f"Собрано: {game_data}")

            save_game_data(game_data)
        except Exception as e:
            print(f"Ошибка для {link}: {e}")

    print("Скрапинг завершен!")


if __name__ == "__main__":
    main()
