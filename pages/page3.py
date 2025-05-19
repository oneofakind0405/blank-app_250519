import streamlit as st
import openai

# OpenAI API Key 설정
openai.api_key = st.secrets["openai"]["api_key"]

# 앱 제목
st.title("🐶 쿠키랑 수다 떨기")
st.write("반려견 쿠키에게 편하게 말 걸어보세요! (쿠키는 반말로 대답해요 🐾)")

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "너는 귀엽고 장난기 많은 강아지 '쿠키'야. 항상 반말로, 친근하고 유쾌하게 대답해."}
    ]

# 사용자 입력
user_input = st.text_input("너: ", key="user_input")

# 응답 처리
if user_input:
    # 사용자 메시지 저장
    st.session_state.messages.append({"role": "user", "content": user_input})

    # OpenAI API 호출
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.messages
    )

    # 쿠키 응답 저장
    reply = response.choices[0].message["content"]
    st.session_state.messages.append({"role": "assistant", "content": reply})

# 대화 출력
st.markdown("### 💬 대화 내용")
for msg in st.session_state.messages[1:]:
    speaker = "너" if msg["role"] == "user" else "🐶 쿠키"
    st.markdown(f"**{speaker}:** {msg['content']}")
