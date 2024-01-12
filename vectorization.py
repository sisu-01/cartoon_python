from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

def main(data):
    # TF-IDF 행렬 생성
    tfidf_vectorizer = TfidfVectorizer(min_df = 2)
    tfidf_vectorizer.fit(data)
    vector = tfidf_vectorizer.transform(data)
    #vector = np.array(temp) # Normalizer를 이용해 변환된 벡터

    return vector