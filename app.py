from python.scraping.scraping import main

main(True)

# from db import get_cartoon_list
# from preprocessing import main as pre_processing
# from vectorization import main as vectorization
# from clustering import main as clustering

# #writer = '급양만와'
# #writer = '무선혜드셋'
# #writer = '찔찔이'
# #writer = '망푸'
# #writer = '금요정'
# #writer = '뭐가요'
# #writer = '칰타'
# #writer = 'devy'
# #writer = '위마'
# writer = '맛기니'
# #writer = '강아지강아지'
# #writer = '날걔란'
# #writer = '조예준'
# #writer = 'ㄴㅋㅍ'
# #writer = '지존박실짱짱맨'

# distance =5
# eps = 0.1

# list = get_cartoon_list(f'SELECT id, title FROM cartoon WHERE writer_nickname = \'{writer}\' ORDER BY id ASC;')
# data = pre_processing(list)
# vectors = vectorization(data)
# result = clustering(distance, eps, vectors, data)