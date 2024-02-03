from mecab import MeCab

mecab = MeCab()

# 제거 단어
exclude_words = ['MANHWA', 'manhwa', 'MANWHA', 'manwha', '만화', '만와', '망가', '단편', 
                 '프롤로그', '에필로그', '마지막화', '完', '후기', '上', '中', '下',
                 '공지', '휴재', 'bgm', 'BGM', 'ㅇㅎ', '스압', '재업']

def main(list):
    # 형태소 목록
    documents = []
    for i in list:
        morphemes = mecab.nouns(i[1])
        morphemes = [morpheme for morpheme in morphemes if morpheme not in exclude_words]
        documents.append(morphemes)
    # 형태소 목록을 문장으로 변환
    document_sentences = [' '.join(doc) for doc in documents]
    
    return document_sentences