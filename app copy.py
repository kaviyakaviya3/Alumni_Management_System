from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = "secret"

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Kaviya@321'
app.config['MYSQL_DB'] = 'alumni'

mysql = MySQL(app)

# Home
@app.route('/')
def home():
    return redirect('/dashboard')

# Dashboard
@app.route('/dashboard')
def dashboard():

    cursor = mysql.connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM jobs")
    total_jobs = cursor.fetchone()[0]

    cursor.close()

    return render_template(
        "alumni_dashboard.html",
        total_jobs=total_jobs
    )

# Add Job
@app.route('/add_job', methods=['GET', 'POST'])
def add_job():

    if request.method == 'POST':

        company = request.form['company_name']
        role = request.form['job_role']
        location = request.form['location']
        salary = request.form['salary']
        apply_link = request.form['apply_link']
        description = request.form['description']

        cursor = mysql.connection.cursor()

        cursor.execute("""
        INSERT INTO jobs(company_name, job_role, location, salary, apply_link, description, posted_by)
        VALUES(%s,%s,%s,%s,%s,%s,%s)
        """, (
            company,
            role,
            location,
            salary,
            apply_link,
            description,
            "alumni"
        ))

        mysql.connection.commit()
        cursor.close()

        return redirect('/jobs')

    return render_template("add_job.html")

# View Jobs
@app.route('/jobs')
def jobs():

    cursor = mysql.connection.cursor()

    cursor.execute("SELECT * FROM jobs ORDER BY posted_date DESC")

    data = cursor.fetchall()

    cursor.close()

    return render_template("jobs.html", jobs=data)

# Run
if __name__ == "__main__":
    app.run(debug=True)