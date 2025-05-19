
import streamlit as st
import streamlit.components.v1 as components
import random
import time
from datetime import datetime

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
    st.session_state.last_key_pressed = None
    st.session_state.game_start_time = None

# 방향 매핑
DIRECTIONS = {
    '↑': 'ArrowUp',
    '↓': 'ArrowDown',
    '←': 'ArrowLeft',
    '→': 'ArrowRight'
}

DIRECTION_NAMES = {
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

def handle_key_press(key_pressed):
    """키 입력 처리"""
    if st.session_state.game_state != 'playing' or not st.session_state.current_direction:
        return
    
    expected_key = DIRECTIONS[st.session_state.current_direction]
    
    if key_pressed == expected_key:
        # 정답
        st.session_state.score += 10 * st.session_state.level
        st.session_state.correct_streak += 1
        
        # 레벨업 체크 (5연속 정답마다)
        if st.session_state.correct_streak % 5 == 0:
            st.session_state.level += 1
            st.session_state.time_limit = max(1.0, st.session_state.time_limit - 0.2)
        
        generate_new_direction()
    else:
        # 오답
        st.session_state.lives -= 1
        st.session_state.correct_streak = 0
        if st.session_state.lives <= 0:
            st.session_state.game_state = 'game_over'
        else:
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
    st.session_state.last_key_pressed = None
    st.session_state.game_start_time = datetime.now()

# 키보드 이벤트 처리를 위한 JavaScript 컴포넌트
def keyboard_listener():
    keyboard_js = """
    <div id="keyboard-listener" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1;"></div>
    <script>
    let lastKeyTime = 0;
    
    document.addEventListener('keydown', function(event) {
        // 중복 키 입력 방지 (100ms 내 같은 키)
        const currentTime = Date.now();
        if (currentTime - lastKeyTime < 100) return;
        lastKeyTime = currentTime;
        
        if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'].includes(event.key)) {
            event.preventDefault();
            
            // Streamlit에 키 입력 전송
            const eventData = {
                key: event.key,
                timestamp: currentTime
            };
            
            // 키 입력을 Streamlit 세션에 저장
            window.parent.postMessage({
                type: 'keypress',
                key: event.key
            }, '*');
            
            // 키 입력 시각적 피드백
            const body = document.body;
            body.style.backgroundColor = '#f0f0f0';
            setTimeout(() => {
                body.style.backgroundColor = '';
            }, 100);
        }
    });
    
    // 페이지 포커스 보장
    window.focus();
    document.getElementById('keyboard-listener').focus();
    </script>
    """
    return keyboard_js

# 메인 타이틀
st.title("🎮 방향키 게임")

# 키보드 리스너 추가 (게임 중일 때만)
if st.session_state.game_state == 'playing':
    components.html(keyboard_listener(), height=0)
    
    # 키 입력 확인 (JavaScript에서 직접 처리하므로 여기서는 시간 체크만)
    if check_time_limit():
        st.rerun()

# 게임 상태별 화면
if st.session_state.game_state == 'menu':
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        ### 🎮 게임 방법
        1. 화면에 나타나는 방향 화살표를 확인하세요
        2. **키보드의 해당 방향키**를 누르세요 (↑ ↓ ← →)
        3. 시간 내에 정답을 맞춰야 합니다
        4. 5연속 정답마다 레벨이 오르고 속도가 빨라집니다
        5. 생명이 3개 있으며, 시간 초과나 오답 시 생명이 감소합니다
        
        ### ⚠️ 주의사항
        - 게임 시작 후 페이지를 클릭하여 키보드 입력을 활성화하세요
        - 브라우저 창이 활성 상태여야 키 입력이 감지됩니다
        """)
        
        if st.button("🎮 게임 시작", use_container_width=True):
            reset_game()
            st.session_state.game_state = 'playing'
            generate_new_direction()
            st.rerun()

elif st.session_state.game_state == 'playing':
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
    
    # 키보드 입력 안내
    st.markdown("""
    <div style="text-align: center; background-color: #f8f9fa; padding: 10px; border-radius: 5px; margin-bottom: 20px;">
        <strong>💡 이 영역을 클릭한 후 키보드 방향키를 사용하세요!</strong>
    </div>
    """, unsafe_allow_html=True)
    
    # 현재 방향 표시
    if st.session_state.current_direction:
        direction = st.session_state.current_direction
        color = DIRECTION_COLORS[direction]
        
        st.markdown(f"""
        <div style="text-align: center; padding: 80px; background-color: {color}; 
                    border-radius: 20px; margin: 20px 0; cursor: pointer;"
             onclick="this.focus();" tabindex="0">
            <h1 style="font-size: 200px; margin: 0; color: white; text-shadow: 3px 3px 6px rgba(0,0,0,0.5);">
                {direction}
            </h1>
            <h2 style="color: white; margin: 20px 0; font-size: 24px;">
                키보드 {DIRECTION_NAMES[direction]}를 누르세요!
            </h2>
            <p style="color: white; font-size: 16px; opacity: 0.9;">
                이 영역을 클릭하고 방향키를 누르세요
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # 게임 컨트롤 버튼
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
    
    # 키보드 이벤트 처리를 위한 숨겨진 JavaScript
    key_handler_js = f"""
    <script>
    let gameActive = true;
    
    function handleKeyPress(event) {{
        if (!gameActive) return;
        
        const allowedKeys = ['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'];
        if (allowedKeys.includes(event.key)) {{
            event.preventDefault();
            
            // Streamlit 콜백 실행
            fetch(window.location.href, {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json',
                }},
                body: JSON.stringify({{
                    key: event.key,
                    action: 'keypress'
                }})
            }}).then(() => {{
                // 페이지 새로고침하여 상태 업데이트
                window.location.reload();
            }});
        }}
    }}
    
    document.addEventListener('keydown', handleKeyPress);
    
    // 페이지 포커스
    window.focus();
    </script>
    """
    
    # 실제 키 처리 (URL 파라미터로 키 입력 감지)
    try:
        # URL 파라미터에서 키 입력 확인
        query_params = st.query_params
        if 'key' in query_params:
            key_pressed = query_params['key']
            # URL 파라미터 클리어
            st.query_params.clear()
            handle_key_press(key_pressed)
            st.rerun()
    except:
        pass
    
    # 자동 새로고침
    time.sleep(0.1)
    st.rerun()

elif st.session_state.game_state == 'game_over':
    st.markdown("---")
    
    # 게임 오버 화면
    st.markdown("""
    <div style="text-align: center; padding: 40px; background-color: #FF6B6B; 
                border-radius: 20px; margin: 20px 0;">
        <h1 style="color: white; margin: 0; font-size: 48px;">🎮 게임 오버</h1>
        <h3 style="color: white; margin: 10px 0;">수고하셨습니다!</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # 최종 점수 표시
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("최종 점수", f"{st.session_state.score:,}")
    
    with col2:
        st.metric("도달 레벨", st.session_state.level)
    
    with col3:
        st.metric("최대 연속 정답", st.session_state.correct_streak)
    
    # 게임 시간 계산
    if st.session_state.game_start_time:
        game_duration = datetime.now() - st.session_state.game_start_time
        minutes = int(game_duration.total_seconds() // 60)
        seconds = int(game_duration.total_seconds() % 60)
        st.markdown(f"<p style='text-align: center; font-size: 18px;'>게임 시간: {minutes}분 {seconds}초</p>", 
                   unsafe_allow_html=True)
    
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