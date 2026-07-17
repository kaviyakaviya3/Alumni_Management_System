from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "alumni_project_2026"

# MySQL Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Kaviya@321",
    database="alumni_db"
)
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        if username == "admin" and password == "admin123":
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template(
                'admin_login.html',
                error="Invalid Username or Password"
            )

    return render_template('admin_login.html')
# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("index.html")


# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        cursor = db.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=%s AND password=%s",
            (email, password)
        )

        user = cursor.fetchone()
        cursor.close()

        if user:

            session["email"] = email

            if user[4] == "student":
                return redirect(url_for("student_dashboard"))

            elif user[4] == "alumni":
                return redirect(url_for("alumni_dashboard"))

            elif user[4] == "admin":
                return redirect(url_for("admin_dashboard"))

            else:
                return "Invalid Role"

        return "Invalid Email or Password"

    return render_template("login.html")

# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        department = request.form["department"]
        batch = request.form["batch"]
        password = request.form["password"]
        role = request.form["role"]

        cursor = db.cursor()

        if role == "student":

            cursor.execute("""
                INSERT INTO students
                (name, email, password, department, batch)
                VALUES (%s, %s, %s, %s, %s)
            """, (name, email, password, department, batch))

        else:

            cursor.execute("""
                INSERT INTO users
                (name, email, password, role, department, batch)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (name, email, password, "alumni", department, batch))

        db.commit()
        cursor.close()

        return "Registration Successful!"

    return render_template("register.html")
   

# ---------------- ALUMNI DASHBOARD ----------------
@app.route("/alumni_dashboard")
def alumni_dashboard():

    if "email" not in session:
        return redirect(url_for("login"))

    return render_template("alumni_dashboard.html")


# ---------------- MY PROFILE ----------------
@app.route('/profile')
def profile():

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Kaviya@321",
        database="alumni_db"
    )

    cur = conn.cursor()

    cur.execute("""
        SELECT name,email,department,batch,role
        FROM users
        WHERE email='kaviyakaviya3315@gmail.com'
    """)

    user = cur.fetchone()

    cur.close()
    conn.close()

    return render_template("profile.html", user=user)


# ---------------- ALUMNI SEARCH ----------------
@app.route('/alumni_search')
def alumni_search():

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT name,email,department,batch 
        FROM users
    """)

    alumni = cur.fetchall()

    cur.close()

    return render_template(
        'alumni_search.html',
        alumni=alumni
    )

# ---------------- JOBS ----------------
@app.route("/jobs")
def jobs():

    if "email" not in session:
        return redirect(url_for("login"))

    cursor = db.cursor()

    cursor.execute("SELECT * FROM jobs")

    jobs = cursor.fetchall()

    cursor.close()

    return render_template("jobs.html", jobs=jobs)


# ---------------- ADD JOB ----------------
@app.route("/add_job", methods=["GET", "POST"])
def add_job():

    if "email" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        company = request.form["company_name"]
        role = request.form["job_role"]
        location = request.form["location"]
        salary = request.form["salary"]
        apply_link = request.form["apply_link"]
        description = request.form["description"]

        cursor = db.cursor()

        cursor.execute("""
        INSERT INTO jobs
        (company_name, job_role, location, salary, apply_link, description, posted_by)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
        """, (
            company,
            role,
            location,
            salary,
            apply_link,
            description,
            session["email"]
        ))

        db.commit()
        cursor.close()

        return redirect(url_for("jobs"))

    return render_template("add_job.html")
# ---------------- EVENTS ----------------
@app.route('/events')
def events():

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Kaviya@321",
        database="alumni_db"
    )

    cur = conn.cursor()

    cur.execute("""
        SELECT title, event_date, event_time, venue, description
        FROM events
    """)

    events = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("events.html", events=events)

