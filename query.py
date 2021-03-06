import psycopg2
import psycopg2.extras
import sys
import json
import time
from datetime import datetime, timedelta
import re
from ldap3 import Server, Connection, ALL,NTLM
from ldap3.core.exceptions import LDAPBindError



def ser_datetime(the):
	if not isinstance(the, datetime):
		raise TypeError(type(the))
	
	return the.strftime('%m/%d/%Y %H:%M %p')
def set_datetime(the):
	st = datetime.fromtimestamp(the).strftime('%Y-%m-%d %H:%M:%S')
	return st
'''
Search query for all the fields
'''
def query(search,mode="stemon",cat=None):

	conn = psycopg2.connect(
		database='nat', 
		user='postgres', 
		password='postgres', 
		host='localhost'
	)
	cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

	if not cat:
		cat_id = None
	else:
		cursor.execute("select id from categories where name = %s", (cat,))
		row = cursor.fetchone()
		cat_id = row['id'] if row else None

	start = time.time()
	begin = datetime.today()+timedelta(days=1)
	end = datetime.today()-timedelta(days=1)
	is_quoted = search[0]=='"' and search[len(search)-1]=='"'


	if search=='@':
		if cat != 'style':
			cursor.execute("""

				select 
						names_and_terms.id, verified, verified_alternates, verification_source, 
						description, comments, relationship, location, name as category,
						created_time, created_by, modified_time, modified_by, revised_time,alpha_order,description_plaintext,verified_plaintext
					from 
						names_and_terms 
						inner join categories 
						on names_and_terms.category_id = categories.id
					where 
						(
							(date %s <= created_time::date AND created_time::date <= date %s)
								OR
							(date %s <= modified_time::date AND modified_time::date <= date %s)
						)
						and 
						(categories.id != %s )
					order by alpha_order
					limit 3000;
					
					""",(end,begin,end,begin,18,))
		else:
			cursor.execute("""

				select 
						names_and_terms.id, verified, verified_alternates, verification_source, 
						description, comments, relationship, location, name as category,
						created_time, created_by,description_plaintext,verified_plaintext, modified_time, modified_by, revised_time,alpha_order
					from 
						names_and_terms 
						inner join categories 
						on names_and_terms.category_id = categories.id
					where 
						(
							(date %s <= created_time::date AND created_time::date <= date %s)
								OR
							(date %s <= modified_time::date AND modified_time::date <= date %s)
						)
						and 
						(categories.id = %s )
					order by alpha_order
					limit 3000;
					
					""",(end,begin,end,begin,18,))
	
	elif search[0]=='*':
		cursor.execute("""

			select 
					names_and_terms.id, verified, verified_alternates, verification_source, 
					description, comments, relationship, location, name as category,
					created_time,description_plaintext,verified_plaintext, created_by,alpha_order, modified_time, modified_by, revised_time
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
						or diacritics ~* %s

					)
					and 
					(categories.id = %s or categories.parent_id = %s or %s)
				order by alpha_order
				limit 3000;
			
		""", (*(search[1:]+"\\M",)*5, *(cat_id,)*2, True if cat is None else False))
	elif search.find("*")>0:

		cursor.execute("""

			select 
					names_and_terms.id, verified, verified_alternates, verification_source, 
					description, comments, relationship, location, name as category,
					created_time,description_plaintext,verified_plaintext, created_by,alpha_order, modified_time, modified_by, revised_time
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
						or diacritics ~* %s

					)
					and 
					(categories.id = %s or categories.parent_id = %s or %s)
				order by alpha_order
				limit 3000;
			
		""", (*("\\m"+search[0:search.find("*")],)*5, *(cat_id,)*2, True if cat is None else False))
	
	
	elif is_quoted or len(search.split()) < 2:
		if is_quoted:
			search = "\\y"+search[1:-1]+"\\y"
		
		if mode =="stemoff":
			search = "\\y"+search+"\\y"
		
		print(search)
		cursor.execute("""

			select 
					names_and_terms.id, verified, verified_alternates, verification_source, 
					description, comments, relationship, location, name as category,
					created_time,description_plaintext,verified_plaintext, created_by,alpha_order, modified_time, modified_by, revised_time
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
						or diacritics ~* %s

					)
					and 
					(categories.id = %s or categories.parent_id = %s or %s)
				order by alpha_order
				limit 3000;
			
		""", (*(search,)*5, *(cat_id,)*2, True if cat is None else False))	
	else:
		checked = replaceSynonym(search)
		if mode == "stemoff":
			if len(checked[1])==0:
				w = ' & '.join(checked[0][:-1])
			else:
				w1 =''.join(checked[1])[:-1].replace('.','\\.')
				w = ' & '.join(checked[0]) + '(' +w1.replace(' ','<->') +')'
		else:
			if len(checked[1])==0:
				w = ':* & '.join(checked[0][:-1])+':*'
			else:
				w1 =''.join(checked[1])[:-1].replace('.','\\.')
				w = ':* & '.join(checked[0]) + '(' +w1.replace(' ','<->') +')'
		# if mode == "stemoff":
		# 	w =' & '.join(search.split())		
		# else:
		# 	w =':* & '.join(search.split())+':*'
			
		
		print(w)

		cursor.execute("""
		select t1id id,verified,verified_alternates, verification_source, 
					description, comments, relationship, location, category,
					created_time,description_plaintext,verified_plaintext, created_by,alpha_order, modified_time, modified_by, revised_time
    	from(
    	select * FROM
        (
            SELECT  names_and_terms.id as t1id,parent_id, verified,verified_alternates, verification_source, 
                        description, comments, relationship, location, name as category,category_id,
                        created_time,description_plaintext,verified_plaintext, created_by, alpha_order,modified_time, modified_by, revised_time,(concat_ws(';',verified_plaintext,verified_alternates,comments,diacritics)) as t1 
                from  
                    (
                    names_and_terms 
                    join categories 
                    on names_and_terms.category_id = categories.id
                    )
        )as t2 
        
        where to_tsvector('simple',t1) @@ to_tsquery('simple',%s) and 
		(category_id = %s or parent_id = %s or %s )
        

    	)as t3
		
		order by alpha_order
		limit 3000;
		""",(w,*(cat_id,)*2,True if cat is None else False))	
	
	return json.dumps({
		'time': time.time() - start,
		'results': list(cursor.fetchall())
	}, default=ser_datetime)

