import streamlit as st
from ai_helper import ask_ai

# 페이지 설정
st.set_page_config(page_title="글쓰기 코칭 앱", layout="wide")

st.title("✍️ AI 글쓰기 코칭 앱")

# 글의 종류 정의
WRITING_TYPES = [
    "일반 글",
    "이메일",
    "보고서",
    "블로그 포스트",
    "창작물",
    "자기소개",
    "건의문",
    "기타"
]

# 사이드바에서 글의 종류 선택
with st.sidebar:
    st.subheader("📋 설정")
    writing_type = st.selectbox(
        "글의 종류를 선택하세요",
        WRITING_TYPES,
        index=0
    )

# 메인 영역
st.write("---")

# 글 입력
st.subheader("📝 당신의 글을 입력하세요")
user_text = st.text_area(
    "글을 입력해주세요 (여러 줄 가능)",
    height=200,
    placeholder="여기에 당신의 글을 입력하세요..."
)

st.write("---")

# 분석 버튼
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    analyze_button = st.button("🚀 코칭 받기", use_container_width=True)

# 분석 처리
if analyze_button:
    if not user_text.strip():
        st.error("글을 입력해주세요!")
    else:
        # 1차: 피드백 생성
        with st.spinner("1/2 AI가 피드백을 작성 중입니다..."):
            feedback_prompt = f"""다음 '{writing_type}' 글을 읽고 피드백을 주세요.

글:
{user_text}

다음 형식으로 피드백을 작성해주세요:
1. **좋은 점** (3-4개 항목)
2. **고칠 점** (3-4개 항목)
3. **개선 팁** (구체적인 조언)"""

            feedback = ask_ai(feedback_prompt)

        # 2차: 글 다듬기
        with st.spinner("2/2 글을 다듬는 중입니다..."):
            refinement_prompt = f"""다음은 원본 글과 피드백입니다.

원본 글:
{user_text}

피드백:
{feedback}

피드백의 내용을 반영하여 글을 더 나아지도록 다시 작성해주세요. 글의 본질과 의도는 유지하되, 더 명확하고 설득력 있게 개선해주세요."""

            refined_text = ask_ai(refinement_prompt)

        # 결과 표시
        st.success("✨ 코칭 완료!")
        st.write("---")

        # 피드백과 다듬어진 글을 나란히 표시
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📌 피드백")
            st.info(feedback)

        with col2:
            st.subheader("✨ 다듬어진 글")
            st.success(refined_text)

        # 원본 글 비교
        with st.expander("📄 원본 글 보기"):
            st.text(user_text)
