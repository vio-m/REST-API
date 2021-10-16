from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os


# Init app, ma
app = Flask(__name__)
#db = SQLAlchemy(app)
ma = Marshmallow(app)


# Set path to db
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'top_movies.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)


# Create movie model
class Movie(db.Model):
    __tablename__ = "movies"
    rank = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    title = db.Column(db.String(100), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def __init__(self, rank, title, year, rating):
        self.rank = rank
        self.title = title
        self.year = year
        self.rating = rating

    def __repr__(self):
        return f"Movie {self.title} from {self.year}, ranked: {self.rank} and rated: {self.rating}"


# Create Schema
class MovieSchema(ma.Schema):
    class Meta:
        fields = ("rank", "title", "year", "rating")


# Init Schema
movie_schema = MovieSchema()#strict=True
movies_schema = MovieSchema(many=True,) #strict=True


@app.route("/")
def home():
    return "Go to /movies"


# C R U D
# Get all the movies
@app.route("/movies", methods=['GET'])
def get_movies():
    movies = Movie.query.all()
    result = movies_schema.dump(movies)
    return jsonify(result)

# Get one movie
@app.route("/movies/<rank>", methods=['GET'])
def get_movie(rank):
    movie = Movie.query.get(rank)
    return movie_schema.jsonify(movie)

# Create a movie entry
@app.route("/movies", methods=['POST'])
def add_movie():
    rank = request.json['rank']
    title = request.json['title']
    year = request.json['year']
    rating = request.json['rating']
    print(rank, title, year, rating)

    new_movie = Movie(rank, title, year, rating)

    db.session.add(new_movie)
    db.session.commit()

    return movie_schema.jsonify(new_movie)

# Update a movie entry
@app.route("/movies/<rank>", methods=['PUT'])
def update_movie(rank):
    movie = Movie.query.get(rank)

    rank = request.json['rank']
    title = request.json['title']
    year = request.json['year']
    rating = request.json['rating']

    movie.rank = rank
    movie.title = title
    movie.year = year
    movie.rating = rating

    db.session.commit()

    return movie_schema.jsonify(movie)

# Delete a movie entry
@app.route("/movies/<rank>", methods=['DELETE'])
def delete_movie(rank):
    movie = Movie.query.get(rank)
    if movie is None:
        return {"Movie": "was not found"}
    db.session.delete(movie)
    db.session.commit()
    return {"Movie": "was deleted"}


# Run server
if __name__ == "__main__":
    app.run(debug=True)






