import random
import time
import streamlit as st

def initialize_game():
    """새로운 게임을 시작하기 위해 상태를 초기화하고 카드를 섞습니다."""
    st.session_state.matched = []
    st.session_state.selected = []
    st.session_state.game_over = False
    st.session_state.phase = "memorize"
    st.session_state.flip_count = 0
    st.session_state.score_saved = False
    
    # 8쌍의 예쁜 이모지 카드 준비 (총 16장)
    emojis = ['🐶', '🐱', '🐭', '🐹', '🐰', '🦊', '🐻', '🐼']
    cards = emojis * 2
    random.shuffle(cards)
    
    st.session_state.cards = cards

def handle_card_click(index):
    """사용자가 카드를 클릭했을 때의 동작을 처리합니다."""
    # 이미 맞춘 카드거나 이미 선택된 카드면 무시
    if index in st.session_state.matched or index in st.session_state.selected:
        return
        
    # 두 장이 이미 선택된 상태라면 더 이상 선택하지 못하게 방어
    if len(st.session_state.selected) >= 2:
        return

    # 카드 선택 상태에 추가
    st.session_state.selected.append(index)
    
    # 두 번째 카드를 뒤집었을 때(1번의 시도 처리) 횟수 1 증가
    if len(st.session_state.selected) == 2:
        st.session_state.flip_count += 1

def check_match():
    """두 장의 카드가 선택되었을 때 같은지 비교합니다."""
    if len(st.session_state.selected) == 2:
        idx1 = st.session_state.selected[0]
        idx2 = st.session_state.selected[1]
        
        # 카드가 같은지 확인
        if st.session_state.cards[idx1] == st.session_state.cards[idx2]:
            # 같으면 matched 목록에 추가하고 선택 상태 초기화
            st.session_state.matched.extend([idx1, idx2])
            st.session_state.selected = []
            
            # 모든 카드를 맞췄는지 확인 (16장)
            if len(st.session_state.matched) == len(st.session_state.cards):
                st.session_state.game_over = True
        else:
            # 다르면 잠시 보여주기 위해 1초 대기 후 상태 초기화 및 화면 다시 그리기
            time.sleep(1.0)
            st.session_state.selected = []
            st.rerun()
