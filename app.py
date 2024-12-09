from flask import Flask, render_template, request 
import pg8000
app = Flask( __name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get the level from the form
        level = request.form["level"]
        return render_template("timetable.html", level=level, data=[], message="Loading timetable...")
    
    return render_template("index.html")

@app.route("/timetable", methods=["GET"])
def timetable():
    level = request.args.get('level') 
    if not level:
        # Get level from the query parameters
        return "Level not provided", 400
    
    # Connect to the PostgreSQL database
    conn = pg8000.connect(
        user="Damir",
        password="1234",
        host="localhost",
        port=5432,
        database="Damir"
    )

    cur = conn.cursor()
    query = "SELECT * FROM Timetable WHERE level = %s;"
    cur.execute(query, (level,))
    rows = cur.fetchall()

    # Pass data to the template
    if rows:
        return render_template("timetable.html", level=level, data=rows, message="")
    else:
        return render_template("timetable.html", level=level, data=[], message="No data found for this level.")
    
if __name__ == "__main__": 
    app.run(debug=True)