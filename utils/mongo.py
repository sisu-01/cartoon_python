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
      latest_field['nickname_history'].insert(0, new_entry)

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

def create_cartoon(writer_id, value):
  value['writer_object_id'] = writer_id
  result = cartoons.insert_one(value)
  return result.acknowledged

# def read_posts():
#   """모든 글을 읽는 함수"""
#   posts = collection.find()
#   for post in posts:
#     print(f'ID: {post["_id"]}, 제목: {post["title"]}, 내용: {post["content"]}')

# def update_post(post_id, title=None, content=None):
#   """글을 수정하는 함수"""
#   update_fields = {}
#   if title:
#     update_fields['title'] = title
#   if content:
#     update_fields['content'] = content

#     if update_fields:
#       result = collection.update_one({'_id': post_id}, {'$set': update_fields})
#       if result.modified_count > 0:
#         print(f'글 ID {post_id}가 수정되었습니다.')
#       else:
#         print(f'글 ID {post_id}를 찾을 수 없거나 변경된 내용이 없습니다.')

# if __name__ == '__main__':
#     print('test')
#     test = '요절복통 앰생요정 -1'
#     create_post(test)
#     query = {'title': test}
#     cartoon = cartoons.find_one(query)
#     print(cartoon)

