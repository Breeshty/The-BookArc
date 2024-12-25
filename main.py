import mariadb
from flask import Flask, render_template, request, redirect, flash

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Replace with a secure key

# Database connection function
def get_db_connection():
    try:
        conn = mariadb.connect(
            user="flask_user",
            password="BristyZarifShafin",
            host="localhost",
            port=3306,
            database="The_BookArc"
        )
        return conn
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB: {e}")
        return None

# Login Page
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM user WHERE email = %s AND password = %s",
                (email, password),
            )
            user = cursor.fetchone()
            conn.close()
            if user:
                return redirect("/catalog")
            else:
                flash("Wrong email/password", "error")
                return redirect("/")  # Redirect back to the same login page
    return render_template("login.html")

# Signup Page
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        
        if password != confirm_password:
            flash("Passwords do not match")
            return redirect("/signup")
        
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "INSERT INTO user (first_name, last_name, email, password) VALUES (%s, %s, %s,%s)",
                    (first_name, last_name, email, password),
                )
                conn.commit()
                conn.close()
                return redirect("/catalog")
            except mariadb.IntegrityError:
                flash("Email already exists")
                return redirect("/signup")
            except Exception as e:
                flash(f"An error occurred: {e}")
                return redirect("/signup")
    
    return render_template("signup.html")

# Catalog Page
@app.route("/catalog")
def catalog():
    return "Welcome to the catalog!"

if __name__ == "__main__":
    app.run(debug=True)
