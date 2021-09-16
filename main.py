from flask import Flask, request, jsonify
import sqlite3

# Init app
app = Flask(__name__)

# Init database
def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("top_movies.db")
    except sqlite3.Error as e:
        print(e)
    return conn

@app.route("/")
def home():
    return "Go to /movies"

# C R U D
@app.route("/movies", methods=["GET", "POST"])
def movies():
    conn = db_connection()
    c = conn.cursor()

    if request.method == "GET":
        all = c.execute("""SELECT * FROM movies""")
        movies = [dict(rank=row[0], title=row[1], year=row[2], rating=row[3])
                  for row in all.fetchall()]
        if movies is not None:
            return jsonify(movies)

    if request.method == "POST":
        new_rank = request.form["rank"]
        new_title = request.form["title"]
        new_year = request.form["year"]
        new_rating = request.form["rating"]
        sql = """INSERT INTO movies (rank, title, year, rating) VALUES (?, ?, ?, ?)"""
        cursor = c.execute(sql, (new_rank, new_title, new_year, new_rating))
        conn.commit()
        return f"Movie with id {cursor.lastrowid} was created."


@app.route("/movies/<int:rank>", methods=["GET", "PUT", "DELETE"])
def movie(rank):
    conn = db_connection()
    c = conn.cursor()
    movie = None
    if request.method == "GET":
        c.execute("""SELECT * FROM movies WHERE rank=?""", (rank,))
        rows = c.fetchall()
        for row in rows:
            movie = row
        if movie is not None:
            return jsonify(movie), 200
        else:
            return "Error, not found", 404

    if request.method == "PUT":
        sql = """UPDATE movies SET title=?, year=?, rating=? WHERE rank=?"""
        title = request.form["title"]
        year = request.form["year"]
        rating = request.form["rating"]
        updated_movie = {
            "rank": rank,
            "title": title,
            "year": year,
            "rating": rating
        }
        conn.execute(sql, (title, year, rating, rank))
        conn.commit()
        return jsonify(updated_movie)

    if request.method == "DELETE":
        sql = """DELETE FROM movies WHERE rank=?"""
        conn.execute(sql, (rank,))
        conn.commit()
        return f"Movie with id {rank} was deleted.", 200

# Run server
if __name__ == "__main__":
    app.run(debug=True)






