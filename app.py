from flask import Flask, render_template, request, redirect
from db_config import get_connection

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/add_car", methods=["GET", "POST"])
def add_car():
    if request.method == "POST":
        brand = request.form["brand"]
        model = request.form["model"]
        rent = request.form["rent"]
        con = get_connection()
        cur = con.cursor()
        cur.execute(
            "INSERT INTO cars (brand, model, rent_per_day) VALUES (%s, %s, %s)",
            (brand, model, rent),
        )
        con.commit()
        con.close()
        return redirect("/view_cars")
    return render_template("add_car.html")


@app.route("/view_cars")
def view_cars():
    con = get_connection()
    cur = con.cursor(dictionary=True)
    cur.execute("SELECT * FROM cars")
    cars = cur.fetchall()
    con.close()
    return render_template("view_cars.html", cars=cars)


@app.route("/book_car/<int:car_id>", methods=["GET", "POST"])
def book_car(car_id):
    con = get_connection()
    cur = con.cursor(dictionary=True)
    cur.execute("SELECT * FROM cars WHERE id = %s", (car_id,))
    car = cur.fetchone()

    if request.method == "POST":
        name = request.form["name"]
        days = int(request.form["days"])
        total_cost = days * car["rent_per_day"]
        cur.execute(
            "INSERT INTO bookings (car_id, customer_name, days, total_cost) VALUES (%s, %s, %s, %s)",
            (car_id, name, days, total_cost),
        )
        cur.execute("UPDATE cars SET available = FALSE WHERE id = %s", (car_id,))
        con.commit()
        con.close()
        return redirect("/view_bookings")

    con.close()
    return render_template("book_car.html", car=car)


@app.route("/view_bookings")
def view_bookings():
    con = get_connection()
    cur = con.cursor(dictionary=True)
    cur.execute("""
        SELECT b.id, b.customer_name, c.brand, c.model, b.days, b.total_cost 
        FROM bookings b JOIN cars c ON b.car_id = c.id
    """)
    bookings = cur.fetchall()
    con.close()
    return render_template("view_bookings.html", bookings=bookings)


if __name__ == "__main__":
    app.run(debug=True)
