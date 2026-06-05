import re
import psycopg2
from flask import Flask, render_template, request 

app = Flask(__name__)


DB_CONFIG = {

    "dbname": "postgres",
    "user": "postgres",
    "password": "Use your actual password here",
    "host": "localhost",
    "port": "5432"
}

@app.route("/")
def boxes():
    return render_template("boxes.html")

@app.route("/calculate", methods=["POST"])
def calculate():
    gender = request.form.get("gender", "")
    age = request.form.get("age", "")
    study = request.form.get("studying") 
    gaming = request.form.get("gaming")
    sleep = request.form.get("sleeping")

    age_val = int(age)
    study_val = float(study)
    gaming_val = float(gaming)
    sleep_val = float(sleep)


    if not re.match(r"^(Male|Female|Other)$", gender):
        return render_template("boxes.html", result="Invalid Gender")
    
    if not re.match(r"\d+", age):
        return render_template("boxes.html", result="Invalid Age")
    
    if not re.match(r"^\d+(\.\d+)?$", study):
        return render_template("boxes.html", result="Invalid hours")
    
    if not re.match(r"^\d+(\.\d+)?$", gaming):
        return render_template("boxes.html", result="Invalid hours")
    
    if not re.match(r"^\d+(\.\d+)?$", sleep):
        return render_template("boxes.html", result="Invalid hours")

    try: 
        connect = psycopg2.connect(**DB_CONFIG)
        cur = connect.cursor()

        query = """
            SELECT AVG(grades), COUNT(*)  
            FROM public.gaming_academic_performance

            WHERE gender = %s
            AND age BETWEEN %s AND %s
            AND study_hours BETWEEN %s AND %s
            AND gaming_hours BETWEEN %s AND %s
            AND sleep_hours BETWEEN %s AND %s
            AND grades <= 100
        """


        age_val = int(age)
        age_min = max(16, age_val - 2)
        age_max = min(25, age_val + 2)

        parameters = (
            gender, age_min, age_max,

            study_val - 3.0, study_val + 3.0, 
            gaming_val - 3.0, gaming_val + 3.0,
            sleep_val - 3.0, sleep_val + 3.0
        )

        cur.execute(query, parameters) 
        row = cur.fetchone()
        cur.close()
        connect.close()

        if row and row[0] is not None:
            avg_grade = float(row[0])
            student_count = row[1]
            
            return render_template("boxes.html",
                result=f"Average grade: {avg_grade:.2f}%", 
                student_count=student_count
            )
        else:
            return render_template("boxes.html", result="No matching")
        
    except Exception as e:
        return render_template("boxes.html", result=f"Database error: {str(e)}")
    
if __name__ == "__main__":
    app.run(debug=True)