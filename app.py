from flask import Flask, jsonify, request
import mysql.connector
import os
from dotenv import load_dotenv

app = Flask(__name__)


def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "mysql"),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE", "new_db")
    )

def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        create table if not exists users (
            id int auto_increment primary key,
            name varchar(100)
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

create_table()

@app.route('/')
def hello():
    return "Hello! Docker!"

@app.route('/api/users', methods=['POST'])
def add_user():
    data = request.get_json()
    name = data.get('name')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (name) values (%s)', (name, ))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "User added successfully!!"}), 201

@app.route('/api/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(users)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)