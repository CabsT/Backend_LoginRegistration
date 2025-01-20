from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

CORS(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

# Register route
@app.route('/register', methods= ['POST'])
def register():
    try:
        # Debug log to check received data
        print("Received JSON:", request.json)

        name = request.json.get('name')
        surname = request.json.get('surname')
        phone = request.json.get('phone')
        email = request.json.get('email')
        password = request.json.get('password')

        # Hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Create a new user instance
        new_user = User(
            name=name,
            surname=surname,
            phone=phone,
            email=email,
            password=hashed_password
        )

        # Save the user to the database
        db.session.add(new_user)
        db.session.commit()

        return '', 200

    except:
        return jsonify({'message': 'An error occurred during registration'}),500
    
if __name__ == '__main__':
    with app.app_context():  # Set up the application context
        db.create_all()  # Create tables if they don't exist
    app.run(debug=True)