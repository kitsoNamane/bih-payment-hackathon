from datetime import datetime, timedelta 
from functools import wraps
from flask import Flask, request, jsonify
import jwt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

# Decorator for JWT authentication
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Check if 'Authorization' header is present
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            token = auth_header.split(' ')[1] if len(auth_header.split(' ')) > 1 else None

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            # Verify and decode the token
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = data['username']

        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401

        # Pass the authenticated user to the decorated function
        return f(current_user, *args, **kwargs)

    return decorated

# Login endpoint
@app.route('/login', methods=['POST'])
def login():
    # Get username and password from the request
    username = request.json.get('username')
    password = request.json.get('password')

    # Perform authentication logic here (e.g., check credentials against database)
    # ...

    # Set expiration time for the token (e.g., 1 day from the current time)
    expires = datetime.utcnow() + timedelta(hours=1)

    # Generate JWT token
    token = jwt.encode({'username': username,'exp':expires}, app.config['SECRET_KEY'])

    # Return the token as a response
    return jsonify({'token': token})

# Account creation endpoint
@app.route('/create_account', methods=['POST'])
def create_account():
    # Get account details from the request
    email = request.json.get('email')
    password = request.json.get('password')
    phone = request.json.get('phone')
    omang = request.json.get('omang')

    # Perform validation on the received data
    if not email or not password or not phone or not omang:
        return jsonify({'message': 'Missing required fields!'}), 400

    # Perform account creation logic here
    # ...

    # Return a success message
    return jsonify({'message': 'Account created successfully!'})



# Protected route example
@app.route('/protected', methods=['GET'])
@token_required
def protected(current_user):
    return jsonify({'message': 'This is a protected route!', 'current_user': current_user})

# Run the Flask application
if __name__ == '__main__':
    app.run()
