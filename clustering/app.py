from utils.db import run_sql
from clustering.preprocessing import main as pre_processing
from clustering.vectorization import main as vectorization
from clustering.clustering import main as clustering

writer = '급양만와'
#writer = '무선혜드셋'
#writer = '찔찔이'
#writer = '망푸'
#writer = '금요정'
#writer = '뭐가요'
#writer = '칰타'
#writer = 'devy'
#writer = '위마'
#writer = '맛기니'
#writer = '강아지강아지'
#writer = '날걔란'
#writer = '조예준'
#writer = 'ㄴㅋㅍ'
#writer = '지존박실짱짱맨'

def main():
    eps = 0.3

    # 작가의 만화 목록 불러오기
    list = run_sql(f'SELECT id, title FROM cartoon WHERE writer_nickname = \'{writer}\' ORDER BY id ASC', None, True)
    # 형태소 분리
    data = pre_processing(list)
    # 벡터화
    vectors = vectorization(data)
    # 군집화
    result = clustering(eps, vectors, data)