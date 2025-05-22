import streamlit as st
import deepl
from openai import OpenAI
import random

# Custom CSS for UI enhancement
st.markdown("""
<style>
/* Import Google Font (Poppins for a trendy vibe) */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

/* Global styles */
body {
    font-family: 'Poppins', sans-serif;
    background: linear-gradient(135deg, #f5f7fa, #c3cfe2);
}

/* Title styling */
h1 {
    color: #6B48FF;
    text-align: center;
    font-weight: 600;
    font-size: 2.5em;
    margin-bottom: 0.5em;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
}

/* Card-like section for inputs and outputs */
.stTextArea, .stButton, .stSlider, .stMarkdown {
    background: #ffffff;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    margin-bottom: 20px;
}

/* Button styling with hover effect */
button {
    background: linear-gradient(45deg, #FF6F91, #FF9671);
    color: white !important;
    border: none;
    border-radius: 10px;
    padding: 10px 20px;
    font-weight: 600;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

button:hover {
    transform: scale(1.05);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

/* Subheader styling */
h2 {
    color: #FF6F91;
    font-size: 1.5em;
    margin-top: 20px;
}

/* Sidebar styling */
.stSidebar {
    background: #2E2E2E;
    color: white;
}

.stSidebar h3 {
    color: #FF9671;
}

/* Text styling */
p, .stMarkdown {
    color: #333;
    font-size: 1.1em;
}

/* Footer styling */
footer {
    text-align: center;
    color: #6B48FF;
    font-size: 1em;
    margin-top: 30px;
}
</style>
""", unsafe_allow_html=True)

# Initialize DeepL and OpenAI clients
try:
    deepl_auth_key = st.secrets["DEEPL_AUTH_KEY"]
    openai_api_key = st.secrets["OPENAI_API_KEY"]
except KeyError as e:
    st.error(f"API 키가 설정되지 않았습니다: {str(e)}. .streamlit/secrets.toml 파일에 DEEPL_AUTH_KEY와 OPENAI_API_KEY를 확인하세요.")
    st.stop()

# Debug: Display API keys in sidebar
st.sidebar.write("### Debug: API Keys")
st.sidebar.write(f"DeepL Key: {'Set' if deepl_auth_key else 'Not set'}")
st.sidebar.write(f"OpenAI Key: {'Set' if openai_api_key else 'Not set'}")

translator = deepl.Translator(deepl_auth_key)
client = OpenAI(api_key=openai_api_key)

# Dictionary of common 20s slang and casual expressions
slang_dict = {
    "cool": ["lit", "dope", "fire", "chill", "valid"],
    "good": ["awesome", "sick", "bomb", "tight", "clean"],
    "great": ["bussin'", "elite", "on point", "goated"],
    "amazing": ["slaps", "next-level", "cracked", "top-tier"],
    "friend": ["homie", "bro", "dude", "fam", "bestie"],
    "happy": ["stoked", "pumped", "vibin'", "feelin’ it"],
    "bad": ["whack", "lame", "trash", "mid", "sus"],
    "really": ["hella", "super", "mad", "lowkey", "highkey"],
    "yes": ["yep", "yup", "bet", "fr", "facts", "say less", "big yes"],
    "no": ["nah", "nope", "naw", "hard pass"],
    "eat": ["grub", "munch", "chow down", "smash food"],
    "hi": ["yo", "what's good", "sup"],
    "boring": ["dry", "dead", "stale"],
    "angry": ["pressed", "salty", "heated"],
    "weird": ["sus", "cringe", "off", "sketchy"],
    "person": ["rando", "main character", "baddie", "NPC"],
    "smart": ["big brain", "galaxy brain", "200 IQ"],
    "dumb": ["NPC", "goofy", "clown", "slow af"],
    "sad": ["down bad", "in my feels", "lowkey hurt"],
    "excited": ["hyped", "juiced", "geeked"],
    "nervous": ["shakin’", "tweakin’", "buggin’"],
    "confident": ["slayin’", "poppin’ off", "unbothered"],
    "sleep": ["catch some Z’s", "crash", "knock out"],
    "say": ["drop", "spit", "hit me with it"],
    "go": ["dip", "bounce", "slide", "head out"],
    "talk": ["spill", "chat", "holla", "link up"],
    "leave me alone": ["chill", "back off", "get off my case"],
    "like": ["vibe with", "rock with", "mess with"],
    "love": ["obsessed", "can’t", "stan", "heart eyes"],
    "hate": ["over it", "can’t deal", "ick"],
    "post": ["drop", "flex", "throw up"],
    "support": ["hype up", "gas up", "show love"]
}

