from utils.db import create_connection_pool, run_sql
from clustering.preprocessing import main as pre_processing
from clustering.vectorization import main as vectorization
from clustering.clustering import main as clustering

def reset_series(connection_pool, id_nickname):
    id_nickname
    update_sql = (
        'UPDATE cartoon SET series_id = null '
        'WHERE writer_id = %s AND writer_nickname = %s'
    )
    set_null_result = run_sql(connection_pool, update_sql, id_nickname)
    if set_null_result:
        delete_sql = (
            'DELETE FROM series '
            'WHERE writer_id = %s AND writer_nickname = %s'
        )
        delete_series_result = run_sql(connection_pool, delete_sql, id_nickname)
        if delete_series_result:
            return True
    return False

def set_series(connection_pool, id_nickname, values):
    insert_sql = (
        'INSERT INTO series (id, title, writer_id, writer_nickname, count, last_update, average) '
        'VALUES(%s, %s, %s, %s, %s, %s, %s)'
    )
    series_values = (
        values['id'],
        values['title'],
        id_nickname[0], id_nickname[1],
        values['count'],
        values['date'],
        round(values['recommend'] / values['count'])
    )
    insert_result = run_sql(connection_pool, insert_sql, series_values)
    if insert_result:
        update_sql = (
            f'UPDATE cartoon SET series_id = %s '
            f'WHERE id IN ({", ".join(["%s"] * len(values["list"]))})'
        )
        run_sql(connection_pool, update_sql, [values['id']]+values["list"])

import traceback


def main(connection_pool, id_nickname):
    try:
        eps = 0.16

        # 작가의 만화 목록 불러오기
        select_sql = (
            'SELECT id, title, date, recommend FROM cartoon '
            'WHERE writer_id = %s AND writer_nickname = %s ORDER BY id ASC'
        )
        list = run_sql(connection_pool, select_sql, id_nickname, True)
        if len(list) >= 2:
            # 형태소 분리
            data = pre_processing(list)
            # 벡터화
            vectors = vectorization(data)
            # 군집화
            result = clustering(eps, vectors, list)

            if reset_series(connection_pool, id_nickname):
                for i in result.keys():
                    if i == -1:
                        continue
                    set_series(connection_pool, id_nickname, result[i])
    except Exception as e:
        print('clustering.app main() encountered an error:')
        print('Error message:', e)
        print('Traceback:')
        traceback.print_exc()

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