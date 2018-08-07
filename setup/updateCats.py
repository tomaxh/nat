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
    
    
    '''???'''
    cursor.execute('''update categories set name=lower(name);''')

    conn.commit()
    conn.close()


    
if __name__ == "__main__":
    dbUpdateName()
    print('Categories update done.')    
    