from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect("tasks.db")
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            completed INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def index():
    conn = get_db_connection()
    tasks = conn.execute("SELECT * FROM tasks ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add_task():
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()

    if title:
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO tasks (title, description) VALUES (?, ?)",
            (title, description)
        )
        conn.commit()
        conn.close()

    return redirect(url_for("index"))

@app.route("/toggle/<int:task_id>", methods=["POST"])
def toggle_task(task_id):
    conn = get_db_connection()
    conn.execute("""
        UPDATE tasks
        SET completed = CASE WHEN completed = 0 THEN 1 ELSE 0 END
        WHERE id = ?
    """, (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    create_table()
    app.run(debug=True)
