import psycopg2
import sys
import json

search = sys.argv[1]

conn = psycopg2.connect(database='nat', user='postgres', 
			password='postgres', host='localhost')
cur = conn.cursor()

cur.execute("select id, verified, description from names_and_terms where verified_plaintext ~ %s or description_plaintext ~ %s", (search,)*2)

results_ser = list()
for row in cur.fetchall():
	results_ser.append({
		'id': row[0],
		'verified': row[1],
		'description': row[2]
	})
	
print(json.dumps(results_ser))

