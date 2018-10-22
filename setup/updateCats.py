import psycopg2
import psycopg2.extras
import sys

def dbUpdateName():
    conn = psycopg2.connect(
        database='nat', 
        user='postgres', 
        password='postgres', 
        host='localhost'
    )
    cursor = conn.cursor()

    cursor.execute('''update categories set name='First Nations and Indigenous Peoples leaders & officials & councillors & elders' where ID=34''')
    cursor.execute('''update categories set name='Specialized terms and Jargon' where ID=37''')
    cursor.execute('''update categories set name='Resource infrastructure' where ID=11''')
    cursor.execute('''update categories set name='First Nations and Indigenous Peoples Organizations' where ID=21''')
    cursor.execute('''update categories set name='First Nations and Indigenous Peoples Words & Phrases' where ID=40''')
    cursor.execute('''update categories set name='physical infrastructure' where ID=13''')

    # Ministers cut to people
    cursor.execute('''update names_and_terms set category_id=29 where category_id=36''')
    # create work cut to work
    cursor.execute('''update names_and_terms set category_id=41 where category_id=45''')
    # medical condition/ job titles cut to jargons
    cursor.execute('''update names_and_terms set category_id=37 where category_id=38 or category_id=35''')
    # merge places
    cursor.execute('''update names_and_terms set category_id=4 where category_id=5 or category_id=8 or category_id=9 or category_id=10 or category_id=14 or category_id=16 or category_id=17 or category_id=12''')
    
    cursor.execute('''delete from categories where ID=36 or ID=45 or ID=38 or ID=35 or ID=5 or ID=8 or ID=9 or ID=10 or ID=14 or ID=16 or ID=17 or ID=12''')
    
    cursor.execute('''update categories set name=lower(name);''')
    

    
    # cursor.execute('''
    # alter table names_and_terms add column "fulltext_search" text;
    # update names_and_terms set fulltext_search = concat_ws(';',verified_plaintext,description_plaintext,verified_alternates,comments)
    # ''')

    conn.commit()
    conn.close()

def dbAddAuthTable():
    conn = psycopg2.connect(    
        database='nat', 
        user='postgres', 
        password='postgres', 
        host='localhost'
    )
    cursor = conn.cursor()
    cursor.execute('''
	create table authorized_users(
	id serial primary key,
	full_name varchar(30),
	username varchar(30),
	groups varchar(15));
''')

    conn.commit()
    conn.close()

# auth update
def dbUpdateUser():
    auth_users = {
        "user":[
            {   "full_name":"Laurel Bernard",
                "username":"LBernard",
                "groups":"etls"
            },
            {   "full_name":"Karol Morris",
                "username":"KMorris",
                "groups":"etls"
            }, 
            {   "full_name":"Amy Reiswig",
                "username":"AReiswig",
                "groups":"etls"
            }, 
            {   "full_name":"Glenn Wigmore",
                "username":"GWigmore",
                "groups":"etls"
            }, 

            {   "full_name":"Mike Beninger",
                "username":"MBeninger",
                "groups":"researchers"
            }, 
            {   "full_name":"Niloo Farahzadeh",
                "username":"NFarahzadeh",
                "groups":"researchers"
            }, 
            {   "full_name":"David Mattison",
                "username":"DMattison",
                "groups":"researchers"
            }, 
            {   "full_name":"Steve Pocock",
                "username":"SPocock",
                "groups":"researchers"
            },
            {
                "full_name":"Tom Qin",
                "username":"tqin",
                "groups":"researchers"
            }
        ]
    }
    tech_ops = {
        "user":[
            {   "full_name":"Dan Kerr",
                "username":"DKerr",
                "groups":"researchers"
            },
            {   "full_name":"Pamela Holmes",
                "username":"PHolmes",
                "groups":"researchers"
            },
            {   "full_name":"Michael Sinclair",
                "username":"mmsinclair",
                "groups":"researchers"
            },
            {   "full_name":"Robin Saxifrage",
                "username":"RSaxifrage",
                "groups":"researchers"
            }
        ]
    }
    ''' use both user groups techops authusers'''
    for i in tech_ops["user"]:
        conn = psycopg2.connect(
            database='nat',
            user='postgres',
            password='postgres',
            host='localhost',
        )
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(
        '''
            insert into 
                authorized_users(full_name,username,groups)
                    values
                        (%s,%s,%s);
        
        ''',(i["full_name"],i["username"],i["groups"],)
        )
        conn.commit()
        conn.close()
        print("auth update done")

    for i in auth_users["user"]:
        conn = psycopg2.connect(
            database='nat',
            user='postgres',
            password='postgres',
            host='localhost',
        )
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(
        '''
            insert into 
                authorized_users(full_name,username,groups)
                    values
                        (%s,%s,%s);
        
        ''',(i["full_name"],i["username"],i["groups"],)
        )
        conn.commit()
        conn.close()

# add unaccent field to search diacritics 
def addUnaccent():
    conn = psycopg2.connect(
        database='nat',
        user='postgres',
        password='postgres',
        host='localhost'
    )
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute(
        '''
            ALTER TABLE names_and_terms
            ADD column diacritics text;

            UPDATE names_and_terms
            set diacritics = concat_ws(';',verified_plaintext,verified_alternates,description_plaintext);

            ----(might not needed if you already have it)
            Create EXTENSION unaccent;

            update names_and_terms
            set diacritics = unaccent(diacritics);
        '''
        )
    conn.commit()
    conn.close()
    conn = psycopg2.connect(
        database='nat',
        user='postgres',
        password='postgres',
        host='localhost'
    )
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute(
        
        '''ALTER TABLE names_and_terms
            ADD column verified_diacritics text;

            UPDATE names_and_terms
            set verified_diacritics = concat_ws(';',verified_plaintext,verified_alternates);

            ----(might not needed if you already have it)
            Create EXTENSION unaccent;

            update names_and_terms
            set diacritics = unaccent(diacritics);
            '''
        )
    conn.commit()
    conn.close()
if __name__ == "__main__":
    dbUpdateName()
    dbUpdateUser()
    