'''
Search query using only verified and verified alternates field
Same as regular search except for the where clause in sql query
'''
def queryVerified(search, mode="stemon", cat=None):
	conn = psycopg2.connect(
		database='nat',
		user='postgres',
		password= 'postgres',
		host='localhost'
	)
	cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
	
	if not cat:
		cat_id = None
	else:
		cursor.execute("select id from categories where name = %s", (cat,))
		row = cursor.fetchone()
		cat_id = row['id'] if row else None

	is_quoted = search[0]=='"' and search[len(search)-1]=='"'

	start = time.time()
	if search[0]=='!':
		cursor.execute("""

			select 
					names_and_terms.id, verified, verified_alternates, verification_source, 
					description, comments, relationship, location, name as category,
					created_time, created_by,alpha_order, modified_time, modified_by, revised_time
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
				order by alpha_order
				limit 3000;
			
		""", (*('\\m'+search[1:]+'\\M',)*2, *(cat_id,)*2, True if cat is None else False))
	
	elif search[0]=='*':
		cursor.execute("""

			select 
					names_and_terms.id, verified, verified_alternates, verification_source, 
					description, comments, relationship, location, name as category,
					created_time,description_plaintext,verified_plaintext, created_by,alpha_order, modified_time, modified_by, revised_time
				from 
					names_and_terms 
					inner join categories 
					on names_and_terms.category_id = categories.id
				where 
					(
						verified_plaintext ~* %s
						or verified_alternates ~* %s
						or verified_diacritics ~* %s


					)
					and 
					(categories.id = %s or categories.parent_id = %s or %s)
				order by alpha_order
				limit 3000;
			
		""", (*("\\w+"+search[1:],)*3, *(cat_id,)*2, True if cat is None else False))
	elif search.find("*")>0:

		cursor.execute("""

			select 
					names_and_terms.id, verified, verified_alternates, verification_source, 
					description, comments, relationship, location, name as category,
					created_time,description_plaintext,verified_plaintext, created_by,alpha_order, modified_time, modified_by, revised_time
				from 
					names_and_terms 
					inner join categories 
					on names_and_terms.category_id = categories.id
				where 
					(
						verified_plaintext ~* %s
						or verified_alternates ~* %s
						or verified_diacritics ~* %s

					)
					and 
					(categories.id = %s or categories.parent_id = %s or %s)
				order by alpha_order
				limit 3000;
			
		""", (*(search[0:search.find("*")]+"\\w+",)*3, *(cat_id,)*2, True if cat is None else False))
	
	elif is_quoted or len(search.split()) < 2:
		if is_quoted:
			search = "\\y"+search[1:-1]+"\\y"
		
		if mode =="stemoff":
			search = "\\y"+search+"\\y"

		cursor.execute("""

			select 
					names_and_terms.id, verified, verified_alternates, verification_source, 
					description, comments, relationship, location, name as category,
					created_time,description_plaintext,verified_plaintext, created_by,alpha_order, modified_time, modified_by, revised_time
				from 
					names_and_terms 
					inner join categories 
					on names_and_terms.category_id = categories.id
				where 
					(
						verified_plaintext ~* %s
						or verified_alternates ~* %s
						or verified_diacritics ~* %s

					)
					and 
					(categories.id = %s or categories.parent_id = %s or %s)
				order by alpha_order
				limit 3000;
			
		""", (*(search,)*3, *(cat_id,)*2, True if cat is None else False))	
	else:
		if mode == "stemoff":
			w =' & '.join(search.split())		
		else:
			w =':* & '.join(search.split())+':*'


		cursor.execute("""
		select t1id id,verified,verified_alternates, verification_source, 
					description, comments, relationship, location, category,
					created_time,description_plaintext,verified_plaintext, created_by,alpha_order, modified_time, modified_by, revised_time
    	from(
    	select * FROM
        (
            SELECT  names_and_terms.id as t1id,parent_id, verified,verified_alternates, verification_source, 
                        description, comments, relationship, location, name as category,category_id,
                        created_time,description_plaintext,verified_plaintext, created_by, alpha_order,modified_time, modified_by, revised_time,(concat_ws(';',verified_plaintext,verified_alternates,verified_diacritics)) as t1 
                from  
                    (
                    names_and_terms 
                    join categories 
                    on names_and_terms.category_id = categories.id
                    )
        )as t2 
        
        where to_tsvector('simple', t1) @@ to_tsquery('simple', %s) and 
		(category_id = %s or parent_id = %s or %s )
        

    	)as t3
		
		order by alpha_order
		limit 3000;
		""",(w,*(cat_id,)*2,True if cat is None else False))	
	
	return json.dumps({
		'time': time.time() - start,
		'results': list(cursor.fetchall())
	}, indent=4, default=ser_datetime)

