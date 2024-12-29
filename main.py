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

            # Check in the user table
            cursor.execute(
                "SELECT * FROM user WHERE email = %s AND password = %s",
                (email, password),
            )
            user = cursor.fetchone()

            # Check in the admin table
            cursor.execute(
                "SELECT * FROM Admin WHERE email = %s AND password = %s",
                (email, password),
            )
            admin = cursor.fetchone()

            conn.close()

            # Redirect based on match
            if user:
                return redirect("/catalog")
            elif admin:
                return redirect("/admindashboard")
            else:
                flash("Wrong email/password", "error")
                return redirect("/")  # Redirect back to the login page

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
                print("Email already exists")
                return redirect("/signup")
            except Exception as e:
                print(f"An error occurred: {e}")
                return redirect("/signup")
    
    return render_template("signup.html")

# Catalog Page
@app.route("/catalog", methods=["GET"])
def catalog():
    conn = get_db_connection()
    if not conn:
        flash("Database connection failed", "error")
        return "Error connecting to the database."

    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Books")
        book_list = cursor.fetchall()
    except mariadb.Error as e:
        flash(f"Database query failed: {e}", "error")
        return "Error querying the database."
    finally:
        cursor.close()
        conn.close()
    print(book_list)
    return render_template('catalog.html', books=book_list)

#Admin Dashboard page
@app.route("/admindashboard",methods=["GET","POST"])
def admin_dashboard():
    conn = get_db_connection()
    if not conn:
        flash("Database connection failed", "error")
        return "Error connecting to the database."

    cursor = conn.cursor()
    try:
        cursor.execute("SELECT B.ISBN, B.Book_Name, B.Author, B.Availability, B.Rating, U.First_Name FROM Books B LEFT JOIN LEND L ON B.ISBN = L.ISBN LEFT JOIN User U ON L.User_Id = U.User_Id ORDER BY B.Book_Name")
        book_list = cursor.fetchall()
    except mariadb.Error as e:
        flash(f"Database query failed: {e}", "error")
        return "Error querying the database."
    finally:
        cursor.close()
        conn.close()
        
    return render_template('admindashboard.html', books=book_list)

@app.route('/add_book', methods=['GET'])
def add_book_form():
    return render_template('add_book.html')


@app.route('/add_book', methods=['POST'])
def add_book():
    # Get form data
    isbn = request.form['isbn']
    book_name = request.form['book_name']
    author = request.form['author']
    availability = int(request.form['availability'])
    rating = float(request.form['rating'])

    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            # Insert the new book into the database
            cursor.execute(
                "INSERT INTO Books (ISBN, Book_Name, Author, Availability, Rating) VALUES (%s, %s, %s, %s, %s)",
                (isbn, book_name, author, availability, rating),
            )
            conn.commit()
            flash('Book added successfully!', 'success')
        except Exception as e:
            flash(f'Error adding book: {e}', 'error')
        finally:
            cursor.close()
            conn.close()
    else:
        flash('Failed to connect to the database', 'error')

    return redirect('/admindashboard')   


@app.route('/delete_book', methods=['POST'])
def delete_book():
    isbn = request.form['isbn']

    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Books WHERE ISBN = %s", (isbn,))
            conn.commit()
            print('Book deleted successfully!', 'success')
        except Exception as e:
            flash(f'Error deleting book: {e}', 'error')
        finally:
            cursor.close()
            conn.close(
)
    else:
        flash('Failed to connect to the database', 'error')

    # Redirect back to the catalog page
    return redirect('/admindashboard')

if __name__ == "__main__":
    app.run(debug=True)