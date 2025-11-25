from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database/cars.db')
    c = conn.cursor()


    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL)''')

    c.execute('''CREATE TABLE IF NOT EXISTS cars (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    image TEXT,
                    description TEXT,
                    base_price INTEGER,
                    end_time TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS bids (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    car_id INTEGER,
                    amount INTEGER,
                    timestamp TEXT,
                    FOREIGN KEY(user_id) REFERENCES users(id),
                    FOREIGN KEY(car_id) REFERENCES cars(id))''')


    c.execute("SELECT COUNT(*) FROM cars")
    if c.fetchone()[0] == 0:
        end_time = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
        cars = [
            ("Toyota Supra", "static/images/toyota_supra.jpg", "3.0L Turbo Coupe", 6500000, end_time),
            ("Subaru Impreza WRX", "static/images/subaru_impreza.jpg", "Rally Edition Turbo", 3200000, end_time),
            ("Land Cruiser V8", "static/images/landcruiser_v8.jpg", "Luxury Offroader", 10800000, end_time)
        ]
        c.executemany("INSERT INTO cars (name, image, description, base_price, end_time) VALUES (?,?,?,?,?)", cars)
        
        conn.commit()
        conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('database/cars.db')
    c = conn.cursor()
    c.execute("SELECT * FROM cars")
    cars = c.fetchall()
    conn.close()
    return render_template('index.html', cars=cars)

@app.route('/bid', methods=['POST'])
def bid():
    username = request.form['username']
    car_id = request.form['car_id']
    bid_amount = int(request.form['bid_amount'])

    conn = sqlite3.connect('database/cars.db')
    c = conn.cursor()

    # Create or fetch user
    c.execute("SELECT id FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    if not user:
        c.execute("INSERT INTO users (username) VALUES (?)", (username,))
        conn.commit()
        user_id = c.lastrowid
    else:
        user_id = user[0]

    # Check if user has already bid on this car
    c.execute("SELECT * FROM bids WHERE user_id = ? AND car_id = ?", (user_id, car_id))
    if c.fetchone():
        conn.close()
        return jsonify({"error": "You have already placed a bid for this car."})

    # Check if bidding is still open
    c.execute("SELECT end_time FROM cars WHERE id = ?", (car_id,))
    end_time = datetime.strptime(c.fetchone()[0], "%Y-%m-%d %H:%M:%S")
    if datetime.now() > end_time:
        conn.close()
        return jsonify({"error": "Bidding has ended for this car."})

    # Insert bid
    c.execute("INSERT INTO bids (user_id, car_id, amount, timestamp) VALUES (?,?,?,?)",
              (user_id, car_id, bid_amount, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return jsonify({"success": True})

@app.route('/bids/<int:car_id>')
def get_bids(car_id):
    conn = sqlite3.connect('database/cars.db')
    c = conn.cursor()
    c.execute("SELECT COUNT(DISTINCT user_id) FROM bids WHERE car_id = ?", (car_id,))
    num_bidders = c.fetchone()[0]

    c.execute("SELECT MAX(amount) FROM bids WHERE car_id = ?", (car_id,))
    highest_bid = c.fetchone()[0]
    conn.close()

    return jsonify({
        "num_bidders": num_bidders,
        "highest_bid": highest_bid if highest_bid else 0
    })

if __name__ == '__main__':
    init_db()
    app.run(debug=True)