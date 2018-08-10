import psycopg2
import psycopg2.extras
import sys
import json
import time
from datetime import datetime
import re

PAGE_OFFSET = 0

def ser_datetime(the):
	if not isinstance(the, datetime):
		raise TypeError(type(the))
	
	return the.strftime('%m/%d/%Y %H:%M %p')

'''
TODO: MULTIPLE CATEGORY (maybe not)

'''
def query(search, cat):

	conn = psycopg2.connect(
		database='nat', 
		user='postgres', 
		password='postgres', 
		host='localhost'
	)
	cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

	cursor.execute("select id from categories where name ~* %s", (cat,))
	row = cursor.fetchone()
	cat_id = row['id'] if row else None

	start = time.time()
	if search[0]=='!':
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
						or comments ~* %s
					)
					and 
					(categories.id = %s or categories.parent_id = %s or %s)
				order by alpha_order;
			
		""", (*('\\m'+search[1:]+'\\M',)*4, *(cat_id,)*2, True if cat is None else False))
	
	elif search[0]=='*':
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
						or comments ~* %s

					)
					and 
					(categories.id = %s or categories.parent_id = %s or %s)
				order by alpha_order;
			
		""", (*(search[1:]+"\\M",)*4, *(cat_id,)*2, True if cat is None else False))
	elif search.find("*")>0:

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
						or comments ~* %s

					)
					and 
					(categories.id = %s or categories.parent_id = %s or %s)
				order by alpha_order;
			
		""", (*("\\m"+search[0:search.find("*")],)*4, *(cat_id,)*2, True if cat is None else False))
	
	
	elif search[0]=='?':
		w =':* & '.join(search[1:].split())+':*'
		print(search)

		cursor.execute("""
		select t1id id,verified,verified_alternates, verification_source, 
					description, comments, relationship, location, category,
					created_time, created_by, modified_time, modified_by, revised_time
    	from(
    	select * FROM
        (
            SELECT  names_and_terms.id as t1id,verified,verified_alternates, verification_source, 
                        description, comments, relationship, location, name as category,category_id,
                        created_time, created_by, alpha_order,modified_time, modified_by, revised_time,(concat_ws(';',verified_plaintext,description_plaintext,verified_alternates)) as t1 
                from  
                    (
                    names_and_terms 
                    join categories 
                    on names_and_terms.category_id = categories.id
                    )
        )as t2 
        
        where (t1) @@ to_tsquery(%s) and 
		(category_id = %s or %s)
        

    )as t3
		
		order by alpha_order;
		""",(w,cat_id,True if cat is None else False))
	else:
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
						or comments ~* %s

					)
					and 
					(categories.id = %s or categories.parent_id = %s or %s)
				order by alpha_order;
			
		""", (*(search,)*4, *(cat_id,)*2, True if cat is None else False))
	

	
	
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
	if search[0]=='!':
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
				order by alpha_order;
			
		""", (*('\\m'+search[1:]+'\\M',)*2, *(cat_id,)*2, True if cat is None else False))
	
	elif search[0]=='*':
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
						or verified_alternates ~* %s

					)
					and 
					(categories.id = %s or categories.parent_id = %s or %s)
				order by alpha_order;
			
		""", (*("\\w+"+search[1:],)*2, *(cat_id,)*2, True if cat is None else False))
	elif search.find("*")>0:

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
						or verified_alternates ~* %s

					)
					and 
					(categories.id = %s or categories.parent_id = %s or %s)
				order by alpha_order;
			
		""", (*(search[0:search.find("*")]+"\\w+",)*2, *(cat_id,)*2, True if cat is None else False))
	else:
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
						or verified_alternates ~* %s

					)
					and 
					(categories.id = %s or categories.parent_id = %s or %s)
				order by alpha_order;
			
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


def checkCat(data):


	conn = psycopg2.connect(
		database='nat',
		user='postgres',
		password= 'postgres',
		host='localhost'
	)
	cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
	cursor.execute("""
		SELECT id FROM
			categories
		WHERE
			name ~* %s;	
		
	""",('\\m'+data['category']+'\\M',)
	)
	k= json.dumps({
		'result':list(cursor.fetchall())
	}, indent=4, default=ser_datetime)

	m = re.search(r'\d+',k)
	if m==None:
		return None
	else:
		return m[0]

def queryInsert(data):
	
	if data['verified']==None or data['alpha_order']==None or data['category']==None:
		return 'Required fields are missing.'
	
	category_id = checkCat(data)
	if category_id==None:
		return "Invalid category name."

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
		category_id
		)
	)
	conn.commit()
	conn.close()
	return "Insert Completed."

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
	
	print(query('?pipe oil', 'places'))

	

	

