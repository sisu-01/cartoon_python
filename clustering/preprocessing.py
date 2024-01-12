from mecab import MeCab

mecab = MeCab()

def main(list):
    # 형태소 목록
    documents = []
    for i in list:
        a = mecab.nouns(i[1])
        documents.append(mecab.nouns(i[1]))
    # 형태소 목록을 문장으로 변환
    document_sentences = [' '.join(doc) for doc in documents]
    
    return document_sentences