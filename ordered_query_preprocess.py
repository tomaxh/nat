import re
import psycopg2
import json

conn = psycopg2.connect(database='nat', user='postgres', password='postgres')
cursor = conn.cursor()

query = 'ICBC Corp.'
occurs = dict()
for word in query.split():
	cursor.execute('''
		select count(exists) from (
			select 1 as exists
			from names_and_terms
			where description_plaintext ~* %s
		) as t;
	''', (word,))
	occurs[word] = cursor.fetchone()[0]

words = list(t[0] for t in sorted(occurs.items(), key = lambda t: t[1]))

selections_top = list()
selections_mid = list()
order = list()
for i, word in enumerate(words):
	name = 'word_%d'%i
	selections_top.append(name)
	selections_mid.append('(regexp_matches(found, \'%s\'))[1] as %s'%(word, name))
	order.append('%s is not null desc, length(%s) desc'%(name, name))

query_main = '''
select found, %s 
	from (
		select found, %s 
		from (
			select description_plaintext as found 
			from names_and_terms 
			where description_plaintext ~* '%s'
		) as t
	)  as t2
	order by %s;
'''%(
	', '.join(selections_top),
	', '.join(selections_mid),
	'|'.join(query.split()),
	', '.join(order)
)

cursor.execute(query_main)
results = list(list(r) for r in cursor.fetchall())
for row in results:
	cnt = 0
	for i in range(len(words)):
		if row[i]:
			cnt += 1
	row.append(cnt)

results.sort(key=lambda r: r[-1], reverse=True)

print('\n'.join(' '.join(repr(s) for s in r) for r in results))

conn.close()