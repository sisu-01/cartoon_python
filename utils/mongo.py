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
wow = db['wow']

def testwow():
  from datetime import datetime
  new_date = datetime.strptime('2021-05-26', '%Y-%m-%d')

  value = {
    'id': 123,
    'nickname': 'sisu',
    'date': new_date,
    'recommend': 100,
  }
  
  old_field = wow.find_one({ "id" : value["id"] })
  if old_field == None:
    result = wow.insert_one(value)
    return result.inserted_id
  else:
    set_value = {}
    #date 비교
    if value['date'] < old_field['date']:
      set_value['date'] = value['date']
    #새 평균 구하기
    new_average = int((old_field['recommend']+value['recommend'])/(old_field['count']+1))
    set_value['average'] = new_average

    a = wow.update_one(
      { 'id': value['id'] },
      {
        "$set": set_value,
        "$inc": {
          'count': 1,
          'recommend': value['recommend'],
        },
      }
    )
    print(a)


def create_writer(value):
  result = writers.insert_one(value)
  return result.inserted_id

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

