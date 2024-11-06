from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parser_kinopoisk(driver, url):
    page = 1
    movies = []
    logging.info(f"Начало парсинга: {url}")

    while True:

        page_url = f"{url}?page={page}"
        driver.get(page_url)
        logging.info(f"Загружаю страницу {page_url}")

        try:

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '.styles_content__nT2IG'))
            )
        except Exception as e:
            logging.error(
                f"Ошибка при ожидании загрузки элементов на странице {page}: {e}")
            break

        try:
            movie_elements = driver.find_elements(
                By.CSS_SELECTOR, '.styles_content__nT2IG')
        except Exception as e:
            logging.error(
                f"Ошибка при получении элементов с фильмами на странице {page}: {e}")
            break

        for movie_element in movie_elements:
            movie = {}

            try:
                title = movie_element.find_element(
                    By.CSS_SELECTOR, '.styles_mainTitle__IFQyZ').text
            except Exception as e:
                logging.warning(f"Ошибка при получении названия фильма: {e}")
                title = None

            try:
                country_and_director = movie_element.find_element(
                    By.CSS_SELECTOR, '.desktop-list-main-info_truncatedText__IMQRP').text
            except Exception as e:
                logging.warning(
                    f"Ошибка при получении страны и режиссера: {e}")
                country_and_director = None

            if country_and_director:
                parts = country_and_director.split('•')
                if len(parts) > 1:
                    country = parts[0].strip()
                    director_part = parts[1].strip()
                    if 'Режиссёр:' in director_part:
                        director = director_part.split('Режиссёр:')[1].strip()
                    else:
                        director = None
                else:
                    country = None
                    director = None
            else:
                country = None
                director = None

            try:
                year_and_duration = movie_element.find_element(
                    By.CSS_SELECTOR, '.desktop-list-main-info_secondaryText__M_aus').text
                if year_and_duration:
                    parts = year_and_duration.split(',')

                    if len(parts) == 3:
                        year = parts[1].strip()
                    elif len(parts) == 2:
                        year = parts[0].strip()
                    else:
                        year = None
                else:
                    year = None
            except Exception as e:
                logging.warning(f"Ошибка при получении года: {e}")
                year = None

            try:
                rating = movie_element.find_element(
                    By.CSS_SELECTOR, '.styles_kinopoiskValuePositive__7AAZG, .styles_kinopoiskValueNeutral__4c8gP').text
            except Exception as e:
                logging.warning(f"Ошибка при получении рейтинга: {e}")
                rating = None

            try:
                watch_button_element = movie_element.find_element(
                    By.CSS_SELECTOR, '.style_button__PNtXT')
                watch_button_text = watch_button_element.text
                if "Смотреть" in watch_button_text:
                    has_watch_button = True
                else:
                    has_watch_button = False
            except Exception as e:
                has_watch_button = False

            movie = {
                'title': title,
                'country': country,
                'year': year,
                'rating': rating,
                'director': director,
                'has_watch_button': has_watch_button
            }

            movies.append(movie)

        try:
            next_page_button = driver.find_element(
                By.CSS_SELECTOR, '.styles_end__aEsmB')
            if "Вперед" in next_page_button.get_attribute('class'):
                logging.info(f"Достигнут конец списка на странице {page}.")
                break
            else:
                page += 1
                logging.info(f"Перехожу на страницу {page}...")
        except Exception as e:
            logging.error(
                f"Ошибка при поиске кнопки следующей страницы на странице {page}: {e}")
            break

    logging.info(f"Парсинг завершен. Найдено {len(movies)} фильмов.")
    return movies
