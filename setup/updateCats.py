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

    cursor.execute('''update categories set name='First Nations and Indigenous Peoples leaders & officials & councillors & elders' where ID=4''')
    cursor.execute('''update categories set name='Specialized terms and Jargon' where ID=10''')
    cursor.execute('''update categories set name='Resource infrastructure' where ID=23''')
    cursor.execute('''update categories set name='First Nations and Indigenous Peoples Organizations' where ID=39''')
    cursor.execute('''update categories set name='First Nations and Indigenous Peoples Words & Phrases' where ID=46''')

    cursor.execute('''update names_and_terms set category_id=1 where category_id=2 or category_id=8''')
    cursor.execute('''update names_and_terms set category_id=10 where category_id=11''')
    cursor.execute('''update names_and_terms set category_id=13 where category_id=15''')
    cursor.execute('''update names_and_terms set category_id=19 where category_id=22 or category_id=24 or category_id=25 or category_id=26 or category_id=28 or category_id=29 or category_id=30 or category_id=32''')
    
    cursor.execute('''delete from categories where ID=2 or ID=8 or ID=11 or ID=15 or ID=22 or ID=24 or ID=25 or ID=26 or ID=28 or ID=29 or ID=30 or ID=32''')
    
    cursor.execute('''update categories set name=lower(name);''')
    

    
    # cursor.execute('''
    # alter table names_and_terms add column "fulltext_search" text;
    # update names_and_terms set fulltext_search = concat_ws(';',verified_plaintext,description_plaintext,verified_alternates,comments)
    # ''')

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
    
if __name__ == "__main__":
    dbUpdateName()
    print('Categories update done.')    
    