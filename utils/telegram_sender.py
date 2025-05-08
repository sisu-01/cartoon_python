import os
import asyncio
import logging
from dotenv import load_dotenv
from telegram import Bot
from telegram.constants import ParseMode
from telegram.error import TelegramError

# 환경 변수 로드
load_dotenv()

# ID와 토큰 가져오기
my_id = os.getenv('ID')
token = os.getenv('TOKEN')
# Bot 인스턴스 생성
bot = Bot(token=token)

# 기본 메시지 설정
DEFAULT_MSG = "msg 변수가 비어이따"

async def send_message(msg, retries=3, delay=5):
    for attempt in range(retries):
        try:
            await bot.send_message(chat_id=my_id, text=msg, parse_mode=ParseMode.HTML)
            break  # 성공하면 반복 종료
        except TelegramError as e:
            if attempt < retries - 1:
                await asyncio.sleep(delay)
            else:
                logging.error(f"Telegram error after {retries} attempts: {str(e)}")
        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            break

def send_sync_message(msg=None):
    try:
        message = msg or DEFAULT_MSG
        try:
            loop = asyncio.get_running_loop()
            asyncio.create_task(send_message(message))
        except RuntimeError:
            asyncio.run(send_message(message))
    except Exception as e:
        logging.error(f"Error in send_sync_message: {str(e)}")
