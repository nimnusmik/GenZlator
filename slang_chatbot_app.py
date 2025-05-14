import streamlit as st
from openai import OpenAI, RateLimitError
from genz_utils import slang_translate
from dotenv import load_dotenv
import os

# .env 파일에서 API 키 로드
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.title("🧃 GenZlator: 슬랭 챗봇")

user_input = st.text_input("너 하고 싶은 말 적어봐 😎")
tone = st.selectbox("감성 스타일 고르기 🎭", ["Gen Z", "Formal", "Sarcastic", "Flirty"])

if st.button("번역해줘 💬"):
    if user_input:
        prompt = slang_translate(user_input, tone)
        with st.spinner("슬랭으로 바꾸는 중..."):
            try:
                # 최신 OpenAI API 호출
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You're a Gen Z slang expert."},
                        {"role": "user", "content": prompt}
                    ]
                )
                answer = response.choices[0].message.content
                st.success("💬 GenZlator의 번역:")
                st.write(answer)
            except RateLimitError as e:
                st.error("Quota exceeded or rate limit hit. Please check your OpenAI plan or try again later.")
                st.info("Details: https://platform.openai.com/docs/guides/error-codes/api-errors")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("먼저 입력해줘!")
