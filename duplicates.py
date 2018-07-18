import psycopg2
import psycopg2.extras
import sys
import xlsxwriter


'''
Find duplicates for MIKE
'''
def dups():
    conn = psycopg2.connect(
        database='nat', 
        user='postgres', 
        password='postgres', 
        host='localhost'
    )
    cursor = conn.cursor()

    cursor.execute("select verified, id, created_by from names_and_terms where verified in(select verified from names_and_terms group by verified having count(verified)>1)order by verified;")
    conn.commit()
    alist = list(cursor.fetchall())
   
    workbook = xlsxwriter.Workbook('data/dups.xlsx')
    worksheet = workbook.add_worksheet()
    index = 1
    worksheet.write('A1','Term')
    worksheet.write('B1','ID')
    for i in alist:
        index+=1    
        worksheet.write('A'+str(index),i[0])
        worksheet.write('B'+str(index),i[1])
        worksheet.write('C'+str(index),i[2])


if __name__ == "__main__":
    dups()
    print('duplicates output done to -> file dups.xlsx.')    
    
