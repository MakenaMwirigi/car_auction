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

