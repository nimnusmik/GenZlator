# GenZlator
GenZlator는 한국어 문장을 Z세대가 실제로 쓰는 자연스러운 영어 표현으로 바꿔주는 Streamlit 기반 번역/스타일링 도구입니다. 기본 번역은 기계 번역 엔진으로 처리하고, 이후 생성형 AI가 슬랭과 톤을 입혀 줍니다.

## 주요 특징
- DeepL 번역 API로 고품질 한국어→영어 기본 번역 수행
- OpenAI Chat Completions 또는 Hugging Face Inference API로 Gen Z 슬랭 스타일 재작성
- 슬랭 강도(0~10) 조절, 다양한 톤(Gen Z/Formal/Sarcastic/Flirty) 선택 지원
- 번역 히스토리, 복사 버튼 등 실용적인 UI 제공
- 커스텀 슬랭 사전을 이용한 추가 표현 추천

## 파이프라인 개요
1. **입력 수집**: Streamlit 텍스트 입력 위젯에서 한국어 문장을 받습니다.
2. **API 키 검증**: `.streamlit/secrets.toml`을 통해 DeepL/OpenAI 키가 존재하는지 확인하고, 없는 경우 앱 실행을 중단합니다 (`slang_translator.py`).
3. **1차 번역 (기본 영어)**: DeepL SDK를 사용해 한국어 문장을 미국식 영어(`EN-US`)로 번역합니다.
4. **2차 스타일링 (Gen Z 슬랭)**:
   - `slang_translator.py`: OpenAI `gpt-3.5-turbo` 모델이 슬랭 강도에 맞춰 문장을 재작성합니다.
   - `app.py`: Hugging Face `HuggingFaceH4/zephyr-7b-beta` 모델이 선택한 톤에 맞춰 한 문장만 반환하도록 지시합니다.
5. **후처리 및 표시**: 불필요한 토큰 제거, 추천 슬랭 제안, 변환 내역(최근 5개) 출력, 복사 버튼 제공 등 UI 요소를 구성합니다.

## 구성 요소
- `slang_translator.py`: DeepL + OpenAI 조합의 메인 Streamlit 앱. 슬랭 강도 조절과 슬랭 추천 기능을 제공합니다.
- `app.py`: Hugging Face Inference API 기반의 경량 앱. 다양한 톤 옵션과 히스토리 관리에 초점을 둡니다.
- `data/`: 슬랭 학습 데이터(JSONL, CSV)와 검증/정제 스크립트가 위치합니다.
- `scripts/`: 데이터 변환 및 파인튜닝을 위한 보조 스크립트(템플릿).
- `static/`, `templates/`: 추후 웹 배포 시 활용 가능한 정적 자원/템플릿.

## 요구 사항
- Python 3.10 이상 권장
- 필수 패키지: `streamlit==1.36.0`, `deepl==1.18.0`, `openai==1.35.7` (루트 `requirements.txt` 참고)

## 설치 & 실행
```bash
# (선택) 가상환경 생성
python3 -m venv venv
source venv/bin/activate  # Windows는 venv\Scripts\activate

pip install -r requirements.txt

# Streamlit 앱 실행
streamlit run slang_translator.py
# 또는
streamlit run app.py
```

## 환경 변수 설정
`slang_translator.py`는 Streamlit 시크릿을 통해 API 키를 읽습니다. 프로젝트 루트에 `.streamlit/secrets.toml` 파일을 생성하고 아래와 같이 입력하세요.
```toml
DEEPL_AUTH_KEY = "your_deepl_key"
OPENAI_API_KEY = "your_openai_key"
```
`app.py`를 사용하는 경우 Hugging Face 토큰을 코드 상단 `HF_TOKEN` 상수에 직접 입력하거나, 환경 변수로 주입한 뒤 `os.environ`에서 읽도록 수정할 수 있습니다.

## 사용 방법
1. Streamlit 앱에 접속하면 한국어 입력창과 슬랭 강도 슬라이더 또는 톤 선택 박스가 표시됩니다.
2. 번역 버튼을 누르면 DeepL 결과와 Gen Z 스타일 문장을 순서대로 확인할 수 있습니다.
3. 추천 슬랭 섹션에서 대체 표현을 참고하거나 복사 버튼으로 결과를 클립보드에 저장하세요.
4. `다시 생성` 버튼(또는 슬랭 강도 재조정)을 이용해 다른 뉘앙스를 빠르게 시도할 수 있습니다.

## 데이터 준비 & 파인튜닝
- `data/slang_dataset.jsonl`: `{"input": "…", "output": "…"}` 형식의 원본 학습 데이터.
- `data/cvs2json.py`: JSONL 내 잘못된 키(예: `' output'`)를 `output`으로 수정해 `slang_dataset_fixed.jsonl`을 생성합니다.
- `data/test.py`: JSONL 레코드가 올바른지(키 존재 여부 등) 검증합니다.
- `GENZSLANGS.xlsx`: 슬랭 표현 정리용 참고 자료.
- `scripts/convert_csv_to_jsonl.py`, `scripts/finetune_model.py`: CSV→JSONL 변환, 모델 파인튜닝 워크플로를 구현할 때 사용할 수 있는 템플릿 파일입니다(직접 로직을 작성해야 합니다).

## 프로젝트 구조
```text
GenZlator/
├─ app.py                # Hugging Face 기반 Streamlit 앱
├─ slang_translator.py   # DeepL + OpenAI 기반 메인 앱
├─ data/                 # 데이터셋 및 정제 스크립트
├─ scripts/              # 데이터 변환/파인튜닝용 스크립트 템플릿
├─ static/               # 스타일시트 등 정적 자원
├─ templates/            # HTML 템플릿(향후 확장용)
└─ utils.py              # 공용 유틸(현재 placeholder)
```

## 주의 사항 & 향후 과제
- OpenAI 및 Hugging Face API 호출에는 요금이 발생할 수 있으니 크레딧을 확인하세요.
- Hugging Face API는 응답 속도 및 토큰 제한에 따라 오류가 발생할 수 있으며, 상태 코드/응답 로그를 통해 디버깅할 수 있습니다 (`app.py`).
- 학습 데이터에 선행/후행 공백 등 노이즈가 있을 수 있으니 모델 파인튜닝 전 정제 과정을 강화하는 것이 좋습니다.
- `scripts/` 디렉터리의 템플릿을 활용해 사용자 정의 학습 파이프라인을 구축하거나, OpenAI/DeepL 대체 모델을 연결할 수 있습니다.

이 프로젝트가 한국어 사용자에게 더 자연스럽고 트렌디한 영어 커뮤니케이션 경험을 제공하는 데 도움이 되길 바랍니다. 즐거운 슬랭 번역을 시작해 보세요! 🧃
