import re
import psycopg2
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

DB_CONFIG = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "you should use actual password",
    "host": "localhost",
    "port": "5432"
}

@app.route("/")
def boxes():
    return render_template("index.html")

@app.route("/calculate", methods=["POST"])
def calculate():
    gender = request.form.get("gender", "")
    age = request.form.get("age", "")
    study = request.form.get("studying", "")
    gaming = request.form.get("gaming", "")
    sleep = request.form.get("sleeping", "")

    gender_pattern = r"^(Male|Female|Other)$"
    age_pattern = r"^(1[6-9]|2[0-5])$"
    hour_pattern = r"^(10(\.0)?|[0-9](\.[0-9])?)$"

    if not re.match(gender_pattern, gender):
        return redirect(url_for("boxes", result="Invalid Gender"))

    if not re.match(age_pattern, age):
        return redirect(url_for("boxes", result="Invalid Age"))

    if not re.match(hour_pattern, study):
        return redirect(url_for("boxes", result="Invalid studying hours"))

    if not re.match(hour_pattern, gaming):
        return redirect(url_for("boxes", result="Invalid gaming hours"))

    if not re.match(hour_pattern, sleep):
        return redirect(url_for("boxes", result="Invalid sleeping hours"))

    age_val = int(age)
    study_val = float(study)
    gaming_val = float(gaming)
    sleep_val = float(sleep)

    age_min = max(16, age_val - 2)
    age_max = min(25, age_val + 2)

    try:
        connect = psycopg2.connect(**DB_CONFIG)
        cur = connect.cursor()

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
            std_dev = float(row[1]) if row[1] else 5.0
            student_count = row[2]

            return redirect(url_for(
                "boxes",
                result=f"Average grade: {avg_grade:.2f}%",
                student_count=student_count,
                chart_mean=f"{avg_grade:.2f}",
                chart_std=f"{std_dev:.2f}"
            ))

        return redirect(url_for("boxes", result="No matching students found"))

    except Exception as e:
        return redirect(url_for("boxes", result=f"Database error: {str(e)}"))

if __name__ == "__main__":
    app.run(debug=True)