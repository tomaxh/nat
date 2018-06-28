import re
import sys
import csv
import requests
import codecs
import psycopg2

from datetime import datetime

VERIFIED = 19
ITEM_TYPE = 3
STATUS = 4
ALPHA_SORT = 5
CREATED_AT = 8
CREATED_BY = 9
ITEM_DESC = 10
LOCATION = 11
MODIFIED_AT = 12
MODIFIED_BY = 13
RELATIONSHIP = 14
VERIFY_SRC = 16
VERIFIED_ALT = 18
COMMENTS = 25

check_links = False
error_links = list()

def maybe_none(value):
	if len(value) == 0:
		return None
	return value

def create_row(src_row):
	row = list()
	#	Verified name.
	verified = re.sub(r'<\/{0,1}div.*?>', '', src_row[VERIFIED])
	verified = verified.replace('&nbsp;', ' ').replace('&amp;', '&').strip()
	row.append(verified)
	#	...and plaintext
	verified_pt = re.sub(r'<.*?>', '', verified)
	row.append(verified_pt.strip())
	#	Verified alt.
	alt = re.sub(r'<.*?>', '', src_row[VERIFIED_ALT])
	alt = alt.replace('&nbsp;', ' ').replace('&quot;', '"')
	row.append(maybe_none(alt.strip()))
	#	Verification src.
	vsrc = src_row[VERIFY_SRC].strip().replace('\n', '; ')
	if check_links and vsrc.startswith('http'):
		if requests.get(vsrc).status_code != 200:
			error_links.append(vsrc)
	row.append(maybe_none(vsrc))

	#	Description.
	desc = src_row[ITEM_DESC]
	desc = re.sub(r'<\/{0,1}(?:div|br).*?>', '', desc)
	desc = desc.replace('&nbsp;', ' ').replace('&quot;', '"')\
		.replace('&amp;', '"').replace("\'", "'").strip()
	row.append(maybe_none(desc))
	#	and plaintext.
	row.append(maybe_none(re.sub(r'<.*?>', '', desc)))

	#	Other text fields.
	row.append(maybe_none(src_row[COMMENTS]))
	row.append(maybe_none(src_row[RELATIONSHIP]))
	row.append(maybe_none(src_row[LOCATION]))

	#	Alphabetical ordering.
	row.append(maybe_none( src_row[ALPHA_SORT]))

	#	Metadata.
	#		Create.
	created = datetime.strptime(src_row[CREATED_AT], '%m/%d/%Y')
	row.append(created)
	created_by = src_row[CREATED_BY]
	if created_by.startswith('LASS'):
		created_by = created_by[5:]
	row.append(maybe_none(created_by))
	#		Modified.
	modified = maybe_none(src_row[MODIFIED_AT])
	if modified:
		modified = datetime.strptime(modified, '%m/%d/%Y')
	row.append(modified)
	modified_by = src_row[MODIFIED_BY]
	if modified_by.startswith('LASS'):
		modified_by = modified_by[5:]
	row.append(maybe_none(modified_by))
	#		Revised.
	revised = modified if len(src_row[STATUS]) > 0 else None
	row.append(revised)

	#	TODO: Categories.
	row.append(None)
	
	return row

def main(argv):
	global check_links

	try:
		filename = argv[0]
	except:
		print('Usage: python transfer_nat.py <access export file> [-c to check links]')
		return 1

	print('Reading from', filename)
	with codecs.open(filename, 'r', encoding='utf-8') as input_file:
		reader = csv.reader(input_file, delimiter=',')
		rows = list(reader)[1:]

	if '-c' in argv:
		print('Checking links')
		check_links = True

	sql = '''
		insert into names_and_terms (
			verified, verified_plaintext,
			verified_alternates, verification_source,
			description, description_plaintext,
			comments, relationship, location,
			alpha_order,
			created_time, created_by, 
			modified_time, modified_by,
			revised_time,
			category_id
		) values (%s);
	'''
	conn = psycopg2.connect(database='nat', user='postgres', 
			password='postgres', host='localhost')
	cur = conn.cursor()
	row_cnt = len(rows)
	for i, row in enumerate(rows):
		db_row = create_row(row)
		fmt = ', '.join('%s' for i in range(len(db_row)))
		try:
			cur.execute(sql%fmt, db_row)
		except Exception as ex:
			print(db_row)
			raise ex
		if i % 100 == 0:
			print('\r%d/%d rows'%(i, row_cnt), end='')
	conn.commit()
	conn.close()

	if check_links:
		print('Dead links:')
		print('\n'.join(error_links))

	return 0

if __name__ == '__main__':
	sys.exit(main(sys.argv[1:]))