from scraping.scraping import main as mysql
from scraping.new import main as mongo
from utils.telegram_sender import send_sync_message
import schedule
import time
import logging
import os

# logs 폴더 생성 (없으면)
os.makedirs('logs', exist_ok=True)

# 로깅 설정
logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/job_log.log'),  # 로그 파일로 기록
        logging.StreamHandler()  # 콘솔에도 출력
    ]
)

previous_return_value = None
def job():
  global previous_return_value
  try:
    previous_return_value = mongo(previous_return_value)
    mysql()
    success_message = f'Job success\nprevious_return_value: {str(previous_return_value)}'
    send_sync_message(success_message)
  except Exception as e:
    error_message = f"Job error: {str(e)}"
    logging.error(error_message)
    send_sync_message(error_message)

schedule.every().day.at('22:55').do(job)

while True:
  try:
    schedule.run_pending()
    time.sleep(1)
  except Exception as e:
    error_message = f'Scheduler error: {str(e)}'
    logging.error(error_message)
    send_sync_message(error_message)
    time.sleep(10)