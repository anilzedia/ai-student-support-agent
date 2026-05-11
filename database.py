import sqlite3

conn = sqlite3.connect('students.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    student_id TEXT,
    cgpa REAL,
    fee_status TEXT,
    hall_ticket TEXT,
    backlog_courses INTEGER
)
''')

sample_data = [
    ('Rahul Sharma', '2024A1PS001', 7.8, 'Paid', 'Generated', 0),
    ('Priya Singh', '2024A1PS002', 5.2, 'Pending', 'Not Generated', 2),
    ('Amit Verma', '2024A1PS003', 8.1, 'Paid', 'Generated', 0)
]

cursor.executemany('''
INSERT INTO students (name, student_id, cgpa, fee_status, hall_ticket, backlog_courses)
VALUES (?, ?, ?, ?, ?, ?)
''', sample_data)

conn.commit()
conn.close()

print('Database created successfully!')