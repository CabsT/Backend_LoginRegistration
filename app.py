from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'your_secret_key'
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

         # Check for duplicates
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email is already registered.'}), 400
        if User.query.filter_by(phone=phone).first():
            return jsonify({'error': 'Phone number is already registered.'}), 400

        # Save the user to the database
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'Registered successfully'}), 200

    except Exception as e:
        return jsonify({'error': 'Registration failed. Please try again'}),500
    

    
# Login route
@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    
    try:
        # Find the user by email
        user = User.query.filter_by(email=email).first()
        if user:
            # If user is found, check if the password matches
            if bcrypt.check_password_hash(user.password, password):
                # Password matches
                session['user_id'] = user.id
                return jsonify({'message': 'Successfully logged in.'}), 201
            elif not bcrypt.check_password_hash(user.password, password):
                # Password doesn't match
                return jsonify({"message": "Incorrect password."}), 401
     
    except Exception as e:
        # User not found
        return jsonify({'error': 'User not registered.'}), 404
       
if __name__ == '__main__':
    with app.app_context():  # Set up the application context
        db.create_all()  # Create tables if they don't exist
    app.run(debug=True)