# Function to rewrite translation in Gen Z style with adjustable slang intensity
def rewrite_to_genz_style(text, slang_intensity):
    intensity_description = "minimal" if slang_intensity <= 3 else "moderate" if slang_intensity <= 7 else "heavy"
    prompt = f"""
    Rewrite the following sentence in a casual, Gen Z style using slang and expressions popular among 20-somethings in 2025. 
    Use {intensity_description} slang based on this intensity level ({slang_intensity}/10). 
    For minimal, use very light slang or none; for moderate, use some trendy words; for heavy, use lots of slang like 'lit', 'vibes', 'fam', 'slay', 'bet', 'yo', 'no cap', 'sksksk', etc. 
    Keep the tone fun and vibey:
    "{text}"
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a Gen Z slang expert who rewrites sentences to sound trendy and casual."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=50,
            temperature=0.6
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"LLM 에러: {str(e)}. OpenAI 크레딧이나 플랜 확인 필요: https://platform.openai.com/account/billing"

# Function to suggest slang based on translated text
def suggest_slang(text):
    used_words = [key for key in slang_dict if key in text.lower()]
    suggestions = []
    if used_words:
        for word in used_words:
            suggestions.append(f"**'{word}'** 대신 사용할 수 있는 슬랭: {', '.join(slang_dict[word])}")
    else:
        suggestions.append("이 문장에 딱 맞는 슬랭을 찾지 못했어요. 😅")
    return suggestions

# Streamlit app
st.title("🇰🇷 ➡️ 🇺🇸 Gen Z Slang Translator")
st.write("한국어를 입력하면 20대 스타일의 영어로 번역해드려요! 💜")

# Input text
korean_input = st.text_area("한국어 문장을 입력하세요:", height=100, value="안녕, 나는 한국인이야")

# Slang intensity slider
slang_intensity = st.slider("Gen Z 슬랭 강도 조절", min_value=0, max_value=10, value=5, step=1)
st.write(f"슬랭 강도: {slang_intensity}/10")

if st.button("번역하기"):
    if korean_input:
        try:
            # Translate Korean to English using DeepL
            result = translator.translate_text(korean_input, source_lang="KO", target_lang="EN-US")
            translated_text = result.text
            
            # Rewrite in Gen Z style with adjustable intensity
            genz_translated = rewrite_to_genz_style(translated_text, slang_intensity)
            
            # Display results
            st.subheader("기본 번역 (DeepL):")
            st.write(translated_text)
            
            st.subheader("20대 스타일 번역:")
            st.write(genz_translated)
            
            # Suggest additional slang
            st.subheader("추천 슬랭 표현:")
            for suggestion in suggest_slang(translated_text):
                st.write(suggestion)
                
        except deepl.DeepLException as e:
            st.error(f"DeepL 에러: {str(e)}. API 키를 확인하거나 잠시 후 다시 시도해주세요!")
        except Exception as e:
            st.error(f"에러 발생: {str(e)}. 다시 시도해주세요!")
    else:
        st.warning("번역할 한국어 문장을 입력해주세요!")

# Add a fun footer
st.markdown("---")
st.markdown("Made with 💖 for K-pop and Gen Z vibes! ✨")