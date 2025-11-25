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