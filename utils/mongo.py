from pymongo import MongoClient
from dotenv import load_dotenv
import os
#import certifi

load_dotenv()
uri = os.getenv("URI")
#client = MongoClient(uri, tlsCAFile=certifi.where())
client = MongoClient(uri, tls=True, tlsInsecure=True)
db = client['cartoon']
cartoons = db['cartoons']
writers = db['writers']
series = db['series']

def find_latest_cartoon_id():
  latest_cartoon = cartoons.find_one(sort=[('id', -1)], projection={'id': 1, '_id': 0})
  if latest_cartoon is None:
    result = False
  else:
    result = latest_cartoon
  return result

def create_writer(value):
  # id, nickname, date, recommend
  if value['id'] == 'a':
    object_id = anony_writer(value)
  else:
    object_id = fix_nik_writer(value)
  return object_id

def anony_writer(value):
  latest_field = writers.find_one({"id": value["id"],"nickname": value["nickname"]})
  if latest_field == None:
    insert = {
      'id': value['id'],
      'nickname': value['nickname'],
      'first_date': value['date'],
      'last_date': value['date'],
      'count': 1,
      'recommend': value['recommend'],
      'average': value['recommend'],
    }
    result = writers.insert_one(insert)
    return result.inserted_id
  else:
    set_value = {}

    #last 시간 갱신
    if value['date'] > latest_field['last_date']:
      set_value['last_date'] = value['date']

    #새 평균 구하기
    new_average = int((latest_field['recommend']+value['recommend'])/(latest_field['count']+1))
    set_value['average'] = new_average

    writers.update_one(
      { 'id': value['id'], 'nickname': value['nickname'] },
      {
        "$set": set_value,
        "$inc": {
          'count': 1,
          'recommend': value['recommend'],
        },
      }
    )
    return latest_field['_id']

def fix_nik_writer(value):
  latest_field = writers.find_one({ "id" : value["id"] })
  if latest_field == None:
    insert = {
      'id': value['id'],
      'nickname': value['nickname'],
      'nickname_history': [{
        'nickname': value['nickname'],
        'date': value['date'],
      }],
      'first_date': value['date'],
      'last_date': value['date'],
      'count': 1,
      'recommend': value['recommend'],
      'average': value['recommend'],
    }
    result = writers.insert_one(insert)
    return result.inserted_id
  else:
    set_value = {}

    #last 시간 갱신
    if value['date'] > latest_field['last_date']:
      set_value['last_date'] = value['date']

    #새 평균 구하기
    new_average = int((latest_field['recommend']+value['recommend'])/(latest_field['count']+1))
    set_value['average'] = new_average

    #닉네임 변경 내역 확인
    if value['nickname'] != latest_field['nickname_history'][0]['nickname']:
      new_entry = {
          'nickname': value['nickname'],
          'date': value['date'],
      }
      set_value['nickname'] = value['nickname']
      set_value['nickname_history'] = [new_entry] + latest_field['nickname_history']

    writers.update_one(
      { 'id': value['id'] },
      {
        "$set": set_value,
        "$inc": {
          'count': 1,
          'recommend': value['recommend'],
        },
      }
    )
    return latest_field['_id']

def create_cartoon(writer_object_id, value):
  value['writer_object_id'] = writer_object_id
  result = cartoons.insert_one(value)
  return result.acknowledged

def find_cartoons(value):
  result = cartoons.find({ 'writer_id': value['id'], 'writer_nickname': value['nickname'] })
  return list(result)

def reset_series(value):
  series_result = series.delete_many({ 'writer_id': value['id'], 'writer_nickname': value['nickname']})
  return series_result.acknowledged

def set_series(value):
  insert = {
    'id': value['id'],
    'title': value['title'],
    'writer_id': value['writer_id'],
    'writer_nickname': value['writer_nickname'],
    'count': value['count'],
    'last_update': value['date'],
    'average': round(value['recommend'] / value['count']),
    'cartoons_id_list': value['list']
  }
  series.insert_one(insert)

def only_mongo():
  projection = {'_id': 0, 'id': 1, 'nickname': 1, 'nickname_history': 1}
  result = writers.find({}, projection).limit(30)
  return list(result)

def sandbox():
  result = writers.update_many(
    {
        "nickname": {"$exists": False},  # "nickname" 필드가 존재하지 않는 도큐먼트
    },
    [
        {
            "$set": {
                "nickname": {"$arrayElemAt": ["$nickname_history.nickname", 0]}
            }
        }
    ]
  )
  return result