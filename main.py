from flask import Flask, render_template, request

local_server=True
app= Flask(__name__)

@app.route("/", methods=["GET","POST"])
def login():
    return render_template('login.html')

@app.route("/sign-up" , methods=["GET","POST"])
def sign_up():
    return render_template('signup.html')


app.run(debug=True)