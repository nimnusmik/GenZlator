import streamlit as st
import requests

SOLAR_API_URL = "https://api.upstage.ai/v1/chat/completions"
SOLAR_MODEL = "solar-1-mini-chat"

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
body {
    font-family: 'Poppins', sans-serif;
    background: linear-gradient(135deg, #f5f7fa, #c3cfe2);
}
h1 {
    color: #6B48FF;
    text-align: center;
    font-weight: 600;
    font-size: 2.5em;
    margin-bottom: 0.5em;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
}
.stTextArea, .stButton, .stSlider, .stMarkdown {
    background: #ffffff;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    margin-bottom: 20px;
}
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
h2 {
    color: #FF6F91;
    font-size: 1.5em;
    margin-top: 20px;
}
.stSidebar {
    background: #2E2E2E;
    color: white;
}
.stSidebar h3 {
    color: #FF9671;
}
p, .stMarkdown {
    color: #333;
    font-size: 1.1em;
}
footer {
    text-align: center;
    color: #6B48FF;
    font-size: 1em;
    margin-top: 30px;
}
</style>
""", unsafe_allow_html=True)

try:
    solar_api_key = st.secrets["SOLAR_API_KEY"]
except KeyError as e:
    st.error("Solar API 키가 설정되지 않았습니다. .streamlit/secrets.toml 파일에서 SOLAR_API_KEY를 확인하세요.")
    st.stop()

st.sidebar.write("### Debug: API Keys")
st.sidebar.write(f"Solar Key: {'Set' if solar_api_key else 'Not set'}")

slang_dict = {
    "cool": ["lit", "dope", "fire", "chill", "valid"],
    "good": ["awesome", "sick", "bomb", "tight", "clean"],
    "great": ["bussin'", "elite", "on point", "goated"],
    "amazing": ["slaps", "next-level", "cracked", "top-tier"],
    "friend": ["homie", "bro", "dude", "fam", "bestie"],
    "happy": ["stoked", "pumped", "vibin'", "feelin' it"],
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
    "nervous": ["shakin'", "tweakin'", "buggin'"],
    "confident": ["slayin'", "poppin' off", "unbothered"],
    "sleep": ["catch some Z's", "crash", "knock out"],
    "say": ["drop", "spit", "hit me with it"],
    "go": ["dip", "bounce", "slide", "head out"],
    "talk": ["spill", "chat", "holla", "link up"],
    "leave me alone": ["chill", "back off", "get off my case"],
    "like": ["vibe with", "rock with", "mess with"],
    "love": ["obsessed", "can't", "stan", "heart eyes"],
    "hate": ["over it", "can't deal", "ick"],
    "post": ["drop", "flex", "throw up"],
    "support": ["hype up", "gas up", "show love"]
}

headers = {
    "Authorization": f"Bearer {solar_api_key}",
    "Content-Type": "application/json"
}


def call_solar(messages, temperature=0.6, max_tokens=256):
    payload = {
        "model": SOLAR_MODEL,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    response = requests.post(SOLAR_API_URL, headers=headers, json=payload, timeout=30)
    if response.status_code != 200:
        raise RuntimeError(f"Solar API 오류: {response.status_code} / {response.text}")
    data = response.json()
    try:
        return data["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError) as exc:
        raise RuntimeError(f"Solar API 응답 파싱 실패: {data}") from exc


def translate_to_english(text):
    messages = [
        {
            "role": "system",
            "content": "You are a professional translator who produces fluent US English without slang or explanations."
        },
        {
            "role": "user",
            "content": f"Translate the following Korean sentence into natural US English. Return only the translation.\n\n{text}"
        }
    ]
    return call_solar(messages, temperature=0.2, max_tokens=180)


def rewrite_to_genz_style(text, slang_intensity):
    intensity_description = "minimal" if slang_intensity <= 3 else "moderate" if slang_intensity <= 7 else "heavy"
    prompt = (
        "Rewrite the sentence below in a casual Gen Z tone using slang popular among 20-somethings in 2025. "
        f"Use {intensity_description} slang based on this intensity level ({slang_intensity}/10). "
        "Keep it short, fun, and natural. Return only the rewritten sentence.\n\n"
        f"{text}"
    )
    messages = [
        {
            "role": "system",
            "content": "You are a Gen Z slang expert who rewrites sentences to sound trendy and casual."
        },
        {"role": "user", "content": prompt}
    ]
    return call_solar(messages, temperature=0.7, max_tokens=120)


def suggest_slang(text):
    used_words = [key for key in slang_dict if key in text.lower()]
    suggestions = []
    if used_words:
        for word in used_words:
            suggestions.append(f"**'{word}'** 대신 사용할 수 있는 슬랭: {', '.join(slang_dict[word])}")
    else:
        suggestions.append("이 문장에 딱 맞는 슬랭을 찾지 못했어요. 😅")
    return suggestions


st.title("🌟 Turn your Korean into natural, native English 📣")
st.write("Tired of awkward translations? We turn your Korean into real-life English people actually use.")
st.sidebar.write("Made with ❤️ by Sunmin Kim")

korean_input = st.text_area("한국어 문장을 입력하세요:", height=100, value=" 안녕하세요! 이 앱은 한국어를 자연스러운 영어로 번역해 줘요.")
slang_intensity = st.slider("Gen Z 슬랭 강도 조절", min_value=0, max_value=10, value=5, step=1)
st.write(f"슬랭 강도: {slang_intensity}/10")

if st.button("번역하기"):
    if korean_input:
        try:
            translated_text = translate_to_english(korean_input)
            genz_translated = rewrite_to_genz_style(translated_text, slang_intensity)

            st.subheader("기본 번역:")
            st.write(translated_text)

            st.subheader("슬랭어 번역:")
            st.write(genz_translated)

            st.subheader("추천 슬랭 표현:")
            for suggestion in suggest_slang(translated_text):
                st.write(suggestion)
        except RuntimeError as err:
            st.error(str(err))
        except requests.RequestException as err:
            st.error(f"네트워크 오류: {err}")
    else:
        st.warning("번역할 한국어 문장을 입력해주세요!")

st.markdown("---")
