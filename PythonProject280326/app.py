from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="P@$$w0rd",
    database="home_automation"
)

@app.route('/')
def index():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM devices")
    devices = cursor.fetchall()
    return render_template('index.html', devices=devices)

@app.route('/toggle/<int:id>')
def toggle(id):
    cursor = db.cursor()
    cursor.execute("SELECT status FROM devices WHERE id=%s", (id,))
    current = cursor.fetchone()[0]

    new_status = "OFF" if current == "ON" else "ON"

    cursor.execute("UPDATE devices SET status=%s WHERE id=%s", (new_status, id))
    db.commit()

    return redirect('/')

@app.route('/view/<int:id>')
def view(id):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM devices WHERE id=%s", (id,))
    device = cursor.fetchone()
    return render_template('view.html', device=device)

if __name__ == '__main__':
    app.run(debug=True)