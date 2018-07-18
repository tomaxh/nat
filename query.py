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

'''
General search using all the feilds
'''
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
					verified_plaintext ~* %s 
					or description_plaintext ~* %s
					or verified_alternates ~* %s
				)
				and 
				(categories.id = %s or categories.parent_id = %s or %s)
			order by alpha_order desc;
		
	""", (*(search,)*3, *(cat_id,)*2, True if cat is None else False))

	return json.dumps({
		'time': time.time() - start,
		'results': list(cursor.fetchall())
	}, indent=4, default=ser_datetime)

'''
search using only verified and verified alternates field
'''
def queryVerified(search, cat):
	conn = psycopg2.connect(
		database='nat',
		user='postgres',
		password= 'postgres',
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
					verified_plaintext~* %s 
					or verified_alternates ~* %s
				)
				and 
				(categories.id = %s or categories.parent_id = %s or %s)
			order by alpha_order desc;
		
	""", (*(search,)*2, *(cat_id,)*2, True if cat is None else False))

	return json.dumps({
		'time': time.time() - start,
		'results': list(cursor.fetchall())
	}, indent=4, default=ser_datetime)

'''delete item from tables'''
def queryDelete(id,table='names_and_terms'):
	conn = psycopg2.connect(
		database='nat',
		user='postgres',
		password= 'postgres',
		host='localhost'
	)
	cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
	try:	
		cursor.execute("""

			DELETE
			FROM
				%s
			WHERE
				id=%s
			
		""" %(table,id)
		)
		conn.commit()
		conn.close()
		return 'Deleted'
	except Exception as e:
		return e


def queryInsert(data):
	
	if data['verified']==None or data['alpha_order']==None or data['category_id']==None:
		return 'Required items not provided.'
	conn = psycopg2.connect(
		database='nat',
		user='postgres',
		password= 'postgres',
		host='localhost'
	)
	
	cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
	cursor.execute("""
		INSERT INTO 
				names_and_terms
				(
					verified,
					verified_plaintext,
					verified_alternates,
					verification_source,
					description,
					description_plaintext,
					comments,
					relationship,
					location,
					alpha_order,
					created_time,
					created_by,
					modified_time,
					modified_by,
					revised_time,
					category_id
				)
			VALUES
				(
					%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
					
				);
	""",(
		data['verified'],
		data['verified_plaintext'],
		data['verified_alternates'],
		data['verification_source'],
		data['description'],
		data['description_plaintext'],
		data['comments'],
		data['relationship'],
		data['location'],
		data['alpha_order'],
		data['created_time'],
		data['created_by'],
		data['modified_time'],
		data['modified_by'],
		data['revised_time'],
		data['category_id']
		)
	)
	conn.commit()
	conn.close()

def queryGetAllInfo(id):
	itemId=id
	'''
	Confirm the itemID and then list the Original Infromation for that Item
	'''
	conn = psycopg2.connect(
		database='nat',
		user='postgres',
		password= 'postgres',
		host='localhost'
	)
	
	cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
	cursor.execute(
		'''
			SELECT* from names_and_terms where id=%s;

		''',(itemId,)
	)
	d1=json.dumps(cursor.fetchall()[0], indent=4, default=ser_datetime)
	d2=json.loads(d1)
	return d2
	'''
	Auto fill the webform for the user to make modifications,ignore unecessary fields
	'''
	
def queryUpdates(data):

	conn = psycopg2.connect(
		database='nat',
		user='postgres',
		password= 'postgres',
		host='localhost'
	)
	
	cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
	cursor.execute("""
		UPDATE 
				names_and_terms
		SET
				verified=%s,
				verified_plaintext=%s,
				verified_alternates=%s,
				verification_source=%s,
				description=%s,
				description_plaintext=%s,
				comments=%s,
				relationship=%s,
				location=%s,
				alpha_order=%s,
				modified_time=%s,
				modified_by=%s,
				revised_time=%s,
				category_id=%s
		WHERE 
				id=%s;
	""",(
		data['verified'],
		data['verified_plaintext'],
		data['verified_alternates'],
		data['verification_source'],
		data['description'],
		data['description_plaintext'],
		data['comments'],
		data['relationship'],
		data['location'],
		data['alpha_order'],
		data['modified_time'],
		data['modified_by'],
		data['revised_time'],
		data['category_id'],
		data['id']
		)
	)
	conn.commit()
	conn.close()

if __name__ == '__main__':
	'''search = sys.argv[1]
	cat = sys.argv[2] if len(sys.argv) > 2 else None
	queryVerified(search, cat)
	print(queryVerified(search, cat))
'''
	json={
                    "id":87699,
                        "verified":"<b>Tester2 UPDATED by new API.</b>",
                        "verified_plaintext":"Tester2 inserted by new API.",
                        "alpha_order":"Tester1 inderted aplha_order.",
                        "category_id":4,
                        "verified_alternates":None,
                        "verification_source":None,
                        "description":"<b>The testing item 2 UPDATEED by REQUEST and POST method",
                        "description_plaintext":"The testing item UPDATE by REQUEST and POST method",
                        "comments":None,
                        "relationship":"Norm's son",
                        "location":None,
                        "created_time":"2025-02-02",
                        "created_by":"Tom",
                        "modified_time":None,
                        "modified_by":None,
                        "revised_time":None
                    }
	queryUpdates(json)

	

