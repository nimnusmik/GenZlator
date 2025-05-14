import streamlit as st
import requests

# Hugging Face API 토큰
HF_TOKEN = "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"

# 초기 세션 상태 설정
if "history" not in st.session_state:
    st.session_state.history = []

# 슬랭 프롬프트 생성 함수
def slang_prompt(text, tone):
    return f"""Rewrite the sentence below in a {tone} style using Gen Z slang. 
Return ONLY the rewritten sentence, NOTHING else. No explanations, no extra text, no quotes.
Use trendy slang like 'vibes', 'lit', 'slay', 'bet', 'fam', etc.

Example:
Original: 배고프다
Rewritten: Starvin' vibes, fam

Original: {text}
Rewritten:"""

# 모델 응답 생성 함수
def generate_response(user_input, tone):
    prompt = slang_prompt(user_input, tone)
    response = requests.post(
        "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta",
        headers={"Authorization": f"Bearer {HF_TOKEN}"},
        json={
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 50,
                "temperature": 0.7,
                "return_full_text": False
            }
        }
    )

    if response.status_code == 200:
        result = response.json()
        raw_output = result[0]["generated_text"]

        # 프롬프트와 불필요한 토큰 제거
        for trash in ["</s>", "[/INST]", "[/USER]", "[/ASST]", "<s>", "[INST]", prompt]:
            raw_output = raw_output.replace(trash, "")

        # "Rewritten:" 이후만 추출
        if "Rewritten:" in raw_output:
            raw_output = raw_output.split("Rewritten:")[-1].strip()

        # 추가 접두사 제거
        for prefix in ["Answer:", "Your answer:"]:
            raw_output = raw_output.replace(prefix, "").strip()

        return raw_output.strip().strip('"').strip()
    else:
        return f"⚠️ 오류 발생! 상태 코드: {response.status_code}"

# UI 시작
st.set_page_config(page_title="GenZlator", layout="centered")
st.title("🧃 GenZlator: 슬랭 챗봇 (FREE ver. 🚀)")

user_input = st.text_input("너 하고 싶은 말 적어봐 😎")
tone = st.selectbox("감성 스타일 고르기 🎭", ["Gen Z", "Formal", "Sarcastic", "Flirty"])

# 번역 버튼
if st.button("번역해줘 💬"):
    if user_input:
        with st.spinner("요즘 감성으로 바꾸는 중... 😎"):
            result = generate_response(user_input, tone)
            st.session_state.history.append((user_input, result))

# 다시 생성 버튼
if st.button("다시 생성 🔁") and user_input:
    with st.spinner("또 다른 요즘 버전 생성 중... 🎲"):
        result = generate_response(user_input, tone)
        st.session_state.history.append((user_input, result))

# 대화 히스토리 보여주기
if st.session_state.history:
    st.markdown("## 🧾 변환 내역 (최신순)")
    for idx, (original, result) in enumerate(reversed(st.session_state.history[-5:]), 1):
        st.markdown(f"**{idx}. 원문:** {original}")
        st.markdown(f"👉 변환 결과:")
        st.code(result, language="markdown")

        # 복사 버튼
        st.markdown(
            f"""
            <button onclick="navigator.clipboard.writeText(`{result}`)">📋 복사하기</button>
            """,
            unsafe_allow_html=True
        )
        st.markdown("---")

# 디버깅 정보
if st.checkbox("디버깅 정보 보기"):
    st.write("프롬프트:", slang_prompt(user_input, tone) if user_input else "입력 없음")
    st.write("HF_TOKEN 상태:", "설정됨" if HF_TOKEN else "설정 필요")