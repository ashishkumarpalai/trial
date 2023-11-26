import os

from flask import Flask, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'ashish'
app.config['MYSQL_DB'] = 'giapratice'
mysql = MySQL(app)


@app.route('/')
def home():
    # return 'Welcome to my Flask app!'
    return '<h1 style="color:blue;text-align:center">Welcome to sql Backend!</h1>'
# Create a new user
@app.route('/users', methods=['POST'])
def create_user():
    name = request.json['name']
    email = request.json['email']

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO Customers (name, email) VALUES (%s, %s)", (name, email))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'User created successfully'})

# Read all users
@app.route('/users', methods=['GET'])
def get_users():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    cur.close()

    users = []
    for row in rows:
        user = {'id': row[0], 'name': row[1], 'email': row[2]}
        users.append(user)

    return jsonify(users)

# Read a specific user
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    row = cur.fetchone()
    cur.close()

    if row:
        user = {'id': row[0], 'name': row[1], 'email': row[2]}
        return jsonify(user)
    else:
        return jsonify({'message': 'User not found'})

# Update a user
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    name = request.json['name']
    email = request.json['email']

    cur = mysql.connection.cursor()
    cur.execute("UPDATE users SET name = %s, email = %s WHERE id = %s", (name, email, user_id))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'User updated successfully'})

# Delete a user
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'User deleted successfully'})

# if __name__ == '__main__':
#     app.run()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)