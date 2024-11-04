import os
from dotenv import load_dotenv
import asyncio
import telegram

# 환경 변수 로드
load_dotenv()

# ID와 토큰 가져오기
my_id = os.getenv('ID')
token = os.getenv('TOKEN')
bot = telegram.Bot(token=token)

# 기본 메시지 설정
DEFAULT_MSG = "msg 변수가 비어이따"

async def send_message(msg):
    await bot.send_message(chat_id=my_id, text=msg)

def send_sync_message(msg=None):
    asyncio.run(send_message(msg or DEFAULT_MSG))