# ---------------- ADD EVENT ----------------------#      
@app.route('/add_event', methods=['GET','POST'])
def add_event():

    if request.method == 'POST':

        title = request.form['title']
        description = request.form['description']
        event_date = request.form['event_date']
        event_time = request.form['event_time']
        venue = request.form['venue']


        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Kaviya@321",
            database="alumni_db"
        )

        cur = conn.cursor()

        cur.execute("""
            INSERT INTO events
            (title, description, event_date, event_time, venue)
            VALUES (%s,%s,%s,%s,%s)
        """,
        (title, description, event_date, event_time, venue))


        conn.commit()

        cur.close()
        conn.close()

        return redirect('/events')


    return render_template("add_event.html")
    
# ---------------- ADMIN DASHBOARD -----------------
@app.route('/admin_dashboard')
def admin_dashboard():

    cur = db.cursor()

    cur.execute("SELECT COUNT(*) FROM users")
    total_students = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM users")
    total_alumni = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM jobs")
    total_jobs = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM events")
    total_events = cur.fetchone()[0]

    cur.close()

    return render_template(
        "admin_dashboard.html",
        total_students=total_students,
        total_alumni=total_alumni,
        total_jobs=total_jobs,
        total_events=total_events
    )
@app.route('/manage_alumni')
def manage_alumni():

    cur = db.cursor()

    cur.execute("SELECT * FROM users")

    alumni = cur.fetchall()

    cur.close()

    return render_template('manage_alumni.html', alumni=alumni)
@app.route('/delete_alumni/<int:id>')
def delete_alumni(id):

    cur = db.cursor()

    cur.execute("DELETE FROM users WHERE id=%s", (id,))

    db.commit()

    cur.close()

    return redirect(url_for('manage_alumni'))
@app.route('/manage_students')
def manage_students():

    cur = db.cursor()

    cur.execute("SELECT * FROM students")

    students = cur.fetchall()

    cur.close()

    return render_template("manage_students.html", students=students)
@app.route('/delete_student/<int:id>')
def delete_student(id):

    cur = mysql.connection.cursor()

    cur.execute("DELETE FROM users WHERE id=%s",(id,))

    mysql.connection.commit()

    cur.close()

    return redirect('/manage_students')
@app.route('/manage_jobs')
def manage_jobs():

    cur = db.cursor()

    cur.execute("SELECT * FROM jobs")

    jobs = cur.fetchall()

    cur.close()

    return render_template('manage_jobs.html', jobs=jobs)
@app.route('/delete_job/<int:id>')
def delete_job(id):

    cur = db.cursor()

    cur.execute("DELETE FROM jobs WHERE id=%s", (id,))

    db.commit()

    cur.close()

    return redirect(url_for('manage_jobs'))
@app.route('/manage_events')
def manage_events():

    cur = db.cursor()

    cur.execute("SELECT * FROM events")

    events = cur.fetchall()

    cur.close()

    return render_template('manage_events.html', events=events)
@app.route('/delete_event/<int:id>')
def delete_event(id):

    cur = db.cursor()

    cur.execute("DELETE FROM events WHERE id=%s", (id,))

    db.commit()

    cur.close()

    return redirect(url_for('manage_events'))
# ---------------- STUDENT DASHBOARD ----------------
@app.route("/student_dashboard")
def student_dashboard():

    if "email" not in session:
        return redirect(url_for("login"))

    cursor = db.cursor()

    cursor.execute("SELECT COUNT(*) FROM users")
    total_alumni = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM jobs")
    total_jobs = cursor.fetchone()[0]

    cursor.close()

    return render_template(
        "student_dashboard.html",
        total_alumni=total_alumni,
        total_jobs=total_jobs
    )
@app.route('/search')
def search():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Kaviya@321",
        database="alumni_db"
    )

    cur = conn.cursor()

    cur.execute("""
        SELECT name,email,department,batch
        FROM users
        WHERE role='alumni'
    """)

    alumni = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("search.html", alumni=alumni)
    


    
# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)