from flask import Flask, render_template, request

local_server=True
app= Flask(__name__)

@app.route("/")
def main():
    return render_template('index1.html')

app.run(debug=True)