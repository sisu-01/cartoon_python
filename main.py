#from scraping.scraping import main
from scraping.new import main
import schedule
import time

previous_return_value = None

def job():
  global previous_return_value
  previous_return_value = main(previous_return_value)

schedule.every().day.at("23:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)

# 작가 목록 싹 돌면서 클러스터링
def onlyClustering():
  from utils.db import create_connection_pool, run_sql
  pool = create_connection_pool()
  list = run_sql(pool, 'select id, nickname from writer where 1=1', None, True)
  from clustering.app import main as group
  for i, row in enumerate(list):
    print(i, row)
    is_a = row[0] == 'a'
    is_dd = row[1] == 'ㅇㅇ' or row[1] == '카갤러'
    if not (is_a and is_dd):
      group(pool, row)

# 작가 목록 싹 돌면서 클러스터링
# mongodb용
def only_clustering_mongo():
  from utils.mongo import only_mongo
  from clustering.mongo import main
  writers = only_mongo()
  for i in writers:
    print(i)
    value = {}
    if i['id'] == 'a':
      if i['nickname'] != 'ㅇㅇ' and i['nickname'] != '카갤러':
        main(i)
    else:
      value = {
        'id': i['id'],
        'nickname': i['nickname_history'][0]['nickname']
      }
      main(value)

#job()
#onlyClustering()
#only_clustering_mongo()