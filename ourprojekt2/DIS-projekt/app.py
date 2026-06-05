import re
import psycopg2
from flask import Flask, render_template, request

app = Flask(__name__)

# Database configuration
DB_CONFIG = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "Dyn49pgh",
    "host": "localhost",
    "port": "5432"
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST']) 
def calculate():
    u_gender = request.form.get('gender', '')
    u_age = request.form.get('age', '')
    u_study = request.form.get('studying', '0')
    u_gaming = request.form.get('gaming', '0')
    u_sleep = request.form.get('sleeping', '0')

    # REGULAR EXPRESSION MATCHING  
    if not re.match(r"^(Male|Female|Other)$", u_gender):
        return render_template('index.html', result="Invalid Gender Selection.")

    if not re.match(r"^(1[6-9]|2[0-5])$", u_age):
        return render_template('index.html', result="Age must be between 16 and 25.")

    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        # RELATIONAL CALCULUS (Declarative)
        # This SQL string represents Tuple Relational Calculus. It describes 
        # "WHAT" data is needed (the AVG of grades for specific tuples) 
        # without defining the procedural steps.
        # UPDATED: 'age' now uses BETWEEN for a broader comparison.
        query = """
            SELECT AVG(grades), STDDEV(grades), COUNT(*)
            FROM public.gaming_academic_performance 
            WHERE gender = %s 
            AND age BETWEEN %s AND %s
            AND study_hours BETWEEN %s AND %s
            AND gaming_hours BETWEEN %s AND %s
            AND sleep_hours BETWEEN %s AND %s
            AND grades <= 100
        """

        # Logic to expand range while keeping age within 16-25
        age_val = int(u_age)
        age_min = max(16, age_val - 2)
        age_max = min(25, age_val + 2)

        # UPDATED: Ranges for hours increased to +/- 3.0 for a larger comparison set.
        params = (
            u_gender, 
            age_min, age_max,
            float(u_study) - 3.0, float(u_study) + 3.0,
            float(u_gaming) - 3.0, float(u_gaming) + 3.0,
            float(u_sleep) - 3.0, float(u_sleep) + 3.0
        )
        
        # RELATIONAL ALGEBRA (Procedural)
        # When cur.execute(query) is called, the database engine translates the 
        # calculus into Relational Algebra operations:
        # 1. Selection (σ): Filtering rows based on the WHERE conditions.
        # 2. Projection (π): Narrowing the data to the 'grades' column.
        # 3. Aggregation: Computing the AVG, STDDEV, and COUNT.
        cur.execute(query, params)
        row = cur.fetchone()
        cur.close()
        conn.close()

        if row and row[0] is not None:
            avg_grade = float(row[0])
            std_dev = float(row[1]) if row[1] else 5.0
            student_count = row[2]
            
            return render_template('index.html', 
                                   result=f"Average grade: {avg_grade:.2f}%",
                                   student_count=student_count,
                                   chart_mean=avg_grade,
                                   chart_std=std_dev)
        else:
            return render_template('index.html', result="No matching records found for this combination.")

    except Exception as e:
        return render_template('index.html', result=f"Database error: {str(e)}")

@app.route('/delete_all', methods=['POST'])
def delete_all():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        # SQL INTERACTION (DELETE)
        cur.execute("DELETE FROM public.gaming_academic_performance;")
        conn.commit()
        cur.close()
        conn.close()
        message = "All records deleted."
    except Exception as e:
        message = f"Error: {str(e)}"
    return render_template('index.html', result=message)  

if __name__ == '__main__':
    app.run(debug=True)