import sqlite3
import pandas as pd
from datetime import datetime

DB_PATH = './fake_news.db'   # Update this path accordingly
FAKE = 'FAKE'
REAL = 'REAL'
UNDETERMINED = 'UNDETERMINED'

def add_to_list(item):
    try:
        conn = sqlite3.connect(DB_PATH)

        # Once a connection has been established, we use the cursor
        # object to execute queries
        c = conn.cursor()

        now = datetime.now()
        formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')

        # Keep the initial status as Not Started
        c.execute('insert into news(title, body, result, news_category_id, created) values(?,?,?,?,?)', (item['title'], item['body'], item['result'], item['news_category_id'], formatted_date))

        # We commit to save the change
        conn.commit()
        # return {0: {"id": c.lastrowid, "title": item['title'], "body": item['body'], "result": item['result'], "news_category_id": item['news_category_id'], "created": formatted_date}}
        return [[c.lastrowid, item['title'], item['body'], item['result'], item['news_category_id'], formatted_date]]
        
    except Exception as e:
        print('Error: ', e)
        return None

def get_all_items(limit = False):
    try:
        conn = sqlite3.connect(DB_PATH)
        if limit == False:
            df = pd.read_sql_query("SELECT * from news", conn)
        else:
            df = pd.read_sql_query("SELECT * from news LIMIT " + str(limit), conn)
        return { "count": len(df), "items": df }
        # c = conn.cursor()
        # c.mode = 'tabs'
        # c.headers = 'on'
        # c.execute('select * from news LIMIT 10')
        # sqlite3 -header -separator " " ./home/data.db "select * from datafile;" > out.txt
        # rows = c.fetchall()
        # return { "count": len(rows), "items": rows }
    except Exception as e:
        print('Error: ', e)
        return None

def get_classified_items():
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query("SELECT * from news WHERE result IN ('REAL', 'FAKE')", conn)
        return { "count": len(df), "items": df }
        
    except Exception as e:
        print('Error: ', e)
        return None

def get_unclassified_item(frame = False):
    try:
        conn = sqlite3.connect(DB_PATH)
        if frame:
            rows = pd.read_sql_query("SELECT * from news WHERE result = 'UNDETERMINED' LIMIT 1", conn)
        else:
            c = conn.cursor()
            c.execute("select * from news WHERE result = 'UNDETERMINED' LIMIT 1")
            rows = c.fetchall()
        return { "count": len(rows), "items": rows }
        
    except Exception as e:
        print('Error: ', e)
        return None

def get_item():
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        # c.execute("select * from news where id='%s'" % id)
        c.execute("select * from news where result='%s'" % UNDETERMINED)
        item = c.fetchone()[0]
        return item
    except Exception as e:
        print('Error: ', e)
        return None

def update_status(id, result):
    # Check if the passed status is a valid value
    if (status.lower().strip() == 'real'):
        status = REAL
    elif (status.lower().strip() == 'fake'):
        status = FAKE
    elif (status.lower().strip() == 'undetermined'):
        status = UNDETERMINED
    else:
        print("Invalid Status: " + result)
        return None

    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('update news set result=? where id=?', (status, id))
        conn.commit()
        return {id: status}
    except Exception as e:
        print('Error: ', e)
        return None

def delete_item(id):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('delete from news where id=?', (id,))
        conn.commit()
        return {'id': id}
    except Exception as e:
        print('Error: ', e)
        return None

def search_items(keyword):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("select * from news where title like ?", ('%'+keyword+'%',))
        rows = c.fetchall()
        return { "count": len(rows), "items": rows }
    except Exception as e:
        print('Error: ', e)
        return None