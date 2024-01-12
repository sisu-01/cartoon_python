import json
import mysql.connector

def load_config(file_path):
    with open(file_path, 'r') as config_file:
        config = json.load(config_file)
    return config

def run_sql(sql, values=None, fetch_result=False):
    try:
        db_config = load_config('config/db.json')['db_config']
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(buffered=True)
        cursor.execute(sql, values)
        
        if fetch_result:
            result = cursor.fetchall()
        else:
            result = True

        conn.commit()
        cursor.close()
        conn.close()

        return result
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return False