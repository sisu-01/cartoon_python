from scraping.scraping import main as mysql
from scraping.new import main as mongo
from telegram import send_sync_message
import schedule
import time

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
    send_sync_message(error_message)

schedule.every().day.at('23:00').do(job)

while True:
  try:
    schedule.run_pending()
    time.sleep(1)
  except Exception as e:
    error_message = f'Scheduler error: {str(e)}'
    send_sync_message(error_message)
    time.sleep(10)