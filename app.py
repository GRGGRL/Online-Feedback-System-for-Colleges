from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
    conn.close()
    if user and check_password_hash(user['password'], password):
        session['user_id'] = user['id']
        session['role'] = user['role']
        return redirect(url_for('feedback')) if user['role'] == 'student' else redirect(url_for('admin'))
    return 'Invalid credentials'

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        role = 'student'
        conn = get_db()
        conn.execute('INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)',
                     (name, email, password, role))
        conn.commit()
        conn.close()
        return redirect(url_for('home'))
    return render_template('register.html')

@app.route('/about_college')
def about_college():
    return render_template('about_college.html')

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        subject = request.form['subject']
        rating = request.form['rating']
        comments = request.form['comments']
        student_id = session['user_id']
        conn = get_db()
        conn.execute('INSERT INTO feedback (student_id, subject, rating, comments) VALUES (?, ?, ?, ?)',
                     (student_id, subject, rating, comments))
        conn.commit()
        conn.close()
        return render_template('thankyou.html')
    return render_template('feedback_form.html')

@app.route('/admin')
def admin():
    conn = get_db()
    feedbacks = conn.execute('SELECT f.*, u.name FROM feedback f JOIN users u ON f.student_id = u.id').fetchall()
    conn.close()
    return render_template('report.html', feedbacks=feedbacks)

if __name__ == '__main__':
    app.run(debug=True)
