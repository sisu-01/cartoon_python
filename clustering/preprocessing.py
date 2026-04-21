import re
from mecab import MeCab

mecab = MeCab()

# 1. 정규표현식 미리 컴파일 (반복문 안에서 매번 컴파일하지 않도록 하여 속도 향상)
# re.IGNORECASE 플래그를 사용하므로 대소문자(MANHWA, manhwa 등)를 중복해서 적을 필요가 없습니다.
PATTERN_KEYWORDS = re.compile(
    r'(완결|manhwa|manwha|\[완\]|만화|만와|망가|단편|프롤로그|에필로그|마지막화|完|후기|上|中|下|공지|휴재|bgm|ㅇㅎ|스압|재업)', 
    flags=re.IGNORECASE
)
PATTERN_EPISODE = re.compile(r'\d+\s*화?\s*$')
PATTERN_SPECIAL_CHARS = re.compile(r'[^가-힣a-zA-Z0-9\s]')
PATTERN_SPACES = re.compile(r'\s+') # 연속된 공백

def main(items):
    document_sentences = []
    
    for item in items:
        # 2. 안전한 데이터 추출 (예약어 list 대신 items 사용, try-except 대신 명시적 확인)
        if isinstance(item, dict) and 'title' in item:
            title = item['title']
        elif isinstance(item, (list, tuple)) and len(item) > 1:
            title = item[1]
        else:
            continue # 예상치 못한 데이터 형태면 건너뜀
            
        if not isinstance(title, str):
            title = str(title)

        # 3. 정규표현식을 이용한 문자열 전처리 (노이즈 제거)
        # 키워드 제거 -> 끝부분 화수 제거 -> 특수문자 공백 치환 -> 다중 공백 1개로 압축
        cleaned = PATTERN_KEYWORDS.sub('', title)
        cleaned = PATTERN_EPISODE.sub('', cleaned)
        cleaned = PATTERN_SPECIAL_CHARS.sub(' ', cleaned)
        cleaned = PATTERN_SPACES.sub(' ', cleaned).strip()

        # 4. MeCab 형태소(명사) 추출 및 문장 병합
        if cleaned: # 전처리 후 문자열이 남아있는 경우에만 실행
            morphemes = mecab.nouns(cleaned)
            document_sentences.append(' '.join(morphemes))
        else:
            document_sentences.append('') # 완전히 지워진 경우 빈 문자열 처리 (인덱스 유지용)
            
    return document_sentences