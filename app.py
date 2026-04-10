import streamlit as st
from state import init_state
from game_logic import initialize_game, handle_card_click, check_match
from leaderboard import save_score, load_leaderboard

# 페이지 기본 설정
st.set_page_config(page_title="카드 기억력 게임", page_icon="🃏", layout="centered")

st.title("🃏 카드 뒤집기 기억력 게임")
st.markdown("같은 이모지 카드를 찾아서 짝을 맞춰보세요! (4x4 짝맞추기)")

# 카드(버튼) 스타일: 게임판(column 내부)에 있는 버튼만 세로로 길게 & 글씨(이미지) 크게
st.markdown("""
<style>
/* 카드 보드(column 내부)의 버튼만 높이 지정 및 이미지 크기 최적화 */
div[data-testid="column"] div.stButton > button {
    height: 120px;
}
div[data-testid="column"] div.stButton > button p {
    font-size: 80px !important;
    line-height: 1.2;
}
</style>
""", unsafe_allow_html=True)

# 1. 상태 초기화 (처음 한 번만 실행됨)
init_state()

# 2. 게임 첫 시작 시 카드 초기화
if not st.session_state.cards:
    initialize_game()

# 시도 횟수 표시
st.subheader(f"🔄 시도 횟수: {st.session_state.flip_count}회")

# 게임 다시 시작 버튼
if st.button("새 게임 시작하기", type="primary"):
    initialize_game()
    st.rerun()

st.divider()

# 3. 4x4 보드 게임판 (Card Grid 렌더링)
# 4개의 열로 이루어진 그리드 생성
cols = st.columns(4)

# 16개의 카드를 순회하며 버튼 생성
for i in range(16):
    col_idx = i % 4
    
    with cols[col_idx]:
        # 카드가 매칭되었거나 현재 선택된 카드, 혹은 '기억하기(memorize)' 단계인 경우 이모지 표시
        is_memorize_phase = st.session_state.phase == "memorize"
        if i in st.session_state.matched or i in st.session_state.selected or is_memorize_phase:
            st.button(st.session_state.cards[i], key=f"card_{i}", disabled=True, use_container_width=True)
        else:
            # 뒷면 카드('❓') 생성 (클릭 시 이벤트 발생)
            if st.button("❓", key=f"card_{i}", use_container_width=True):
                handle_card_click(i)
                st.rerun() # 바로 화면 갱신하여 선택된 카드 표시

# 암기 시간 (게임 시작 시 5초 카운트다운 제한)
if st.session_state.phase == "memorize":
    import time
    countdown_placeholder = st.empty()
    for sec in range(5, 0, -1):
        countdown_placeholder.warning(f"👀 카드를 외워주세요! {sec}초 후에 카드가 뒤집힙니다...")
        time.sleep(1)
    
    # 5초가 지나면 플레이 모드로 전환하고 다시 렌더링
    st.session_state.phase = "play"
    st.rerun()

# 4. 카드 비교 로직 (play 모드일 때만)
if st.session_state.phase == "play":
    # 두 장을 선택한 경우 check_match가 이를 검증함 (1초 보여준 후 rerun 발생)
    check_match()

# 5. 게임 종료 메시지 및 리더보드
if st.session_state.game_over:
    st.divider()
    st.success("🎉 축하합니다! 모든 카드를 맞췄습니다!")
    
    # 점수 저장 및 폭죽 발생 (한 번만 실행되도록 score_saved 플래그 사용)
    if not st.session_state.score_saved:
        st.session_state.score_saved = True
        save_score(st.session_state.flip_count)
        st.balloons()

    st.subheader("🏆 명예의 전당 (Top 5)")
    st.caption("시도 횟수가 적을수록 순위가 높습니다.")
    
    # 최신 리더보드 로드
    top_scores = load_leaderboard()
    
    # 상위 5위 출력
    for idx, s in enumerate(top_scores):
        if s == st.session_state.flip_count:
            # 방금 달성한 점수 강조
            st.markdown(f"**{idx + 1}위: {s}회 (현재 내 기록! 🎉)**")
        else:
            st.markdown(f"**{idx + 1}위**: {s}회")
