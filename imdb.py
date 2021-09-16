from bs4 import BeautifulSoup
import requests
import sqlite3

conn = sqlite3.connect('top_movies.db')
c = conn.cursor()
with conn:
    c.execute('''CREATE TABLE IF NOT EXISTS movies (rank INTEGER, title TEXT, year INTEGER, rating REAL) ''')

url = "https://www.imdb.com/chart/top/"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:91.0) Gecko/20100101 Firefox/91.0"}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")
body = soup.find("tbody")

with conn:
    for line in body.find_all("tr"):
        rank = int(line.find("td", class_="titleColumn").text.split(".")[0])
        title = line.find("img", alt=True)['alt']
        year = int(line.find("span", class_="secondaryInfo").text.replace("(", "").replace(")", ""))
        rating = float(line.find("td", class_="ratingColumn imdbRating").text)
        sql = """INSERT INTO movies (rank, title, year, rating) VALUES (?, ?, ?, ?)"""
        c.execute(sql, (rank, title, year, rating))

with conn:
    c.execute('''SELECT * FROM movies''')
    print(c.fetchall())