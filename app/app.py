from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host="db",
        database="students",
        user="postgres",
        password="postgres"
    )
    return conn

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            age INTEGER,
            gender VARCHAR(10)
        );
    """)
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Databas initierad med tabellen 'students'.")

@app.route("/")
def home():
    return "Welcome to the Student Records API!"

@app.route("/students", methods=["GET"])
def get_students():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, age, gender FROM students;")
    students = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(students)

@app.route("/students", methods=["POST"])
def add_student():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO students (name, age, gender) VALUES (%s, %s, %s) RETURNING id;",
        (data["name"], data.get("age"), data.get("gender"))
    )
    student_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({
        "id": student_id,
        "name": data["name"],
        "age": data.get("age"),
        "gender": data.get("gender")
    }), 201

@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE id = %s RETURNING id;", (student_id,))
    deleted = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if deleted:
        return jsonify({"message": f"Student med ID {student_id} raderad."}), 200
    else:
        return jsonify({"error": f"Student med ID {student_id} finns inte."}), 404

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
