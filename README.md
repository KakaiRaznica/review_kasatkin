
# RetroGame Vault

RetroGame Vault — это веб-приложение для скрапинга информации о ретро-играх. Оно позволяет пользователям искать игры, фильтровать их по категориям, годам выпуска и диапазонам оценок, а также отображает игры в удобных карточках с изображениями и описанием.

---

## Функциональность

- **Скрапинг данных**: Автоматический сбор данных о ретро-играх с веб-ресурса.
- **Фильтры**:
  - По категории.
  - По году выпуска.
  - По диапазону оценок (0-25, 25-50 и т.д.).
- **Поиск**: Возможность искать игры по ключевым словам.
- **Карточки**: Удобное отображение игр в виде карточек с изображением, названием, категорией, годом и рейтингом.

---

## Установка и запуск

### Локальный запуск

1. **Клонируйте репозиторий**:
   ```bash
   https://github.com/KakaiRaznica/review_kasatkin.git
   cd retrogame-vault
   ```

2. **Установите зависимости**:
   Убедитесь, что у вас установлен Python 3.9 или выше. Установите зависимости из `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

3. **Запустите приложение**:
   ```bash
   python app.py
   ```

4. **Откройте приложение**:
   Перейдите в браузере по адресу:
   ```
   http://127.0.0.1:5000
   ```

---

### Запуск с Docker

1. **Убедитесь, что Docker установлен**:
   Установите [Docker](https://www.docker.com/products/docker-desktop), если он ещё не установлен.

2. **Соберите и запустите контейнер**:
   Выполните команду:
   ```bash
   docker-compose up --build
   ```

3. **Откройте приложение**:
   Перейдите в браузере по адресу:
   ```
   http://localhost:5000
   ```

4. **Остановка контейнеров**:
   Для остановки приложения выполните:
   ```bash
   docker-compose down
   ```

---

## Скрипты

- **`build.sh`**: Скрипт для автоматического запуска приложения с использованием Docker Compose.

---

## Структура проекта

```plaintext
.
├── app.py               # Основное приложение Flask
├── requirements.txt     # Зависимости Python
├── Dockerfile           # Конфигурация Docker
├── docker-compose.yml   # Docker Compose для запуска приложения
├── templates/           # HTML-шаблоны
│   └── index.html       # Главная страница приложения
├── static/              # Статические файлы (CSS, изображения)
│   └── styles.css       # Стили приложения
├── scraper.py           # Скрипт для скрапинга данных
└── games.db             # SQLite база данных
```

---

## Пример использования

1. Перейдите на главную страницу.
2. Используйте фильтры для выбора категории, года или диапазона оценок.
3. Введите ключевые слова в строку поиска для нахождения конкретной игры.
4. Просмотрите игры в виде карточек с изображением и описанием.

---

## Будущие улучшения

- Добавление возможности авторизации пользователей.
- Усовершенствование интерфейса.
- Поддержка сохранения избранных игр.
- Деплой на удалённый сервер.

---

## Лицензия

Этот проект распространяется под [MIT License](LICENSE).
