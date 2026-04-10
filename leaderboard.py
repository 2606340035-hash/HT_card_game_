import json
import os

FILE_NAME = "leaderboard.json"

def load_leaderboard():
    """leaderboard.json 파일에서 순위 데이터를 불러옵니다."""
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_score(score):
    """새로운 점수(시도 횟수)를 추가하고, 오름차순(적은 수)으로 정렬하여 5위까지만 저장합니다."""
    scores = load_leaderboard()
    scores.append(score)
    
    # 횟수가 적을수록 상위권이므로 오름차순 정렬
    scores.sort()
    
    # 1위부터 5위까지만 유지
    top_5 = scores[:5]
    
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(top_5, f, ensure_ascii=False, indent=4)
        
    return top_5
