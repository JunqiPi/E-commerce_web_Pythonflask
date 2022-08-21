import sqlite3 as sql

def Lists():
	connection =sql.connect("nittany.db")
	cursor = connection.cursor()

	cursor.execute('ALTER TABLE listing ADD COLUMN active BOOLEAN DEFAULT true;')
	cursor.execute("SELECT * FROM listing")

	data = cursor.fetchall()
	for row in data:
		print(row)
	connection.commit()

Lists()