import requests
import re
import json

import psycopg2
import psycopg2.extras

from ldap3 import Server, Connection, ALL,NTLM
from ldap3.core.exceptions import LDAPBindError
def testInsert():
    requests.post("http://localhost:7990/insert",
                
                    json={
                        "verified":"TERMXX",
                        "verified_plaintext":"Tester2 inserted by new API.",
                        "alpha_order":"Tester1 inderted aplha_order.",
                        "category":"PEopLE",
                        "verified_alternates":None,
                        "verification_source":None,
                        "description":"<b>The testing item 2 inserted by REQUEST and POST method",
                        "description_plaintext":"The testing item inserted by REQUEST and POST method",
                        "comments":None,
                        "relationship":"JACK's son",
                        "location":None,
                        "created_time":"2025-02-02",
                        "created_by":"Tom",
                        "modified_time":None,
                        "modified_by":None,
                        "revised_time":None

                        
                    }
                )

def testGet():
    requests.get("http://localhost:7990/get?87701")

def testDelete():
    requests.get("http://localhost:7990/get?87701")


def testUpdate():
    requests.post( "http://localhost:7990/update",
                json={
                        "id":87821,
                        "verified":"<b>Tester2 UPDATED by new API.</b>",
                        "verified_plaintext":"Tester2 inserted by new API.",
                        "alpha_order":"Tester1 inderted aplha_order.",
                        "category_id":4,
                        "verified_alternates":None,
                        "verification_source":None,
                        "description":"UPDATED method",
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
        
        )
def processSearch():
    originalSearch = "?the searching string"
    if originalSearch[0]=="?":
        w = originalSearch[1:].split()
        print(w)

def withAuthentication(meth):
    def authenticate(self, req, resp):
        ldapTest(req, resp)
        return meth(self, req, resp)
    return authenticate


def ldapTest():
    
    
        try:
            url = 'ldaps://lass.leg.bc.ca'
            with Connection(url, 
                    user="LASS\\tqinadmin", password="Aspirine1992*", 
                    authentication='NTLM', 
                    auto_bind=True) as connection:
                readback = connection.extend.standard.who_am_i()
                tmp = readback.split("u:LASS\\")[1]
                print(tmp)

        except LDAPBindError:
            readback = None

        if not readback:
            #    Invalid user.
            raise "invalid"

def authTest():
    resp = requests.post("http://localhost:7990/auth",json={"username":"tqinadmin","password":"Aspirine1992*"})
    print(resp.text)

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
		print((json.dumps(rows[0])))
	except:
		rows = None
		return rows


def setCookies():
	url = "http://localhost:7991/"
	r = requests.get(url)
	print(r.cookies["user"])

def synonymCheck():
    keyword = 'bc'
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
            synonym
        where item ~* %s;
	''',(keyword,))
    try:
        rows = cursor.fetchall()
        result = json.dumps((rows[0]['item'][1:-1]))
        print(type(result))
    except:
        rows = "None"
        return rows
    # for item in result:
        # result.pop(result.index(""))
    " ".join(list(result))
    print(result)

if __name__ == '__main__':
    # queryCheckUser("tqin")
	synonymCheck()