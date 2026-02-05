# =============================================================================
# Part 4: User Login
# =============================================================================

from flask import Flask, render_template, request, jsonify
from models import db, User, init_db
from auth import hash_password, verify_password, create_token
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_db(app)


# =============================================================================
# PAGE ROUTES
# =============================================================================

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/register')
def register_page():
    return render_template('register.html')


@app.route('/login')
def login_page():
    return render_template('login.html')


@app.route('/dashboard')
def dashboard_page():
    return render_template('dashboard.html')


# =============================================================================
# API ROUTES
# =============================================================================

@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json()  # Get JSON from request body

    if not data:
        return jsonify({'error': 'No data provided'}), 400  # 400 = Bad Request

    username = data.get('username')  # .get() returns None if key missing
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'error': 'All fields are required'}), 400

    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400

    if User.query.filter_by(email=email).first():  # Check if email exists
        return jsonify({'error': 'Email already registered'}), 400

    if User.query.filter_by(username=username).first():  # Check if username exists
        return jsonify({'error': 'Username already taken'}), 400

    new_user = User(
        username=username,
        email=email,
        password_hash=hash_password(password)  # "secret" -> "pbkdf2:sha256:..."
    )

    db.session.add(new_user)  # Add to session
    db.session.commit()  # Save to database

    return jsonify({'message': 'Registration successful!'}), 201  # 201 = Created


@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    email = data.get('email')
    password = data.get('password')
    remember_me = data.get('remember_me', False)

    # ACTIVITY 4: Login attempt logging
    print(f"\n{'='*50}")
    print("LOGIN ATTEMPT")
    print(f"{'='*50}")
    print(f"Time: {datetime.now()}")
    print(f"Email: {email}")
    print(f"Remember me: {remember_me}")

    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400

    user = User.query.filter_by(email=email).first()  # Find user by email

    if not user or not verify_password(user.password_hash, password):  # Check password
        return jsonify({'error': 'Invalid email or password'}), 401  # 401 = Unauthorized

     # ACTIVITY 3: Determine token expiration based on remember_me
    if remember_me:
        token_expiration_hours = 24 * 30  # 30 days = 720 hours
        expiration_description = "30 days"
    else:
        token_expiration_hours = 1  # 1 hour
        expiration_description = "1 hour"

    token = create_token(user.id, user.is_admin,token_expiration_hours)  # Create JWT token

    # ACTIVITY 4: Log success
    print(f"Status: SUCCESS")
    print(f"User ID: {user.id}")
    print(f"Username: {user.username}")
    print(f"Token expiration: {expiration_description}")
    print(f"{'='*50}")

    return jsonify({
        'message': 'Login successful!',
        'token': token,  # Frontend stores this in localStorage
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'is_admin': user.is_admin
        }
    }), 200


# =============================================================================
# RUN THE SERVER
# =============================================================================
if __name__ == '__main__':
    print("\n" + "="*50)
    print("  Part 4: User Login")
    print("  Open: http://127.0.0.1:5000")
    print("="*50 + "\n")
    app.run(debug=True)
