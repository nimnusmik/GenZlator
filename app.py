import streamlit as st
import requests

# Hugging Face API 토큰
HF_TOKEN = "YOUR_HUGGINGFACE_TOKEN"  # 여기에 Hugging Face API 토큰을 입력하세요.

model_url = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"

# 초기 세션 상태 설정
if "history" not in st.session_state:
    st.session_state.history = []

# 프롬프트 생성 함수
def slang_prompt(text, tone):
    return f"""Rewrite the following Korean sentence into Gen Z English slang. 
Tone: {tone}
Only return one short, modern, fun sentence.
No explanation, no extra text.
"{text}"
"""

# 응답 생성 함수
def generate_response(user_input, tone):
    prompt = slang_prompt(user_input, tone)
    
    response = requests.post(
    model_url,
    headers={"Authorization": f"Bearer {HF_TOKEN}"},
    json={"inputs": prompt}
    )
    
    print("Response Status Code:", response.status_code)
    print("Response Text:", response.text)

    # 응답 상태 코드 확인
    if response.status_code != 200:
        return f"⚠️ 모델 응답 오류 발생! (Status: {response.status_code}, Text: {response.text})"
    
    try:
        result = response.json()
        raw_output = result[0].get("generated_text", "").strip()

        # 불필요한 토큰 제거
        for trash in ["</s>", "[/INST]", "[/USER]", "[/ASST]", "<s>", "[INST]"]:
            raw_output = raw_output.replace(trash, "")

        # "Answer:", "Solution:" 등의 문장 앞부분 제거
        for prefix in ["Answer:", "Solution:", "Rewritten:", "Output:", "Original:"]:
            if prefix in raw_output:
                raw_output = raw_output.split(prefix)[-1].strip()

        return raw_output.split("\n")[0].strip().strip('"')

    except Exception as e:
        print("RESPONSE ERROR:", response.text)
        return "⚠️ 모델 응답 오류 발생!"

# Streamlit UI 시작
st.set_page_config(page_title="GenZlator", layout="centered")
st.title("🧃 GenZlator: 슬랭 챗봇 (Clean ver. 🚀)")

user_input = st.text_input("너 하고 싶은 말 적어봐 😎")
tone = st.selectbox("감성 스타일 고르기 🎭", ["Gen Z", "Formal", "Sarcastic", "Flirty"])

# "번역해줘" 버튼
if st.button("번역해줘 💬"):
    if user_input:
        with st.spinner("요즘 감성으로 바꾸는 중..."):
            result = generate_response(user_input, tone)
            st.session_state.history.append((user_input, result))

# "다시 생성" 버튼
if st.button("다시 생성 🔁") and user_input:
    with st.spinner("또 다른 요즘 버전 생성 중... 🎲"):
        result = generate_response(user_input, tone)
        st.session_state.history.append((user_input, result))

# 변환 내역 보여주기
if st.session_state.history:
    st.markdown("#### 🧾 변환 내역 (최신순)")
    for idx, (original, result) in enumerate(reversed(st.session_state.history[-5:]), 1):
        st.markdown(f"**{idx}. 원문:** {original}")
        st.markdown("👉 **변환 결과:**")
        st.code(result, language="markdown")

        # 복사 버튼
        st.markdown(
            f"""
            <button onclick="navigator.clipboard.writeText(`{result}`)">📋 복사하기</button>
            """,
            unsafe_allow_html=True
        )
        st.markdown("---")