'''
delete item from tables
'''
def queryDelete(id):
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
				names_and_terms
			WHERE
				id=%s			
		""" %(id)
		)
		conn.commit()
		conn.close()
		return 'Deleted'
	except Exception as e:
		return e

'''
Return the full name of the category, take category id as parameter
Used in queryInsert to chekc the input category
'''
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
		return m.group(0)

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
	return d1

def queryUpdates(data):
	
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
		category_id,
		data['id']
		)
	)
	conn.commit()
	conn.close()
# auth update
def ldapTest(user):
        try:
            url = 'ldaps://lass.leg.bc.ca'
            u = user["username"]
            p = user["password"]
            with Connection(url, 
                    user="LASS\\"+ u, password=p, 
                    authentication='NTLM', 
                    auto_bind=True) as connection:
                readback = (connection.extend.standard.who_am_i()).split("u:LASS\\")[1]

        except LDAPBindError:
            readback = 'Unrecognized'

        return readback

#auth update
def queryCheckUser(username):
	conn = psycopg2.connect(
		database='nat',
		user='postgres',
		password='postgres',
		host='localhost'
	)
	cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
	cursor.execute('''
		select 
			full_name, groups
		from
			authorized_users
		where lower(username) = lower(%s)
	''',(username,))
	try:
		rows = cursor.fetchall()
		return json.dumps(rows[0])
	except:
		rows = {'full_name':username,'groups':'Unrecognized'}
		return json.dumps(rows)

def getSynonym(keyword):
    conn = psycopg2.connect(
		database='nat',
		user='postgres',
		password='postgres',
		host='localhost'
    )
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute('''
        select 
            * 
        from 
            synonyms
        where item ~* %s;
	''',('\\;'+keyword+'\\;',))
    try:
        rows = cursor.fetchall()
        result = json.dumps((rows[0]['item']))
        result = "|".join([i for i in result.split(";") if i !='"'])
    except:
        result = None

    return result

# check if the search string contains a synonym return if exist
def replaceSynonym(search):
    result = []
    search = search.split()    
    for i in search:
        if getSynonym(i):
            result.append(getSynonym(i)+'|')
    search = [x for x in search if not getSynonym(x)]+['']
    
    return [search,list(set(result))]



if __name__ == '__main__':
	query("pipe west","stemoff")

	

	

