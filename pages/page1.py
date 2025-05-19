import streamlit as st

# 제목
st.title("🍽️ 저녁 메뉴 추천기")
st.write("기분과 날씨에 맞는 오늘의 저녁 메뉴를 추천해드려요!")

# 사용자 입력
mood = st.selectbox("지금 기분은 어떤가요?", ["😊 기분 좋아요", "😐 그냥 그래요", "😢 우울해요", "😠 짜증나요"])
weather = st.selectbox("오늘 날씨는 어떤가요?", ["☀️ 맑음", "🌧️ 비", "⛅ 흐림", "❄️ 눈", "🌬️ 바람 많음"])

# 추천 로직
def recommend_menu(mood, weather):
    if mood == "😊 기분 좋아요":
        if weather == "☀️ 맑음":
            return "삼겹살과 냉면 어때요?"
        elif weather == "🌧️ 비":
            return "전과 막걸리 추천드려요!"
        elif weather == "❄️ 눈":
            return "샤브샤브가 딱이에요!"
        else:
            return "피자나 파스타도 좋겠네요!"
    elif mood == "😐 그냥 그래요":
        if weather == "🌧️ 비":
            return "따뜻한 라면에 김밥 조합은 어때요?"
        else:
            return "제육볶음 정식 추천해요."
    elif mood == "😢 우울해요":
        return "매콤한 떡볶이로 기분전환 해보세요!"
    elif mood == "😠 짜증나요":
        return "고기 먹고 스트레스 날려보세요! 고기 종류는 취향대로~"
    else:
        return "오늘은 배달음식이 정답일지도 몰라요 😊"

# 결과 출력
if st.button("🍴 메뉴 추천 받기"):
    recommendation = recommend_menu(mood, weather)
    st.success(f"👉 추천 메뉴: **{recommendation}**")
