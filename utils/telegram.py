import os
from dotenv import load_dotenv
import asyncio
import telegram
import time

# 환경 변수 로드
load_dotenv()

# ID와 토큰 가져오기
my_id = os.getenv('ID')
token = os.getenv('TOKEN')
bot = telegram.Bot(token=token)

# 기본 메시지 설정
DEFAULT_MSG = "msg 변수가 비어이따"

async def send_message(msg, retries=3, delay=5):
    for attempt in range(retries):
        try:
            await bot.send_message(chat_id=my_id, text=msg)  # 타임아웃 설정
            break  # 성공하면 반복 종료
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(delay)  # 지연 후 재시도
            else:
                print(f'telegram error: {str(e)}')

def send_sync_message(msg=None):
    try:
        # 이미 실행 중인 이벤트 루프가 있는지 확인
        if asyncio.get_event_loop().is_running():
            # 비동기 함수를 바로 호출
            asyncio.create_task(send_message(msg or DEFAULT_MSG))
        else:
            # 새 이벤트 루프 생성 및 실행
            asyncio.run(send_message(msg or DEFAULT_MSG))
    except Exception as e:
        print(f"에러 in send_sync_message: {e}")