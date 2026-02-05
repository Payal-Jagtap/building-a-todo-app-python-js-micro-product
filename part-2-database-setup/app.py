# =============================================================================
# Part 2: Database Setup
# =============================================================================
# Now we add a database to store data permanently.
# We will learn:
#   1. What is SQLAlchemy (database toolkit)
#   2. How to create database models (tables)
#   3. How to query the database
# =============================================================================

from flask import Flask, render_template
from models import db, User, Todo, init_db

app = Flask(__name__)

# Database configuration
# 'sqlite:///todo.db' creates a file called 'todo.db' in instance/ folder
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
init_db(app)


# =============================================================================
# ROUTES
# =============================================================================

@app.route('/')
def home():
    """Home page"""
    return render_template('index.html')


@app.route('/test-db')
def test_db():
    """
    Test route to verify database is working.
    Creates a test user and todo if they don't exist.
    """
    # Check if test user exists
    #user = User.query.filter_by(username='testuser').first()
    # Clear existing data for clean demonstration
    Todo.query.delete()
    User.query.delete()
    db.session.commit()
    
    # ACTIVITY 4: Create 3 users instead of 1
    print("\n" + "="*50)
    print("ACTIVITY 4: CREATING 3 USERS WITH DIFFERENT TODOS")
    print("="*50)
    
    # Create 3 test users
    user1 = User(username='alice', email='alice@example.com', password_hash='pass1')
    user2 = User(username='bob', email='bob@example.com', password_hash='pass2')
    user3 = User(username='charlie', email='charlie@example.com', password_hash='pass3')
    
    db.session.add_all([user1, user2, user3])
    db.session.commit()
    print("✓ Created 3 users: alice, bob, charlie")
    
    # ACTIVITY 4: Create different todos for each user
    # User 1 (alice) todos:
    todo1 = Todo(task_content='Buy groceries', user_id=user1.id)
    todo2 = Todo(task_content='Finish homework', user_id=user1.id)
    
    # User 2 (bob) todos:
    todo3 = Todo(task_content='Call mom', user_id=user2.id)
    todo4 = Todo(task_content='Pay bills', user_id=user2.id)
    todo5 = Todo(task_content='Go to gym', user_id=user2.id)
    
    # User 3 (charlie) todos:
    todo6 = Todo(task_content='Study Flask', user_id=user3.id)
    todo7 = Todo(task_content='Complete project', user_id=user3.id, is_completed=True)
    
    db.session.add_all([todo1, todo2, todo3, todo4, todo5, todo6, todo7])
    db.session.commit()
    print("✓ Created different todos for each user")
    print(f"  - alice: 2 todos")
    print(f"  - bob: 3 todos")
    print(f"  - charlie: 2 todos (1 completed)")
    print("="*50)

   # ============================================
    # ACTIVITY 2: QUERY PRACTICE
    # ============================================
    
    print("\n" + "="*50)
    print("ACTIVITY 2: QUERY PRACTICE")
    print("="*50)
    
    # Query 1: Get all users
    all_users = User.query.all()
    print(f"\n1. User.query.all()")
    print(f"   Result: {all_users}")
    print(f"   Number of users: {len(all_users)}")
    print(f"   Users created: {[user.username for user in all_users]}")

    # 2. User.query.first() - gets first user
    first_user = User.query.first()
    print(f"\n2. User.query.first()")
    print(f"   Result: {first_user}")
    print(f"   Username: {first_user.username}")


    # Query 3: Count users
    user_count = User.query.count()
    print(f"\n3. User.query.count()")
    print(f"   Result: {user_count}")
    print(f"   Total users: {user_count}")
    
    print("\n" + "="*50)
    all_todos = Todo.query.all()

    return render_template('test_db.html', users=all_users, todos=all_todos)


# =============================================================================
# RUN THE SERVER
# =============================================================================
if __name__ == '__main__':
    print("\n" + "="*50)
    print("  Part 2: Database Setup")
    print("  Open: http://127.0.0.1:5000")
    print("  Test DB: http://127.0.0.1:5000/test-db")
    print("="*50 + "\n")
    app.run(debug=True)


# ============================================
# SELF-STUDY QUESTIONS
# ============================================
# 1. What is SQLAlchemy and why do we use it?
# 2. What does db.Column(db.String(80)) mean?
# 3. What is the difference between db.session.add() and db.session.commit()?
# 4. What does filter_by() do? How is it different from get()?
# 5. What happens if you delete todo.db file and restart the app?
#
# ============================================
# ACTIVITIES - Try These!
# ============================================
# Activity 1: Add a new field
#   - In models.py, add 'phone' field to User model
#   - Delete todo.db file (so tables are recreated)
#   - Restart the app and check if it works
#
# Activity 2: Query practice
#   - In test_db route, try: User.query.all() (gets all users)
#   - Try: User.query.first() (gets first user)
#   - Try: User.query.count() (counts users)
#
# Activity 3: View database file
#   - Install "DB Browser for SQLite" software
#   - Open instance/todo.db file
#   - See the tables and data inside
#
# Activity 4: Add more test data
#   - Modify test_db() to create 3 users instead of 1
#   - Create different todos for each user
# ============================================
