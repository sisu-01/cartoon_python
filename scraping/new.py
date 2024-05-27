from bs4 import BeautifulSoup
from utils.mongo import create_writer, create_cartoon
import requests
import time

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def main():
  print('zz')
  scraping(688418)

def scraping(last_id):
  page = 1
  while True:
    #time.sleep(1)
    if page == 5:
      return True
    soup_list = get_soup_list(page)
    for soup in soup_list:
      valid_result = validation(soup)
      if valid_result == 'continue':
         continue
      writer_dict, cartoon_dict = soup_to_dict(soup)
      writer_inserted_id = create_writer(writer_dict)
      cartoon_acknowledged = create_cartoon(writer_inserted_id, cartoon_dict)

    return True

def get_soup_list(page):
  url = f'https://gall.dcinside.com/board/lists/?id=cartoon&page={page}&exception_mode=recommend'
  html = requests.get(url, headers=headers).text
  soup_list = BeautifulSoup(html, 'html.parser').select('tbody > tr.ub-content')
  return soup_list

def validation(soup):
    result = ''
    id = soup.get('data-no')
    if id == None:
      result = 'continue'
      return result

def soup_to_dict(soup):
  id = soup.get('data-no')
  title = soup.select_one('td.gall_tit a').text.strip()
  tempId = soup.select_one('.gall_writer').get('data-uid')
  writer_id = 'a' if not tempId else tempId
  temp_nickname = soup.select_one('td.gall_writer span.nickname em')
  if temp_nickname == None:
    writer_nickname = soup.select_one('td.gall_writer').get('data-nick').strip()
  else:
    writer_nickname = temp_nickname.text.strip()
  date = soup.select_one('.gall_date').get('title')
  recommend = soup.select_one('.gall_recommend').text

  writer_values = {
    'writer_id': writer_id,
    'writer_nickname': writer_nickname,
    'date': date,
    'count': 1,
    'recommend': recommend,
    'average': recommend,
  }
  cartoon_values = {
    'id': id,
    'title': title,
    'writer_id': writer_id,
    'writer_nickname': writer_nickname,
    'date': date,
    'recommend': recommend,
  }
  return [writer_values, cartoon_values]