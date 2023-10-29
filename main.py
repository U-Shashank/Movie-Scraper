from bs4 import BeautifulSoup
import requests
import mysql.connector
import json

with open('config.json') as config_file:
    config = json.load(config_file)


cnx = mysql.connector.connect(user=config['user'], password=config['password'],
                              host=config['host'],
                              database=config['database'])

cursor = cnx.cursor()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}

top_movies = requests.get('https://www.imdb.com/chart/top/?ref_=nv_mv_250', headers=headers)

check_table_query = "SHOW TABLES LIKE 'imdb_movies'"
cursor.execute(check_table_query)
table_exists = cursor.fetchone()

if not table_exists:
    create_table_query = """
    CREATE TABLE imdb_movies (
        movie_id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        link VARCHAR(255) NOT NULL,
        rating DECIMAL(3, 1) NOT NULL,
        year INT,
        runtime VARCHAR(6),
        certification VARCHAR(10)
    );
    """
    cursor.execute(create_table_query)

if top_movies.status_code == 200: 
    soup = BeautifulSoup(top_movies.text, 'lxml')
    movies = soup.find_all('div', class_='sc-c7e5f54-0 gytZrF cli-children')
    

    for movie in movies:
        movie_link = "https://www.imdb.com/"+movie.find('a')['href']
        movie_title = movie.find('a').h3.text.split('.')[1].strip()
        movie_rating = movie.find('span', class_='ipc-rating-star ipc-rating-star--base ipc-rating-star--imdb ratingGroup--imdb-rating').text.split()[0]
        movie_other_info = []
        other_info_div = movie.find('div', class_='sc-c7e5f54-7 brlapf cli-title-metadata')
        other_info_spans = other_info_div.find_all('span')

        for span in other_info_spans:
            movie_other_info.append(span.text)

        if len(movie_other_info) == 2:
            movie_other_info.append(None)
        movie_data = (movie_title, movie_link, movie_rating, int(movie_other_info[0]), movie_other_info[1], movie_other_info[2])
        insert_movie = """
        INSERT INTO imdb_movies (title, link, rating, year, runtime, certification)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_movie, movie_data)
        cnx.commit()

# select_query = "SELECT * FROM imdb_movies"
# cursor.execute(select_query)
# rows = cursor.fetchall()

# for row in rows:
#     print(row)

cursor.close()
cnx.close()

