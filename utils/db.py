import json
import mysql.connector
from mysql.connector import pooling

# db 접속 정보 불러오기
def load_config(file_path):
    with open(file_path, 'r') as config_file:
        config = json.load(config_file)
    return config

# 커넥션 풀 생성
def create_connection_pool():
    db_config = load_config('config/db.json')['db_config']
    return pooling.MySQLConnectionPool(pool_name="my_pool", pool_size=5, **db_config)

def run_sql(pool, sql, values=None, fetch_result=False):
    try:

        #db_config = load_config('config/db.json')['db_config']
        #conn = mysql.connector.connect(**db_config)
        conn = pool.get_connection()

        cursor = conn.cursor(buffered=True)
        cursor.execute(sql, values)
        
        if fetch_result:
            if cursor.rowcount > 0:
                result = cursor.fetchall()
            else:
                result = None
        else:
            result = True

        conn.commit()
        cursor.close()
        conn.close()

        return result
    except mysql.connector.Error as e:
        print(f'Error: {e}')
        conn.rollback()
        return False