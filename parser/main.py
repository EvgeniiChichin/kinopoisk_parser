from scraper import parser_kinopoisk
from config import get_driver
from utils import create_database, save_movies_to_db

if __name__ == "__main__":
    driver = get_driver()
    url = "https://www.kinopoisk.ru/lists/movies/top_1000/"

    create_database()

    movies = parser_kinopoisk(driver, url)

    save_movies_to_db(movies)

    driver.quit()

    print(f"Сохранено {len(movies)} фильмов в базу данных.")
