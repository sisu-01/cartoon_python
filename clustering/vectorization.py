from sklearn.feature_extraction.text import TfidfVectorizer

def main(data):
    # TF-IDF 행렬 생성
    # min_df 용어가 어휘에 포함되기 위해 출현해야 하는 최소 문서 수
    # max_df 용어가 어휘에 포함되기 위해 출현할 수 있는 최대 문서 수
    # min_df가 커질수록 유니크, max_df가 작아질 수록 유니크
    # min_df = 2, max_df = 0.8은 최소 문서 두 개에 포함되고 전체 문서 80퍼센트 이하에만 나타나야 함
    tfidf_vectorizer = TfidfVectorizer(min_df = 3)
    tfidf_vectorizer.fit(data)
    vector = tfidf_vectorizer.transform(data)

    return vector