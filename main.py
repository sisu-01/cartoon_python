from scraping.scraping import main as mysql
from scraping.new import main as mongo
from utils.telegram import send_sync_message
import schedule
import time

previous_return_value = None

def job():
  global previous_return_value
  try:
    previous_return_value = mongo(previous_return_value)
    print('1. mongo는 됐다이')
    mysql()
    print('2. mysql도 됐다이')
    success_message = f'Job success\nprevious_return_value: {str(previous_return_value)}'
    print('3. 메시지 설정하고')
    send_sync_message(success_message)
    print('4. 전송도 했다아ㅣ')
  except Exception as e:
    print('1. 실패했다이')
    error_message = f"Job error: {str(e)}"
    print('2. 메시지 설정하고')
    send_sync_message(error_message)
    print('3. 실패 메시지 전송했다이')

schedule.every().day.at('23:00').do(job)

while True:
  try:
    schedule.run_pending()
    time.sleep(1)
  except Exception as e:
    error_message = f'Scheduler error: {str(e)}'
    send_sync_message(error_message)
    time.sleep(10)