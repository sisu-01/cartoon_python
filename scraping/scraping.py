import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from utils.db import create_connection_pool, run_sql
from clustering.app import main as group
import time

def validation(soup, newest):
    # 공지 건너뛰기
    result = ''
    id = soup.get('data-no')
    if id == None:
        result = 'continue'
        return result
    
    # 가장 최신 만화까지 보면 끝내기
    if newest >= int(id):
        result = 'escape'
        return result

    # 만화 게시일 2주 이내
    date_format = '%Y-%m-%d %H:%M:%S'
    date = datetime.strptime(soup.select_one('.gall_date').get('title'), date_format)
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    is_within_two_weeks = date - today > timedelta(days=-13)
    if is_within_two_weeks:
        result = 'continue'
        return result
    
    return ''

def make_values(soup):
    id = soup.get('data-no')
    title = soup.select_one('td.gall_tit a').text
    tempId = soup.select_one('.gall_writer').get('data-uid')
    writer_id = 'a' if not tempId else tempId
    temp_nickname = soup.select_one('td.gall_writer span.nickname em')
    if temp_nickname == None:
        writer_nickname = soup.select_one('td.gall_writer').get('data-nick').strip()
    else:
        writer_nickname = temp_nickname.text.strip()
    date = soup.select_one('.gall_date').get('title')
    recommend = soup.select_one('.gall_recommend').text

    writer_values = (writer_id, writer_nickname, date, 1, recommend, recommend)
    cartoon_values = (id, title, writer_id, writer_nickname, date, recommend)
    return [writer_values, cartoon_values]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def scraping(connection_pool, newest):
    #print(f'id {newest}까지 간다')
    i = 1
    while True:
        time.sleep(1)
        # if i == 5:
        #     return True
        #print(f'{i}페이지')
        url = f'https://gall.dcinside.com/board/lists/?id=cartoon&page={i}&exception_mode=recommend'
        html = requests.get(url, headers=headers).text
        soup_list = BeautifulSoup(html, 'html.parser').select('tbody > tr.ub-content')

        for soup in soup_list:
            validate = validation(soup, newest)
            if validate == 'continue':
                continue
            elif validate == 'escape':
                return True
            values = make_values(soup)
            writer_sql = f'''
                INSERT INTO writer (id, nickname, date, count, recommend, average)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY
                UPDATE count = count+1,
                date = CASE
                WHEN '{values[0][2]}' < date THEN '{values[0][2]}' ELSE date END,
                recommend = recommend+{values[0][4]},
                average = recommend / count
            '''
            writer_result = run_sql(connection_pool, writer_sql, values[0])
            if writer_result:
                cartoon_sql = '''
                INSERT INTO cartoon (id, title, writer_id, writer_nickname, date, recommend)
                VALUES (%s, %s, %s, %s, %s, %s)
                '''
                cartoon_result = run_sql(connection_pool, cartoon_sql, values[1])
                if cartoon_result:
                    is_a = values[0][0] == 'a'
                    is_dd = values[0][1] == 'ㅇㅇ' or values[0][1] == '카갤러'
                    if not (is_a and is_dd):
                        group(connection_pool, (values[1][2], values[1][3])) # writer_id and writer_nickname
                if newest == 0 and int(values[1][0]) == 67:
                    return True
        i += 1

def main():
    connection_pool = create_connection_pool()
    sql = 'SELECT id FROM cartoon WHERE 1=1 ORDER BY id DESC LIMIT 1'
    data = run_sql(connection_pool, sql, None, True)

    if data == None:
        scraping_result = scraping(connection_pool, 0)
    else:
        scraping_result = scraping(connection_pool, data[0][0])
    if not scraping_result:
        print('에러 발생')