from flask import Flask, render_template, request, redirect, flash
import mariadb

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Replace with a strong key for security

# Database connection setup
def get_db_connection():
    try:
        conn = mariadb.connect(
            user="your_username",
            password="your_password",
            host="127.0.0.1",
            port=3306,
            database="your_database"
        )
        return conn
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB: {e}")
        return None

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/signup", methods=["POST"])
def signup():
    # Extract form data
    first_name = request.form["first_name"]
    email = request.form["email"]
    password = request.form["password"]
    confirm_password = request.form["confirm_password"]

    if password != confirm_password:
        flash("Passwords do not match.")
        return redirect("/")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Insert user data into the database
        cursor.execute(
            "INSERT INTO users (first_name, email, password) VALUES (?, ?, ?)",
            (first_name, email, password)
        )
        conn.commit()
        flash("Signup successful! You can now log in.")
    except mariadb.Error as e:
        flash(f"Error: {e}")
    finally:
        if conn:
            conn.close()
    return redirect("/")

@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Check if user exists and password matches
        cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        user = cursor.fetchone()

        if user:
            flash("Login successful! Welcome back.")
            # Redirect to a dashboard or homepage
        else:
            flash("Invalid email or password.")
    except mariadb.Error as e:
        flash(f"Error: {e}")
    finally:
        if conn:
            conn.close()

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
