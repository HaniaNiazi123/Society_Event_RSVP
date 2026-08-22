from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)


def get_database_connection():
    base_folder = os.path.dirname(os.path.abspath(__file__))
    database_path = os.path.join(base_folder, "events.db")

    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    return connection


# Home Page
@app.route("/")
def home():
    connection = get_database_connection()

    events = connection.execute(
        "SELECT * FROM events"
    ).fetchall()

    connection.close()

    return render_template("index.html", events=events)


# Create Event
@app.route("/create_event", methods=["GET", "POST"])
def create_event():

    if request.method == "POST":

        name = request.form["name"]
        date = request.form["date"]
        location = request.form["location"]

        connection = get_database_connection()

        connection.execute(
            "INSERT INTO events (name, date, location) VALUES (?, ?, ?)",
            (name, date, location)
        )

        connection.commit()
        connection.close()

        return redirect("/")

    return render_template("create_event.html")


# Events Page
@app.route("/events")
def events():

    connection = get_database_connection()

    events = connection.execute(
        "SELECT * FROM events"
    ).fetchall()

    connection.close()

    return render_template("events.html", events=events)


# RSVP Page
@app.route("/rsvp/<int:event_id>", methods=["GET", "POST"])
def rsvp(event_id):

    connection = get_database_connection()

    event = connection.execute(
        "SELECT * FROM events WHERE id = ?",
        (event_id,)
    ).fetchone()

    if event is None:
        connection.close()
        return "Event not found"

    if request.method == "POST":

        student_name = request.form["name"]
        email = request.form["email"]

        connection.execute(
            """
            INSERT INTO rsvps (event_id, student_name, email)
            VALUES (?, ?, ?)
            """,
            (event_id, student_name, email)
        )

        connection.commit()
        connection.close()

        return "RSVP Successful! Thank you for registering."

    connection.close()

    return render_template("rsvp.html", event=event)


# RSVP Records Page
@app.route("/rsvps")
def rsvps():

    connection = get_database_connection()

    rsvps = connection.execute(
        """
        SELECT
            rsvps.id,
            rsvps.student_name,
            rsvps.email,
            events.name AS event_name
        FROM rsvps
        JOIN events ON rsvps.event_id = events.id
        ORDER BY rsvps.id DESC
        """
    ).fetchall()

    connection.close()

    return render_template("rsvps.html", rsvps=rsvps)


# Edit Event
@app.route("/edit_event/<int:event_id>", methods=["GET", "POST"])
def edit_event(event_id):

    connection = get_database_connection()

    event = connection.execute(
        "SELECT * FROM events WHERE id = ?",
        (event_id,)
    ).fetchone()

    if event is None:
        connection.close()
        return "Event not found"

    if request.method == "POST":

        name = request.form["name"]
        date = request.form["date"]
        location = request.form["location"]

        connection.execute(
            """
            UPDATE events
            SET name = ?, date = ?, location = ?
            WHERE id = ?
            """,
            (name, date, location, event_id)
        )

        connection.commit()
        connection.close()

        return redirect("/events")

    connection.close()

    return render_template("edit_event.html", event=event)


# Delete Event
@app.route("/delete_event/<int:event_id>", methods=["POST"])
def delete_event(event_id):

    connection = get_database_connection()

    connection.execute(
        "DELETE FROM rsvps WHERE event_id = ?",
        (event_id,)
    )

    connection.execute(
        "DELETE FROM events WHERE id = ?",
        (event_id,)
    )

    connection.commit()
    connection.close()

    return redirect("/events")


# Run Application
if __name__ == "__main__":
    app.run(debug=True)