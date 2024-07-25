from flask import Flask, jsonify
app = Flask(__name__)
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
ma = Marshmallow(app)


app = Flask(__name__)

## DB CONNECTION AREA
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://tomato:qwerty@localhost:5432/ripe_tomatoes_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Creating the database object
db = SQLAlchemy(app)

# CLI COMMANDS AREA

# Create app's cli command named create, so you can the run it in the terminal as "flask create", it will invoke create_db function.
@app.cli.command("create")
def create_db():
    db.create_all()
    print("Tables created")

# Create app's cli command named seed, so you can add or seed Movie and Actor objects to their respective tables.
@app.cli.command("seed")
def seed_db():
   # Import the datatime module to get the Date format for dob.
   from datetime import date
   # Create first Movie object:
   Movie1 = Movie(
      title = "The Shawshank Redemption",
      genre = "Drama",
      length = 142,
      release_year = 1994
   )
   # Add the object as a new row to the Movies table
   db.session.add(Movie1)
   
   Movie2 = Movie(
      title = "The Fugitive",
      genre = "Action",
      length = 130,
      release_year = 1993
   )
   db.session.add(Movie2)

   Movie3 = Movie(
      title = "Office Space",
      genre = "Comedy",
      length = 89,
      release_year = 1999
   )
   db.session.add(Movie3)

   Movie4 = Movie(
      title = "Pirates Of The Caribbean",
      genre = "Adventure",
      length = 143,
      release_year = 2003
   )
   db.session.add(Movie4)

   # Create First Actor object:
   Actor1 = Actor(
      f_name = "Morgan",
      l_name = "Freeman",
      gender = "Male",
      country = "USA",
      dob = date(1937, 6, 1)
   )
   db.session.add(Actor1)

   Actor2 = Actor(
      f_name = "Harrison",
      l_name = "Ford",
      gender = "Male",
      country = "USA",
      dob = date(1942, 7, 13)
      )
   db.session.add(Actor2)

   Actor3 = Actor(
      f_name = "Jennifer",
      l_name = "Aniston",
      gender = "Female",
      country = "USA",
      dob = date(1969, 2, 11)
   )
   db.session.add(Actor3)

   Actor4 = Actor(
      f_name = "Johnny",
      l_name = "Depp",
      gender = "Male",
      country = "USA",
      dob = date(1963, 6, 9)
   )
   db.session.add(Actor4)

   # Commit the changes
   db.session.commit()
   print("Table Seeded")
   

# Create app's cli command name drop, so you can the run it in the terminal as "flask drop", will delete tables from database.
@app.cli.command("drop")
def drop_db():
    db.drop_all()
    print("Tables dropped") 

# MODELS AREA

# Movie class Model
class Movie(db.Model):
  # Define the table's name
   __tablename__ = "MOVIES"
   # Set primary key
   id = db.Column(db.Integer,primary_key=True)
   # Set the other attributes
   title = db.Column(db.String())
   genre = db.Column(db.String())
   length = db.Column(db.Integer)
   release_year = db.Column(db.Integer)

# Actor class Model
class Actor(db.Model):
   __tablename__ = "ACTORS"
   id = db.Column(db.Integer,primary_key=True)
   f_name = db.Column(db.String())
   l_name = db.Column(db.String())
   gender = db.Column(db.String())
   country = db.Column(db.String())
   # Date stores values like: 2024-07-25
   dob = db.Column(db.Date)

# SCHEMAS AREA

# Create the Movies Schema with Marshmallow, it will provide the serialization needed for converting the data into JSON
class MovieSchema(ma.Schema):
   class Meta:
      # Fields to expose
      fields = ("id", "title", "genre", "length", "release_year")
# Single movie schema, when one movie needs to be retrieved
movie_schema = MovieSchema()
# Multiple movie schema, when many movies need to be retrieved
movies_schema = MovieSchema(many=True)

# Create the Actors Schema with Marshmallow
class ActorSchema(ma.Schema):
   class Meta:
      fields = ("id", "f_name", "l_name", "gender", "country", "dob")
actor_schema = ActorSchema()
actors_schema = ActorSchema(many=True)

# ROUTING AREA

# Creating the movies route.
@app.route("/movies", methods=["GET"])
def get_movies():
   # Get all movies from the database:
   movies_list = Movie.query.all()
   # Convert the cards from the database into a JSON format and store them in result
   result = movies_schema.dump(movies_list)
   # Return the data in JSON format
   return jsonify(result)

# Creating the actors route.
@app.route("/actors", methods=["GET"])
def get_actors():
   actors_list = Actor.query.all()
   result = actors_schema.dump(actors_list)
   return jsonify(result)
   
# Creating the hello page route.
@app.route("/")
def hello():
  return "Welcome to Ripe Tomatoes API"
