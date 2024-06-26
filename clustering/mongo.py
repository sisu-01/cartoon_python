from utils.mongo import find_cartoons, reset_series, set_series
from clustering.preprocessing import main as pre_processing
from clustering.vectorization import main as vectorization
from clustering.clustering import main as clustering

eps = 0.16

def main(value):
  try:
    #작가의 만화 목록 불러오기
    cartoons = find_cartoons(value)
    if len(cartoons) >= 2:
      # 형태소 분리      
      data = pre_processing(cartoons)
      # 벡터화
      vectors = vectorization(data)
      # 군집화
      result = clustering(eps, vectors, cartoons)

      reset_result = reset_series(value)
      if reset_result:
        for i in result.keys():
          if i == -1:
            continue
          set_series(result[i])
  except Exception as e:
    print(e)
    # print('예외 유형:', type(e))  # 예외의 유형을 출력
    # print('예외 메시지:', e)  # 기본적인 예외 메시지를 출력
    # print('예외의 세부 정보:', e.args)  # 예외 메시지의 세부 정보