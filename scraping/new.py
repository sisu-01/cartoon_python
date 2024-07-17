from bs4 import BeautifulSoup
from utils.mongo import find_latest_cartoon_id, create_writer, create_cartoon
from datetime import datetime, timedelta
from clustering.mongo import main as clustering
import requests
import time
import re

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def main(prev_page):
  latest_id = find_latest_cartoon_id()
  if latest_id:
    page = daily_scraping(prev_page, int(latest_id['id']))
  else:
    page = init_scraping(get_last_page())
  return page

def init_scraping(last_page):
  page = last_page
  flag = True
  while flag:
    soup_list = get_html(page)
    for soup in reversed(soup_list):
      valid_result = validation(soup)
      if valid_result == 'continue':
        continue
      elif valid_result == 'end':
        flag = False
        break
      writer_dict, cartoon_dict = soup_to_dict(soup)
      insert_db(writer_dict, cartoon_dict)
    #for end
    if flag:
      print(page)
      page = page - 1
      time.sleep(1)
  #while end
  return page

def daily_scraping(prev_page, latest_id):
  page = 1 if prev_page is None else prev_page
  soup_list = None
  while(True):
    soup_list = get_html(page)
    if latest_id >= int(soup_list[-1].get('data-no')):
      break
    page = page + 1
    time.sleep(1)
  #while end
  
  flag = True
  while flag:
    for soup in reversed(soup_list):
      valid_result = validation(soup, latest_id)
      if valid_result == 'continue':
        continue
      elif valid_result == 'end':
        flag = False
        break
      writer_dict, cartoon_dict = soup_to_dict(soup)
      insert_db(writer_dict, cartoon_dict)
    #for end
    if flag:
      print(page)
      page = page - 1
      soup_list = get_html(page)
      time.sleep(1)
  #while end
  return page

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

def validation(soup, latest_id=None):
  # 공지 건너뛰기
  id = soup.get('data-no')
  if id == None:
    return 'continue'
  
  #daily 전용 중복 건너띄기
  if latest_id is not None and latest_id >= int(id):
    return 'continue'
  
  # 만화 게시일 2주 이내
  date_format = '%Y-%m-%d %H:%M:%S'
  date = datetime.strptime(soup.select_one('.gall_date').get('title'), date_format)
  today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
  is_within_two_weeks = date - today > timedelta(days=-12)
  if is_within_two_weeks:
    return 'end'

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
  detail_soup = get_detail_soup(cartoon_id)
  og_image = get_og_image(detail_soup)
  urls = get_urls(detail_soup)

  temp_writer_values = {
    'id': writer_id,
    'nickname': writer_nickname,
    'date': date,
    'recommend': recommend,
  }
  writer_values = merge_urls_and_writer_values(urls, temp_writer_values)

  cartoon_values = {
    'id': cartoon_id,
    'title': title,
    'date': date,
    'recommend': recommend,
    'writer_object_id': None,
    'writer_id': writer_id,
    'writer_nickname': writer_nickname,
    'og_image': og_image,
  }
  return [writer_values, cartoon_values]

def get_detail_soup(cartoon_id):
  time.sleep(1)
  url = f'https://gall.dcinside.com/board/view/?id=cartoon&no={cartoon_id}'
  max_retries = 3
  retries = 0
  while(True):
    if retries >= max_retries:
      return None
    try:
      response = requests.get(url, headers=headers)
      response.raise_for_status()  # Status Code가 400이나 500대면 예외 발생
      res = response.text
      if res.strip():
        soup  = BeautifulSoup(res, 'html.parser')
        if soup:
          return soup
        else:
          print(cartoon_id, 'No soup, retrying...')
      else:
        print(cartoon_id, 'Empty response, retrying...')
    except requests.exceptions.RequestException as e:
      print(f"Request failed for cartoon_id {cartoon_id}: {e}")
    time.sleep(5)
    retries += 1

# def get_og_image(cartoon_id):
#   time.sleep(1)
#   url = f'https://gall.dcinside.com/board/view/?id=cartoon&no={cartoon_id}'
#   max_retries = 3
#   retries = 0
#   while(True):
#     if retries >= max_retries:
#       #실제로는 ""만,
#       return None
#     try:
#       response = requests.get(url, headers=headers)
#       response.raise_for_status()  # Status Code가 400이나 500대면 예외 발생
#       res = response.text
#       if res.strip():
#         soup  = BeautifulSoup(res, 'html.parser')
#         og_image = soup.find('meta', property='og:image')
#         if og_image:
#           ###
#           # import random
#           # if random.random() < 0.01:  # 10% 확률로 출력
#           #   print(cartoon_id, '\n', og_image['content'])
#           ###
#           return og_image['content']
#         else:
#           print(cartoon_id, 'No og:image meta tag found, retrying...')
#       else:
#         print(cartoon_id, 'Empty response, retrying...')
#     except requests.exceptions.RequestException as e:
#       print(f"Request failed for cartoon_id {cartoon_id}: {e}")
#     time.sleep(5)
#     retries += 1

def get_og_image(soup):
  og_image = soup.find('meta', property='og:image')
  if og_image:
    return og_image['content']
  else:
    return None

# 허용할 URL 패턴과 키
pattern_to_key = {
    re.compile(r'm\.blog\.naver\.com'): 'naver',
    re.compile(r'blog\.naver\.com'): 'naver',
    re.compile(r'pixiv\.net/users'): 'pixiv',
    re.compile(r'x\.com'): 'x',
    re.compile(r'twitter\.com'): 'x'
}
def get_urls(soup):
  # 결과를 담을 dict (초기에는 빈 dict)
  result = {}
  view_box_div = soup.find('div', class_='writing_view_box')
  if view_box_div:
    a_tags = view_box_div.find_all('a')
    for a in a_tags:
      if 'href' in a.attrs:
        href = a['href']
        for pattern, key in pattern_to_key.items():
          if pattern.search(href):
            result[key] = href
            break
  if result:
    # 만약 result에 데이터가 있다면
    return result
  else:
    # result가 비어있다면 False 반환
    return False
  
def merge_urls_and_writer_values(urls, writer_values):
  if writer_values.get('id') == "a":
    return writer_values
  if urls:
    urls.update(writer_values)
    return urls
  else:
    return writer_values


def insert_db(writer_value, cartoon_value):
  writer_object_id = create_writer(writer_value)
  if writer_object_id:
    cartoon_acknowledged = create_cartoon(writer_object_id, cartoon_value)
    if cartoon_acknowledged:
      if writer_value['id'] == 'a':
        if writer_value['nickname'] != 'ㅇㅇ' and writer_value['nickname'] != '카갤러':
          clustering({
            'writer_id': writer_value['id'],
            'writer_nickname': writer_value['nickname'],
          })
      else:
        clustering({
          'writer_id': writer_value['id']
        })