from pymongo import MongoClient
from dotenv import load_dotenv
import os
import certifi

load_dotenv()
uri = os.getenv("URI")
client = MongoClient(uri, tlsCAFile=certifi.where())

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
    'cartoons_id_list': value['list'],
    'og_image': value['og_image'],
  }
  series.insert_one(insert)

#클러스터링만
def only_mongo():
  projection = {'_id': 0, 'id': 1, 'nickname': 1, 'nickname_history': 1}
  result = writers.find({'nickname': '군게'}, projection).limit(30)
  return list(result)

#nickname 없는 고닉들 추가
def create_nickname():
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

#series_id null인 애들 지워
def delete_series_id():
  # series_id 필드를 제거하는 작업을 수행할 쿼리
  filter_query = {"series_id": {"$exists": True}}  # series_id 필드가 존재하는 문서들을 대상으로 합니다.
  update_query = {"$unset": {"series_id": ""}}  # series_id 필드를 제거하는 업데이트 연산

  # update_many()를 사용하여 모든 해당 문서들에 대해 제거 작업을 수행합니다.
  result = cartoons.update_many(filter_query, update_query)

#og:image 싹 추가
def create_og_image():
  filter_query = {
    "og_image": {"$exists": False},
    "writer_nickname": {"$nin": ["괴도흥부", "아이오에우", "행쑨", "아래하", "류ㅎ", "삼식이"]}
  }
  projection = {'_id': -1, 'id': 1}
  result = cartoons.find(filter_query, projection).sort({'_id': 1})
  return list(result)

def update_image(cartoon_id, og_image):
  # 업데이트할 필드와 값을 설정합니다.
  filter_query = {"id": cartoon_id}  # id가 cartoon_id인 문서를 대상으로 합니다.
  update_query = {"$set": {"og_image": og_image}}  # og_image 필드를 추가하는 업데이트 연산

  # update_one()을 사용하여 해당 문서에 대해 업데이트 작업을 수행합니다.
  cartoons.update_one(filter_query, update_query)