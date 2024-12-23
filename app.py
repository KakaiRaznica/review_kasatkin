from flask import Flask, jsonify, request, render_template
import sqlite3

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/games", methods=["GET"])
def get_games():
    """
    API для получения игр с фильтрацией и пагинацией.
    """
    page = int(request.args.get("page", 1))  # Текущая страница (по умолчанию 1)
    per_page = int(request.args.get("per_page", 20))  # Количество игр на странице (по умолчанию 20)

    # Фильтры
    search = request.args.get("search", "").strip()
    category = request.args.get("category", "").strip()
    year = request.args.get("year", "").strip()
    rating_range = request.args.get("rating_range", "").strip()

    offset = (page - 1) * per_page

    conn = sqlite3.connect('games.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Базовый запрос
    query = "SELECT * FROM games WHERE 1=1"
    params = []

    # Применяем фильтры
    if search:
        query += " AND title LIKE ?"
        params.append(f"%{search}%")
    if category:
        query += " AND category = ?"
        params.append(category)
    if year:
        query += " AND year = ?"
        params.append(year)
    if rating_range:
        try:
            min_rating, max_rating = map(int, rating_range.split('-'))
            query += " AND CAST(rating AS INTEGER) BETWEEN ? AND ?"
            params.extend([min_rating, max_rating])
        except ValueError:
            pass  # Игнорируем некорректные диапазоны рейтингов

    # Считаем общее количество записей с учётом фильтров
    total_query = f"SELECT COUNT(*) FROM ({query})"
    cursor.execute(total_query, params)
    total_games = cursor.fetchone()[0]

    # Применяем пагинацию
    query += " LIMIT ? OFFSET ?"
    params.extend([per_page, offset])

    cursor.execute(query, params)
    games = cursor.fetchall()
    conn.close()

    # Формируем ответ
    return jsonify({
        "games": [dict(row) for row in games],
        "total_games": total_games,
        "page": page,
        "per_page": per_page,
        "total_pages": (total_games + per_page - 1) // per_page  # Округляем вверх
    })

@app.route("/api/categories", methods=["GET"])
def get_categories():
    """
    API для получения списка уникальных категорий.
    """
    conn = sqlite3.connect('games.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Получаем уникальные категории
    cursor.execute("SELECT DISTINCT category FROM games WHERE category IS NOT NULL")
    categories = [row["category"] for row in cursor.fetchall()]
    conn.close()

    return jsonify(categories)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
