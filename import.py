import csv
import os

from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


app = Flask(__name__)

engine = create_engine("postgresql://postgres:aditya05@localhost:5432/postgres")
#engine = create_engine("DATABASE_URL")
db = scoped_session(sessionmaker(bind=engine))



@app.route("/")
def index():
    flights = db.execute("SELECT * FROM flights").fetchall()
    return render_template("index.html", flights=flights)


@app.route("/bookf", methods=["POST","GET"])
def bookf():
    """Book a flight."""

    return render_template("book.html", )


@app.route("/book", methods=["POST","GET"])
def book():
    """Book a flight."""

    # Get form information.
    name = request.form.get("name")

    try:
        flight_id = int(request.form.get("flight_id"))
    except ValueError:
        return render_template("error.html", message="Invalid flight number.")

    # Make sure flight exists.
    if db.execute("SELECT * FROM flights WHERE id = :id", {"id": flight_id}).rowcount == 0:
        return render_template("error.html", message="No such flight with that id.")
    db.execute("INSERT INTO passengers (name, flight_id) VALUES (:name, :flight_id)",
            {"name": name, "flight_id": flight_id})
    db.commit()

    return render_template("success.html")



'''def main():
	f = open("flights.csv")
	reader = csv.reader(f)
	for origin, destination, duration in reader:
		db.execute("INSERT INTO flights(origin, destination, duration) VALUES(:origin, :destination, :duration)", 					{"origin": origin, "destination": destination, "duration": duration})
		print(f"Added flights from {origin} to {destination}lasting {duration} minutes.")
	db.commit()
	
if __name__ == "__main__":
	main()
	
'''	
