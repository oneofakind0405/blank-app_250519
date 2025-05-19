import streamlit as st
import random
import time
from datetime import datetime, timedelta

# 페이지 설정
st.set_page_config(page_title="방향키 게임", page_icon="🎮", layout="centered")

# 게임 상태 초기화
if 'game_state' not in st.session_state:
    st.session_state.game_state = 'menu'  # menu, playing, game_over
    st.session_state.score = 0
    st.session_state.current_direction = None
    st.session_state.direction_time = None
    st.session_state.level = 1
    st.session_state.lives = 3
    st.session_state.correct_streak = 0
    st.session_state.time_limit = 3.0  # 초기 시간 제한

# 방향 매핑
DIRECTIONS = {
    '↑': '위쪽 화살표 키 (↑)',
    '↓': '아래쪽 화살표 키 (↓)',
    '←': '왼쪽 화살표 키 (←)',
    '→': '오른쪽 화살표 키 (→)'
}

DIRECTION_COLORS = {
    '↑': '#FF6B6B',  # 빨강
    '↓': '#4ECDC4',  # 청록
    '←': '#45B7D1',  # 파랑
    '→': '#FFA07A'   # 주황
}

def generate_new_direction():
    """새로운 방향 생성"""
    direction = random.choice(list(DIRECTIONS.keys()))
    st.session_state.current_direction = direction
    st.session_state.direction_time = datetime.now()

def check_time_limit():
    """시간 제한 체크"""
    if st.session_state.direction_time:
        elapsed = datetime.now() - st.session_state.direction_time
        if elapsed.total_seconds() > st.session_state.time_limit:
            # 시간 초과
            st.session_state.lives -= 1
            st.session_state.correct_streak = 0
            if st.session_state.lives <= 0:
                st.session_state.game_state = 'game_over'
            else:
                generate_new_direction()
            return True
    return False

def handle_correct_answer():
    """정답 처리"""
    st.session_state.score += 10 * st.session_state.level
    st.session_state.correct_streak += 1
    
    # 레벨업 체크 (5연속 정답마다)
    if st.session_state.correct_streak % 5 == 0:
        st.session_state.level += 1
        st.session_state.time_limit = max(1.0, st.session_state.time_limit - 0.2)
    
    generate_new_direction()

def reset_game():
    """게임 초기화"""
    st.session_state.score = 0
    st.session_state.current_direction = None
    st.session_state.direction_time = None
    st.session_state.level = 1
    st.session_state.lives = 3
    st.session_state.correct_streak = 0
    st.session_state.time_limit = 3.0

# 메인 타이틀
st.title("🎮 방향키 게임")

