import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from db import run_sql

def validation(soup, newest):
    # 공지 건너뛰기
    result = ''
    id = soup.get('data-no')
    if id == None:
        result = 'continue'
        return result
    
    # 가장 최신 만화까지 보면 끝내기
    if newest >= int(id):
        result = 'break'
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
    writer_nickname = soup.select_one('td.gall_writer span.nickname em').text
    date = soup.select_one('.gall_date').get('title')
    recommend = soup.select_one('.gall_recommend').text

    writer_values = (writer_id, writer_nickname, date, 1, recommend, recommend)
    cartoon_values = (id, title, writer_id, writer_nickname, date, recommend)
    return [writer_values, cartoon_values]

loop = 5
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
def scraping(newest):
    print(f'id {newest}까지 간다')
    for i in range(1, loop+1):
        print(f'{i}페이지')
        url = f'https://gall.dcinside.com/board/lists/?id=cartoon&page={i}&exception_mode=recommend'
        html = requests.get(url, headers=headers).text
        soup_list = BeautifulSoup(html, 'html.parser').select('tbody > tr.ub-content')

        for soup in soup_list:
            validate = validation(soup, newest)
            if validate == 'continue':
                continue
            elif validate == 'break':
                break
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
            result = run_sql(writer_sql, values[0])
            if result:
                cartoon_sql = '''
                INSERT INTO cartoon (id, title, writer_id, writer_nickname, date, recommend)
                VALUES (%s, %s, %s, %s, %s, %s)
                '''
                run_sql(cartoon_sql, values[1])

def main(empty=False):
    sql = 'SELECT id FROM cartoon WHERE 1=1 ORDER BY id DESC LIMIT 1'
    data = run_sql(sql, None, True)
    if not empty and len(data) == 0:
        return False
    else:
        newest = 1 if empty else data[0][0]
        scraping(newest)