from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
import sqlite3
import json
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'sonavane-hospital-2024'
DB_PATH = 'sonavane.db'

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    db = get_db()
    db.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT NOT NULL,
            email         TEXT UNIQUE NOT NULL,
            phone         TEXT,
            age           INTEGER,
            gender        TEXT,
            address       TEXT,
            password_hash TEXT NOT NULL,
            created_at    DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS doctors (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            name           TEXT NOT NULL,
            specialization TEXT NOT NULL,
            qualification  TEXT,
            experience     TEXT,
            available_days TEXT,
            timing         TEXT,
            image_url      TEXT,
            available      INTEGER DEFAULT 1
        );
        CREATE TABLE IF NOT EXISTS appointments (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id    INTEGER,
            doctor_id  INTEGER,
            patient_name TEXT NOT NULL,
            phone      TEXT NOT NULL,
            age        INTEGER,
            gender     TEXT,
            date       TEXT NOT NULL,
            time_slot  TEXT NOT NULL,
            problem    TEXT,
            status     TEXT DEFAULT "pending",
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(doctor_id) REFERENCES doctors(id)
        );
        CREATE TABLE IF NOT EXISTS admins (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            username      TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        );
    ''')

    # Seed doctors
    count = db.execute('SELECT COUNT(*) FROM doctors').fetchone()[0]
    if count == 0:
        doctors = [
            ('Dr. Rajesh Sonavane',    'Orthopedic Surgeon',       'MS Orthopedics, MBBS', '20+ Years', 'Mon, Wed, Fri', '10:00 AM - 2:00 PM', '/static/images/doctor1.jpg'),
            ('Dr. Priya Sharma',       'Joint Replacement Surgeon', 'MS Orthopedics, MBBS', '15+ Years', 'Tue, Thu, Sat', '11:00 AM - 3:00 PM', '/static/images/doctor2.jpg'),
            ('Dr. Amit Kulkarni',      'Spine Specialist',          'MCh Spine Surgery',    '12+ Years', 'Mon, Tue, Thu', '9:00 AM - 1:00 PM',  '/static/images/doctor3.jpg'),
            ('Dr. Sunita Deshmukh',    'Sports Medicine',           'MS Orthopedics, MBBS', '10+ Years', 'Wed, Fri, Sat', '2:00 PM - 6:00 PM',  '/static/images/doctor4.jpg'),
        ]
        db.executemany('INSERT INTO doctors (name,specialization,qualification,experience,available_days,timing,image_url) VALUES (?,?,?,?,?,?,?)', doctors)

    # Seed admin
    admin_count = db.execute('SELECT COUNT(*) FROM admins').fetchone()[0]
    if admin_count == 0:
        db.execute('INSERT INTO admins (username, password_hash) VALUES (?,?)',
                   ('admin', generate_password_hash('admin123')))

    db.commit()
    db.close()

# ── PATIENT ROUTES ────────────────────────────────────────────────────────────
@app.route('/')
def index():
    db      = get_db()
    doctors = db.execute('SELECT * FROM doctors WHERE available=1').fetchall()
    db.close()
    return render_template('index.html', doctors=doctors)

@app.route('/doctors')
def doctors():
    db      = get_db()
    doctors = db.execute('SELECT * FROM doctors WHERE available=1').fetchall()
    db.close()
    return render_template('doctors.html', doctors=doctors)

@app.route('/book', methods=['GET', 'POST'])
def book():
    if 'user_id' not in session:
        flash('Please login to book an appointment.')
        return redirect(url_for('login'))
    db      = get_db()
    doctors = db.execute('SELECT * FROM doctors WHERE available=1').fetchall()
    user    = db.execute('SELECT * FROM users WHERE id=?', (session['user_id'],)).fetchone()
    db.close()
    if request.method == 'POST':
        data = request.get_json()
        db   = get_db()
        db.execute(
            'INSERT INTO appointments (user_id,doctor_id,patient_name,phone,age,gender,date,time_slot,problem) VALUES (?,?,?,?,?,?,?,?,?)',
            (session['user_id'], data['doctor_id'], data['patient_name'], data['phone'],
             data['age'], data['gender'], data['date'], data['time_slot'], data.get('problem',''))
        )
        db.commit()
        db.close()
        return jsonify({'success': True})
    return render_template('book.html', doctors=doctors, user=user)

@app.route('/my-appointments')
def my_appointments():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    db = get_db()
    appointments = db.execute('''
        SELECT a.*, d.name as doctor_name, d.specialization
        FROM appointments a
        JOIN doctors d ON a.doctor_id = d.id
        WHERE a.user_id = ?
        ORDER BY a.created_at DESC
    ''', (session['user_id'],)).fetchall()
    db.close()
    return render_template('my_appointments.html', appointments=appointments)

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/skeleton')
def skeleton():
    return render_template('skeleton.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email    = request.form['email']
        password = request.form['password']
        db   = get_db()
        user = db.execute('SELECT * FROM users WHERE email=?', (email,)).fetchone()
        db.close()
        if user and check_password_hash(user['password_hash'], password):
            session['user_id']   = user['id']
            session['user_name'] = user['name']
            return redirect(url_for('index'))
        flash('Invalid email or password.')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name     = request.form['name']
        email    = request.form['email']
        phone    = request.form.get('phone','')
        age      = request.form.get('age','')
        gender   = request.form.get('gender','')
        password = generate_password_hash(request.form['password'])
        try:
            db = get_db()
            db.execute('INSERT INTO users (name,email,phone,age,gender,password_hash) VALUES (?,?,?,?,?,?)',
                       (name, email, phone, age, gender, password))
            db.commit()
            db.close()
            flash('Account created! Please log in.')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Email already registered.')
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# ── ADMIN ROUTES ──────────────────────────────────────────────────────────────
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db    = get_db()
        admin = db.execute('SELECT * FROM admins WHERE username=?', (username,)).fetchone()
        db.close()
        if admin and check_password_hash(admin['password_hash'], password):
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        flash('Invalid credentials.')
    return render_template('admin_login.html')

@app.route('/admin')
def admin_dashboard():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    db = get_db()
    total_appointments = db.execute('SELECT COUNT(*) FROM appointments').fetchone()[0]
    pending            = db.execute('SELECT COUNT(*) FROM appointments WHERE status="pending"').fetchone()[0]
    confirmed          = db.execute('SELECT COUNT(*) FROM appointments WHERE status="confirmed"').fetchone()[0]
    total_patients     = db.execute('SELECT COUNT(*) FROM users').fetchone()[0]
    appointments = db.execute('''
        SELECT a.*, d.name as doctor_name, d.specialization
        FROM appointments a JOIN doctors d ON a.doctor_id=d.id
        ORDER BY a.created_at DESC
    ''').fetchall()
    doctors = db.execute('SELECT * FROM doctors').fetchall()
    db.close()
    return render_template('admin_dashboard.html',
        total_appointments=total_appointments, pending=pending,
        confirmed=confirmed, total_patients=total_patients,
        appointments=appointments, doctors=doctors)

@app.route('/admin/appointment/<int:aid>/status', methods=['POST'])
def update_status(aid):
    if not session.get('admin'):
        return jsonify({'error': 'Unauthorized'}), 401
    data = request.get_json()
    db   = get_db()
    db.execute('UPDATE appointments SET status=? WHERE id=?', (data['status'], aid))
    db.commit()
    db.close()
    return jsonify({'success': True})

@app.route('/admin/doctor/add', methods=['POST'])
def add_doctor():
    if not session.get('admin'):
        return jsonify({'error': 'Unauthorized'}), 401
    data = request.get_json()
    db   = get_db()
    db.execute('INSERT INTO doctors (name,specialization,qualification,experience,available_days,timing,image_url) VALUES (?,?,?,?,?,?,?)',
               (data['name'], data['specialization'], data.get('qualification',''), data.get('experience',''),
                data.get('available_days',''), data.get('timing',''), '/static/images/doctor1.jpg'))
    db.commit()
    db.close()
    return jsonify({'success': True})

@app.route('/admin/doctor/<int:did>/delete', methods=['POST'])
def delete_doctor(did):
    if not session.get('admin'):
        return jsonify({'error': 'Unauthorized'}), 401
    db = get_db()
    db.execute('UPDATE doctors SET available=0 WHERE id=?', (did,))
    db.commit()
    db.close()
    return jsonify({'success': True})

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('admin_login'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
