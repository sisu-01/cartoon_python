from bs4 import BeautifulSoup
from utils.mongo import create_writer, create_cartoon
from datetime import datetime, timedelta
import requests
import time

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def main():
  #db에 아무것도 없다면??
  if False:
    init_scraping(get_last_page())
  else:
    daily_scraping(688722)
  
def init_scraping(last_page):
  page = last_page
  while True:
    print(page)
    time.sleep(1)
    if page == last_page-5:
      break
    soup_list = get_html(page)
    for soup in reversed(soup_list):
      valid_result = validation(soup)
      if valid_result == 'continue':
         continue
      writer_dict, cartoon_dict = soup_to_dict(soup)
      writer_object_id = create_writer(writer_dict)
      is_success = create_cartoon(writer_object_id, cartoon_dict)
    page = page - 1

def daily_scraping(latest_id):
  page = 1
  b = []
  while(True):
    print(page)
    time.sleep(1)
    if page == 2+1:
      break
    soup_list = get_html(page)
    for soup in soup_list:
      valid_result = validation(soup, latest_id)
      print(valid_result)
      if valid_result == 'continue':
        continue
      elif valid_result == 'break':
        break
      writer_dict, cartoon_dict = soup_to_dict(soup)
      b.append((writer_dict, cartoon_dict))
    page = page + 1
  for i in reversed(b):
    insert_db(*i)

def get_last_page():
  import re
  url = f'https://gall.dcinside.com/board/lists/?id=cartoon&page=1&exception_mode=recommend'
  html = requests.get(url, headers=headers).text
  a_tag = BeautifulSoup(html, 'html.parser').find('a', class_='page_end')
  href = a_tag['href']
  match = re.search(r'page=(\d+)', href)
  page = int(match.group(1))
  return page

def get_html(page):
  url = f'https://gall.dcinside.com/board/lists/?id=cartoon&page={page}&exception_mode=recommend'
  html = requests.get(url, headers=headers).text
  soup_list = BeautifulSoup(html, 'html.parser').select('tbody > tr.ub-content')
  return soup_list

def validation(soup, latest_id):
  # 공지 건너뛰기
  id = soup.get('data-no')
  if id == None:
    return 'continue'
  # 끊기
  elif latest_id  >= int(id):
    return 'break'
  
  # 만화 게시일 2주 이내
  date_format = '%Y-%m-%d %H:%M:%S'
  date = datetime.strptime(soup.select_one('.gall_date').get('title'), date_format)
  today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
  is_within_two_weeks = date - today > timedelta(days=-12)
  if is_within_two_weeks:
    return 'continuezzzz'

def soup_to_dict(soup):
  cartoon_id = int(soup.get('data-no'))
  title = soup.select_one('td.gall_tit a').text.strip()
  tempId = soup.select_one('.gall_writer').get('data-uid')
  writer_id = 'a' if not tempId else tempId
  temp_nickname = soup.select_one('td.gall_writer span.nickname em')
  if temp_nickname == None:
    writer_nickname = soup.select_one('td.gall_writer').get('data-nick').strip()
  else:
    writer_nickname = temp_nickname.text.strip()
  date = soup.select_one('.gall_date').get('title')
  recommend = int(soup.select_one('.gall_recommend').text)

  writer_values = {
    'id': writer_id,
    'nickname': writer_nickname,
    'date': date,
    'recommend': recommend,
  }
  cartoon_values = {
    'id': cartoon_id,
    'title': title,
    'date': date,
    'recommend': recommend,
    'writer_object_id': None,
    'writer_id': writer_id,
    'writer_nickname': writer_nickname,
  }
  return [writer_values, cartoon_values]

def insert_db(writer_value, cartoon_value):
  print(writer_value, cartoon_value)
  return 'zz'
  # writer_object_id = create_writer(writer_value)
  # cartoon_acknowledged = create_cartoon(writer_object_id, cartoon_value)
  # return cartoon_acknowledged
