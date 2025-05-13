# import os
# import asyncio
# import logging
# from dotenv import load_dotenv
# from telegram import Bot
# from telegram.constants import ParseMode
# from telegram.error import TelegramError

# # 환경 변수 로드
# load_dotenv()

# # Telegram 설정
# my_id = os.getenv('ID')
# token = os.getenv('TOKEN')
# DEFAULT_MSG = "msg 변수가 비어이따"

# # 전역 Bot 인스턴스
# bot = Bot(token=token)

# # 비동기 메시지 전송
# async def send_message(msg, retries=3, delay=5):
#     for attempt in range(retries):
#         try:
#             await bot.send_message(chat_id=my_id, text=msg, parse_mode=ParseMode.HTML)
#             break
#         except TelegramError as e:
#             if attempt < retries - 1:
#                 await asyncio.sleep(delay)
#             else:
#                 logging.error(f"Telegram error after {retries} attempts: {str(e)}")
#         except Exception as e:
#             logging.error(f"Unexpected error: {str(e)}")
#             break

# # 동기에서 호출 가능한 wrapper
# def send_sync_message(msg=None):
#     try:
#         message = msg or DEFAULT_MSG
#         try:
#             # 이미 asyncio 루프가 돌고 있으면 create_task
#             loop = asyncio.get_running_loop()
#             asyncio.create_task(send_message(message))
#         except RuntimeError:
#             # 루프가 없으면 run
#             asyncio.run(send_message(message))
#     except Exception as e:
#         logging.error(f"Error in send_sync_message: {str(e)}")
