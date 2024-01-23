from sklearn.feature_extraction.text import TfidfVectorizer

def main(data):
    # TF-IDF 행렬 생성
    tfidf_vectorizer = TfidfVectorizer(min_df = 2)
    tfidf_vectorizer.fit(data)
    vector = tfidf_vectorizer.transform(data)

    return vector