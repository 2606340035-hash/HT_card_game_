import streamlit as st

def init_state():
    """게임에 필요한 초기 상태를 설정합니다."""
    if "cards" not in st.session_state:
        st.session_state.cards = []
    
    if "selected" not in st.session_state:
        st.session_state.selected = []
        
    if "matched" not in st.session_state:
        st.session_state.matched = []
        
    if "game_over" not in st.session_state:
        st.session_state.game_over = False
        
    if "phase" not in st.session_state:
        st.session_state.phase = "memorize"
        
    if "flip_count" not in st.session_state:
        st.session_state.flip_count = 0
        
    if "score_saved" not in st.session_state:
        st.session_state.score_saved = False