# 게임 상태별 화면
if st.session_state.game_state == 'menu':
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        ### 게임 방법
        1. 화면에 나타나는 방향 화살표를 확인하세요
        2. 해당하는 방향키를 클릭하세요
        3. 시간 내에 정답을 맞춰야 합니다
        4. 5연속 정답마다 레벨이 오르고 속도가 빨라집니다
        5. 생명이 3개 있으며, 시간 초과나 오답 시 생명이 감소합니다
        """)
        
        if st.button("🎮 게임 시작", use_container_width=True):
            reset_game()
            st.session_state.game_state = 'playing'
            generate_new_direction()
            st.rerun()

elif st.session_state.game_state == 'playing':
    # 시간 제한 체크
    if not check_time_limit():
        # 게임 정보 표시
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("점수", st.session_state.score)
        
        with col2:
            st.metric("레벨", st.session_state.level)
        
        with col3:
            st.metric("생명", "❤️" * st.session_state.lives)
        
        with col4:
            if st.session_state.direction_time:
                elapsed = datetime.now() - st.session_state.direction_time
                remaining = max(0, st.session_state.time_limit - elapsed.total_seconds())
                st.metric("남은 시간", f"{remaining:.1f}초")
        
        st.markdown("---")
        
        # 현재 방향 표시
        if st.session_state.current_direction:
            direction = st.session_state.current_direction
            color = DIRECTION_COLORS[direction]
            
            st.markdown(f"""
            <div style="text-align: center; padding: 50px; background-color: {color}; 
                        border-radius: 20px; margin: 20px 0;">
                <h1 style="font-size: 150px; margin: 0; color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">
                    {direction}
                </h1>
                <h3 style="color: white; margin: 10px 0;">
                    {DIRECTIONS[direction]}를 누르세요!
                </h3>
            </div>
            """, unsafe_allow_html=True)
            
            # 방향키 버튼들
            st.markdown("<br>", unsafe_allow_html=True)
            
            # 위쪽 화살표
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button("↑", key="up", use_container_width=True):
                    if direction == "↑":
                        handle_correct_answer()
                        st.rerun()
                    else:
                        st.session_state.lives -= 1
                        st.session_state.correct_streak = 0
                        if st.session_state.lives <= 0:
                            st.session_state.game_state = 'game_over'
                        else:
                            generate_new_direction()
                        st.rerun()
            
            # 왼쪽, 아래쪽, 오른쪽 화살표
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col1:
                if st.button("←", key="left", use_container_width=True):
                    if direction == "←":
                        handle_correct_answer()
                        st.rerun()
                    else:
                        st.session_state.lives -= 1
                        st.session_state.correct_streak = 0
                        if st.session_state.lives <= 0:
                            st.session_state.game_state = 'game_over'
                        else:
                            generate_new_direction()
                        st.rerun()
            
            with col2:
                if st.button("↓", key="down", use_container_width=True):
                    if direction == "↓":
                        handle_correct_answer()
                        st.rerun()
                    else:
                        st.session_state.lives -= 1
                        st.session_state.correct_streak = 0
                        if st.session_state.lives <= 0:
                            st.session_state.game_state = 'game_over'
                        else:
                            generate_new_direction()
                        st.rerun()
            
            with col3:
                if st.button("→", key="right", use_container_width=True):
                    if direction == "→":
                        handle_correct_answer()
                        st.rerun()
                    else:
                        st.session_state.lives -= 1
                        st.session_state.correct_streak = 0
                        if st.session_state.lives <= 0:
                            st.session_state.game_state = 'game_over'
                        else:
                            generate_new_direction()
                        st.rerun()
        
        # 게임 일시정지 버튼
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("⏸️ 일시정지"):
                st.session_state.game_state = 'menu'
                st.rerun()
        
        with col2:
            if st.button("🔄 다시 시작"):
                reset_game()
                st.session_state.game_state = 'playing'
                generate_new_direction()
                st.rerun()
    
    else:
        st.rerun()

elif st.session_state.game_state == 'game_over':
    st.markdown("---")
    
    # 게임 오버 화면
    st.markdown("""
    <div style="text-align: center; padding: 30px; background-color: #FF6B6B; 
                border-radius: 20px; margin: 20px 0;">
        <h1 style="color: white; margin: 0;">🎮 게임 오버</h1>
        <h3 style="color: white; margin: 10px 0;">수고하셨습니다!</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # 최종 점수 표시
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("최종 점수", st.session_state.score)
    
    with col2:
        st.metric("도달 레벨", st.session_state.level)
    
    with col3:
        st.metric("최대 연속 정답", st.session_state.correct_streak)
    
    st.markdown("---")
    
    # 다시 시작 버튼
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 다시 플레이", use_container_width=True):
            reset_game()
            st.session_state.game_state = 'playing'
            generate_new_direction()
            st.rerun()
    
    with col2:
        if st.button("🏠 메인 메뉴", use_container_width=True):
            st.session_state.game_state = 'menu'
            st.rerun()

# 자동 새로고침 (게임 중일 때)
if st.session_state.game_state == 'playing':
    time.sleep(0.1)
    st.rerun()