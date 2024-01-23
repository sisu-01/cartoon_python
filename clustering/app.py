from utils.db import run_sql
from clustering.preprocessing import main as pre_processing
from clustering.vectorization import main as vectorization
from clustering.clustering import main as clustering

writer = '급양만와'

def main():
    eps = 0.1

    # 작가의 만화 목록 불러오기
    list = run_sql(f'SELECT id, title, date, recommend FROM cartoon WHERE writer_nickname = \'{writer}\' ORDER BY id ASC', None, True)
    # 형태소 분리
    data = pre_processing(list)
    # 벡터화
    vectors = vectorization(data)
    # 군집화
    result = clustering(eps, vectors, list)

    for i in result.keys():
        if i == -1:
            continue
        insert_sql = (
            'INSERT INTO series (id, title, count, last_update, average) '
            'VALUES({}, \'{}\', {}, \'{}\', {})'
        ).format(
            result[i]['id'],
            result[i]['title'],
            result[i]['count'],
            result[i]['date'],
            round(result[i]['recommend'] / result[i]['count'])
        )
        insert_result = run_sql(insert_sql, None)
        if insert_result:
            update_sql = f"UPDATE cartoon SET series_id = {result[i]['id']} WHERE id IN ({result[i]['list'][:-1]})"
            run_sql(update_sql, None)