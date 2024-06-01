from bs4 import BeautifulSoup
from utils.mongo import create_writer, create_cartoon
import requests
import time

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def main():
  print('zz')
  scraping()

def scraping():
  page = 1497
  while True:
    print(page)
    #time.sleep(1)
    if page == 1492:
      return True
    soup_list = get_html(page)
    for soup in soup_list:
      valid_result = validation(soup)
      if valid_result == 'continue':
         continue
      writer_dict, cartoon_dict = soup_to_dict(soup)
      writer_inserted_id = create_writer(writer_dict)
      print(writer_inserted_id)
      #cartoon_acknowledged = create_cartoon(writer_inserted_id, cartoon_dict)
    return True
    page = page - 1

def get_html(page):
  url = f'https://gall.dcinside.com/board/lists/?id=cartoon&page={page}&exception_mode=recommend'
  html = requests.get(url, headers=headers).text
  soup_list = reversed(BeautifulSoup(html, 'html.parser').select('tbody > tr.ub-content'))
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
  recommend = int(soup.select_one('.gall_recommend').text)

  writer_values = {
    'id': writer_id,
    'nickname': writer_nickname,
    'date': date,
    'recommend': recommend,
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