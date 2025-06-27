import sqlite3

# Connect to the database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Fetch all feedback entries
cursor.execute("""
SELECT feedback.id, users.name, subject, rating, comments 
FROM feedback 
JOIN users ON feedback.student_id = users.id
""")

rows = cursor.fetchall()

print("📋 FEEDBACK ENTRIES:")
print("-" * 60)
for row in rows:
    print(f"ID: {row[0]}, Name: {row[1]}, Subject: {row[2]}, Rating: {row[3]}, Comments: {row[4]}")

conn.close()