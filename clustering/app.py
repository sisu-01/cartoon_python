from utils.db import create_connection_pool, run_sql
from clustering.preprocessing import main as pre_processing
from clustering.vectorization import main as vectorization
from clustering.clustering import main as clustering

def main(id, nickname):
    connection_pool = create_connection_pool()
    eps = 0.1

    # 작가의 만화 목록 불러오기
    list = run_sql(connection_pool, f'SELECT id, title, date, recommend FROM cartoon WHERE writer_id = \'{id}\' AND writer_nickname = \'{nickname}\' ORDER BY id ASC', None, True)
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
        insert_result = run_sql(connection_pool, insert_sql, None)
        if insert_result:
            update_sql = f"UPDATE cartoon SET series_id = {result[i]['id']} WHERE id IN ({result[i]['list'][:-1]})"
            run_sql(connection_pool, update_sql, None)