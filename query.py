import psycopg2
import psycopg2.extras
import sys
import json
import time

from datetime import datetime

def ser_datetime(the):
	if not isinstance(the, datetime):
		raise TypeError(type(the))
	
	return the.strftime('%m/%d/%Y %H:%M %p')

def query(search, cat):
	conn = psycopg2.connect(
		database='nat', 
		user='postgres', 
		password='postgres', 
		host='localhost'
	)
	cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

	cursor.execute("select id from categories where name = %s", (cat,))
	row = cursor.fetchone()
	cat_id = row['id'] if row else None

	start = time.time()
	cursor.execute("""

		select 
				names_and_terms.id, verified, verified_alternates, verification_source, 
				description, comments, relationship, location, name as category,
				created_time, created_by, modified_time, modified_by, revised_time
			from 
				names_and_terms 
				inner join categories 
				on names_and_terms.category_id = categories.id
			where 
				(
					verified_plaintext ~ %s 
					or description_plaintext ~ %s
					or verified_alternates ~ %s
				)
				and 
				(categories.id = %s or categories.parent_id = %s or %s)
			order by alpha_order desc;
		
	""", (*(search,)*3, *(cat_id,)*2, True if cat is None else False))

	return json.dumps({
		'time': time.time() - start,
		'results': list(cursor.fetchall())
	}, indent=4, default=ser_datetime)

if __name__ == '__main__':
	search = sys.argv[1]
	cat = sys.argv[2] if len(sys.argv) > 2 else None
	query(search, cat)
