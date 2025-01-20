from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/register', methods= ['POST'])
def register():
    try:
        # Debug log to check received data
        print("Received JSON:", request.json)
    except:
        return({'message': 'An error occurred during registration'}),500
    

    return 'User Registered'

if __name__ == '__main__':
    app.run(debug=True)