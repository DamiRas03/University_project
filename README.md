# University project
My University project that I made using Docker. It shows table with courses.

# 1. Run following docker commands:
```Docker
docker pull postgres:latest

docker run --name your_database-db -e POSTGRES_USER=you -e POSTGRES_PASSWORD=password -d -p 5432:5432 postgres:latest

# This is just to check if container is running
docker ps

docker exec -it your_database-db psql -U you
```
# 2. Setup SQL database. This is just example of how I did it, you can set up your own database:
```SQL
CREATE TABLE Timetable (id SERIAL PRIMARY KEY, course_code VARCHAR(10), section VARCHAR(10), hours NUMERIC(3, 1), title VARCHAR(100), instructor VARCHAR(100), campus VARCHAR(100), building VARCHAR(50), room VARCHAR(10), days VARCHAR(10), time VARCHAR(20), start_date DATE, end_date DATE, type VARCHAR(20), level INT);

INSERT INTO Timetable (course_code, section, hours, title, instructor, campus, building, room, days, time, start_date, end_date, type, level) VALUES ('COSC 2110', '5T', 3.0, 'Computer Languages', 'Khusanov', 'Webster Univ Tashkent, Uzbekistan', 'North Hall Classrooms', '115', 'F', '09:00a-11:20a', '2024-08-19', '2024-12-13', 'Lecture', 1), ('COSC 2610', '3T', 3.0, 'Operating Systems', 'Boeva, Sok', 'Webster Univ Tashkent, Uzbekistan', 'North Hall Classrooms', '304', 'M', '04:30p-06:50p', '2024-08-19', '2024-12-13', 'Lecture', 1), ('COSC 2710', '2T', 3.0, 'Social Engineering', 'Guseynov', 'Webster Univ Tashkent, Uzbekistan', 'North Hall Classrooms', '406', 'R', '11:30a-01:50p', '2024-08-19', '2024-12-13', 'Lecture', 1), ('ARHS 1050', '1T', 3.0, 'Art Appreciation', 'Novovic, K', 'Webster Univ Tashkent, Uzbekistan', 'North Hall Classrooms', '306', 'F', '11:30a-01:50p', '2024-08-19', '2024-12-13', 'Lecture', 1), ('SCIN 1030', '1T', 3.0, 'Science in the News', 'Attanayake', 'WebNet+', '', '', 'F', '04:30p-06:50p', '2024-08-19', '2024-12-13', 'WebNet+', 1);

# This is optional:
CREATE TABLE Students (student_id SERIAL PRIMARY KEY, name VARCHAR(255), level INT);

INSERT INTO Students (name, level) VALUES ('Damir Rasmuxamedov', 1);

CREATE TABLE Rooms (room_id SERIAL PRIMARY KEY, room_name VARCHAR(50), building_name VARCHAR(50));

INSERT INTO Rooms (room_name, building_name) VALUES ('115', 'North Hall Classrooms'), ('304', 'North Hall Classrooms'), ('406', 'North Hall Classrooms'), ('306', 'North Hall Classrooms');

# This is just to check if it worked:
SELECT * FROM Timetable;
SELECT * FROM Students;
SELECT * FROM Rooms;
```
# 3. Create Flask app like this one:
```python
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
```
# 4. HTML templates:
index.html 
```HTML
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Project of Damir Rasmuxamedov</title>
</head>
<body>
    <h1>University Timetable</h1>

    <form action="/timetable", method="GET">
        <label for="level">Select Level:</label>
        <select name="level" id="level">
            <option value="1">Level 1</option>
            <option value="2">Level 2</option>
            <option value="3">Level 3</option>
        </select>
        <button type="submit">Submit</button>
    </form>
    
</body>
</html>
```
timetable.html
```HTML
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Timetable for Level {{ request.args.get('level') }}</title>
</head>
<body>
    <h1>Timetable for Level {{ request.args.get('level') }}</h1>

    {% if message %}
        <p>{{ message }}</p>
    {% else %}
        <table border="1">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Course Code</th>
                    <th>Section</th>
                    <th>Hours</th>
                    <th>Title</th>
                    <th>Instructor</th>
                    <th>Campus</th>
                    <th>Building</th>
                    <th>Room</th>
                    <th>Days</th>
                    <th>Time</th>
                    <th>Start Date</th>
                    <th>End Date</th>
                    <th>Type</th>
                    <th>Level</th>
                </tr>
            </thead>
            <tbody>
                {% for row in data %}
                    <tr>
                        <td>{{ row[0] }}</td>
                        <td>{{ row[1] }}</td>
                        <td>{{ row[2] }}</td>
                        <td>{{ row[3] }}</td>
                        <td>{{ row[4] }}</td>
                        <td>{{ row[5] }}</td>
                        <td>{{ row[6] }}</td>
                        <td>{{ row[7] }}</td>
                        <td>{{ row[8] }}</td>
                        <td>{{ row[9] }}</td>
                        <td>{{ row[10] }}</td>
                        <td>{{ row[11] }}</td>
                        <td>{{ row[12] }}</td>
                        <td>{{ row[13] }}</td>
                        <td>{{ row[14] }}</td>
                    </tr>
                {% endfor %}
            </tbody>
        </table>
    {% endif %}

    <a href="/">Go Back</a>
</body>
</html>
```
# 5. Install Python and Flask Dependencies
```bash
python -m venv venv

venv\Scripts\activate
If your Windows is blocking this action run this command:
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

pip install flask pg8000
```
# 6. Run the app
```bash
python app.py
```
This is the way how I created this table.
