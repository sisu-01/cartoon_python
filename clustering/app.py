from utils.db import create_connection_pool, run_sql
from clustering.preprocessing import main as pre_processing
from clustering.vectorization import main as vectorization
from clustering.clustering import main as clustering

def reset_series(connection_pool, writer_id, writer_nickname):
    set_null_result = run_sql(connection_pool, f'UPDATE cartoon SET series_id = null WHERE writer_id = \'{writer_id}\' AND writer_nickname = \'{writer_nickname}\';', None)
    if set_null_result:
        delete_series_result = run_sql(connection_pool, f'DELETE FROM series WHERE writer_id = \'{writer_id}\' AND writer_nickname = \'{writer_nickname}\'', None)
        if delete_series_result:
            return True
    return False

def set_series(connection_pool, writer_id, writer_nickname, values):
    insert_sql = (
        'INSERT INTO series (id, title, writer_id, writer_nickname, count, last_update, average) '
        'VALUES({}, \'{}\', \'{}\', \'{}\', {}, \'{}\', {})'
    ).format(
        values['id'],
        values['title'],
        writer_id, writer_nickname,
        values['count'],
        values['date'],
        round(values['recommend'] / values['count'])
    )
    insert_result = run_sql(connection_pool, insert_sql, None)
    if insert_result:
        update_sql = f"UPDATE cartoon SET series_id = {values['id']} WHERE id IN ({values['list'][:-1]})"
        run_sql(connection_pool, update_sql, None)

def main(writer_id, writer_nickname):
    connection_pool = create_connection_pool()
    eps = 0.1

    # 작가의 만화 목록 불러오기
    list = run_sql(connection_pool, f'SELECT id, title, date, recommend FROM cartoon WHERE writer_id = \'{writer_id}\' AND writer_nickname = \'{writer_nickname}\' ORDER BY id ASC', None, True)
    # 형태소 분리
    data = pre_processing(list)
    # 벡터화
    vectors = vectorization(data)
    # 군집화
    result = clustering(eps, vectors, list)

    if reset_series(connection_pool, writer_id, writer_nickname):
        for i in result.keys():
            if i == -1:
                continue
            set_series(connection_pool, writer_id, writer_nickname, result[i])

"""
class 어쩌구():
    def __init__(self, *args, **kwargs):
        self.writer_id = 어쩌구
        self.writer_nickname = 어쩌구
    def clustering():
        어쩌구
    def reset_series():
    def set_series():
"""