import psycopg2
import json

x = '''1;#People
1;#People:Job titles
46;#Style
16;#Technical ? Scientific Terms
5;#Programs ? Initiatives
48;#Works
2;#Works:Reports ? studies
15;#Works:Creative works
13;#Events ? Awards
14;#Places
7;#Organizations
32;#Organizations:Post-secondary organizations
27;#Organizations:Federal ? other jurisdictions
39;#Places:Cities ? towns
51;#Organizations:Health sector organizations
29;#Organizations:K-12 organizations
6;#Places:Physical infrastructure:Buildings ? landmarks
45;#Places:Transportation Infrastructure:Highways ? Roads
43;#Places:Transportation Infrastructure
26;#Organizations:Crown corporations ? government agencies
49;#Works:Accords ? charters ? conventions ? declarations
18;#Modes of Transport
4;#Brand Names
50;#Works:Legislation
17;#Non-English Words ? Phrases
44;#Places:Transportation Infrastructure:Airports
37;#People:MLAs ? elected officials
35;#People:First Nations leaders ? officials ? councillors ? elders
28;#Organizations:First Nations organizations
33;#Organizations:Unions
36;#People:Government ? legislature ? statutory officers employees
56;#Non-English Words ? Phrases:First Nations Words ? Phrases
25;#Places:Transportation Infrastructure:Bridges
24;#Places:Physical infrastructure
40;#Places:Parks
30;#Organizations:Local governments ? regional districts
34;#People:Fictional personal names ? nicknames
42;#Places:Regions and areas of B.C.
20;#Technical ? Scientific Terms:Medical conditions
23;#Places:Physical infrastructure:Mines
22;#Places:Physical infrastructure:Dams
38;#People:Parliamentary officials ? statutory officers
3;#People:MLAs ? elected officials:Ministers
21;#Places:Fictional place names ? nicknames
31;#Organizations:Ministries
41;#Places:Parliamentary places
12;#Miscellaneous'''

top_levels = dict()
for one in x.split('\n'):
	one = one.split('#')[1]
	if ':' in one:
		level, *subs = one.split(':')
		level = level.replace('?', '&')
		if level not in top_levels:
			top_levels[level] = dict()
		for sub in subs:
			sub = sub.replace('?', '&')
			top_levels[level][sub] = dict()
	else:
		level, sub = top_levels, one
		sub = sub.replace('?', '&')
		level[sub] = dict()


conn = psycopg2.connect(database='nat', user='postgres', 
			password='postgres', host='localhost')
cur = conn.cursor()

def create_one(name, parent_id=None):
	cur.execute('insert into categories (name, parent_id) values (%s, %s) returning id;', (name, parent_id))
	my_id = cur.fetchone()[0]
	print(name)
	if not parent_id:
		for key in top_levels[name].keys():
			create_one(key, my_id)

for key in top_levels.keys():
	create_one(key)

conn.commit()
conn.close()