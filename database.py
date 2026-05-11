import sqlite3

conn = sqlite3.connect('students.db')
cursor = conn.cursor()

# Drop old table if exists
cursor.execute("DROP TABLE IF EXISTS students")

# Create new table
cursor.execute('''
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    student_id TEXT,
    cgpa REAL,
    fee_status TEXT,
    hall_ticket TEXT,
    backlog_courses INTEGER,
    registered_courses INTEGER,
    exam_center TEXT
)
''')

# Insert sample data
sample_data = [

    # Your Data
    ('Anil Kumar Zedia', '2023AAPS001', 7.4, 'Paid', 'Generated', 0, 4, 'Jaipur'),

    # Other Students
    ('Rahul Sharma', '2024A1PS001', 7.8, 'Paid', 'Generated', 0, 4, 'Delhi'),

    ('Priya Singh', '2024A1PS002', 5.2, 'Pending', 'Not Generated', 2, 2, 'Mumbai'),

    ('Amit Verma', '2024A1PS003', 8.1, 'Paid', 'Generated', 0, 5, 'Bangalore'),

    ('Sneha Patel', '2024A1PS004', 6.4, 'Pending', 'Generated', 1, 3, 'Hyderabad'),

    ('Karan Mehta', '2024A1PS005', 4.9, 'Pending', 'Not Generated', 4, 1, 'Pune'),

    ('Neha Joshi', '2024A1PS006', 9.0, 'Paid', 'Generated', 0, 5, 'Chennai'),

    ('Rohit Jain', '2024A1PS007', 5.8, 'Paid', 'Generated', 1, 4, 'Kolkata'),

    ('Simran Kaur', '2024A1PS008', 7.1, 'Paid', 'Generated', 0, 4, 'Ahmedabad')
]

cursor.executemany('''
INSERT INTO students
(name, student_id, cgpa, fee_status, hall_ticket,
 backlog_courses, registered_courses, exam_center)

VALUES (?, ?, ?, ?, ?, ?, ?, ?)
''', sample_data)

conn.commit()
conn.close()

print("Database with sample students created successfully!")