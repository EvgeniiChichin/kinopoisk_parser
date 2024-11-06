import sqlite3
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def create_database(db_name="movies.db"):
    """Создает базу данных и таблицу movies, если она не существует."""
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                country TEXT,
                year TEXT,
                rating TEXT,
                director TEXT,
                has_watch_button INTEGER
            )
        ''')
        conn.commit()
        logging.info("Таблица 'movies' создана или уже существует.")
    except Exception as e:
        logging.error(f"Ошибка при создании таблицы: {e}")
    finally:
        conn.close()


def save_movies_to_db(movies, db_name="movies.db"):
    """Сохраняет список фильмов в базу данных."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    try:
        for movie in movies:
            cursor.execute('''
                INSERT INTO movies (title, country, year, rating, director, has_watch_button)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (movie['title'], movie['country'], movie['year'], movie['rating'], movie['director'], movie['has_watch_button']))
        conn.commit()
        logging.info(f"Сохранено {len(movies)} фильмов в базе данных.")
    except Exception as e:
        logging.error(f"Ошибка при сохранении данных: {e}")
    finally:
        conn.close()
