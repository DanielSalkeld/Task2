import csv
import os
import sqlite3

currentlocation = os.path.dirname(os.path.abspath(__file__))

from flask import Flask, render_template, request, redirect
from datetime import datetime
from flask import Flask, request




app = Flask(__name__)

from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Database setup
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()
#Login / Register page.
@app.route("/")
def home():
    if "user" in session:
        return render_template("index.html", user=session["user"])
    return render_template("index.html")
#Allows users to register an account with Rolsa Technologies to allow them access to rest of the site.
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        return redirect(url_for("login"))

    return render_template("register.html")
#Allows users to login once they have registerd an account with Rolsa Technologies
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        #This will connect the code to the database to allow it to search for the users username and password 
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = c.fetchone()
        conn.close()

        #If users username and password does not match anything located in the database then output = "Invalid credentials"
        if user:
            session["user"] = username
            return redirect(url_for("homepage"))
        else:
            return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")
#Allows users to logout so they can switch accounts.
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))




#This allows Users to be able to book and order items or consultations/installations and keep track of it
@app.route("/bookings", methods=["GET", "POST"])
def bookings():
    if request.method == "POST":
        full_name = request.form.get("full_name")
        studentID = request.form.get("studentID")
        equipment_booked = request.form.get("equipment")
        date_of_booking = request.form.get("date_of_booking")
        days_booked = request.form.get("days")

        date_of_booking = datetime.now().strftime("%d/%m/%Y")
        
        

        
        file_exists = os.path.isfile("bookings.csv")
        with open("bookings.csv", "a", newline="") as file:
            writer = csv.writer(file)
            if not file_exists:
                    writer.writerow([
                         "full_name", "studentID", "equipment_booked",
                         "date_of_booking",
                         "days_booked"
                    ])
            writer.writerow([
                 full_name, studentID, equipment_booked,
                         date_of_booking,
                         days_booked
            ])
        return render_template(
             "confirmation.html",
             full_name=full_name,
             days_booked=days_booked,
             date_of_booking=date_of_booking,
        )
    return render_template("bookings.html")
#These html are all for information and are filled with Product information and methods to lower your carbon footprint that Rolsa Technologies provides.         
@app.route("/List")
def List():
    return render_template("List.html")

@app.route("/Solar panels")
def Camera():
     return render_template("Solar.html")

@app.route("/Information")
def Information():
     return render_template("Information.html")


@app.route("/Air-pumps")
def Lenses():
     return render_template("Airpumps.html")

@app.route("/Wind turbines")
def Tripods():
     return render_template("Wind.html")

@app.route("/Modern boilers")
def MemoryCards():
     return render_template("Boiler.html")

@app.route("/Home insulation")
def audio_equipement():
     return render_template("Insulation.html")

@app.route("/EVcharging")
def studio_lighting():
     return render_template("EVcharging.html")

@app.route("/Travel")
def Travel():
     return render_template("Travel.html")

@app.route("/Workplace")
def workplace():
     return render_template("Workplace.html")

@app.route("/HomeCarbon")
def HomeCarbon():
     return render_template("HomeCarbon.html")

@app.route("/Food")
def Food():
     return render_template("Food.html")

@app.route("/homepage", methods=["GET", "POST"])
def homepage():
     return render_template("homepage.html")
#Allows users to Calculate there own Carbon footprint to allow them to see where they are releasing emmissions and help them to reduce it through out the year.
@app.route("/carbon-footprint", methods=["GET", "POST"])
def carbon_footprint():
    if request.method == "POST":
        # Retrieve user input from form
        energy_use = float(request.form.get("energy_use", 0))  # in kWh
        travel_distance = float(request.form.get("travel_distance", 0))  # in km
        diet_type = request.form.get("diet_type", "mixed")  # 'vegan', 'vegetarian', or 'mixed'

        # Emission factors
        emission_factors = {
            "energy": 0.233,  # kg CO2e per kWh
            "car_travel": 0.121,  # kg CO2e per km
            "diet": {"vegan": 2.0, "vegetarian": 2.5, "mixed": 5.0}  # kg CO2e per day
        }

        # Calculate emissions
        energy_emissions = energy_use * emission_factors["energy"]
        travel_emissions = travel_distance * emission_factors["car_travel"]
        diet_emissions = emission_factors["diet"].get(diet_type, 5.0) * 30  # monthly

        total_emissions = energy_emissions + travel_emissions + diet_emissions

        # Render results along with the form
        return render_template("carbon_footprint.html", energy_use=energy_use, travel_distance=travel_distance,
                               diet_type=diet_type, energy_emissions=energy_emissions,
                               travel_emissions=travel_emissions, diet_emissions=diet_emissions,
                               total_emissions=total_emissions)
    return render_template("carbon_footprint.html")

     
if __name__ == "__main__":
    app.run(debug=True)
