import streamlit as st
from openai import OpenAI

import streamlit as st
from openai import OpenAI
import anthropic
from anthropic import Anthropic

# Show title and description.
st.title("📄 Document question answering")
st.write(
    "Upload a document below and ask a question about it – GPT will answer! "
    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
)

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:

    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Let the user upload a file via `st.file_uploader`.
    uploaded_file = st.file_uploader(
        "Upload a document (.txt or .md)", type=("txt", "md")
    )

    # Ask the user for a question via `st.text_area`.
    question = st.text_area(
        "Now ask a question about the document!",
        placeholder="Can you give me a short summary?",
        disabled=not uploaded_file,
    )

    if uploaded_file and question:

        # Process the uploaded file and question.
        document = uploaded_file.read().decode()
        messages = [
            {
                "role": "user",
                "content": f"Here's a document: {document} \n\n---\n\n {question}",
            }
        ]

        # Generate an answer using the OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            stream=True,
        )

        # 클로드 API를 사용하여 사업계획서 생성
        with st.spinner('사업계획서를 생성하고 있습니다...'):
            # 회사 정보 입력 받기
            st.subheader("회사 정보 입력")
            company_name = st.text_input("회사명")
            company_address = st.text_input("회사 주소") 
            company_type = st.selectbox("회사 형태", ["주식회사", "유한회사", "개인사업자", "기타"])
            employee_count = st.number_input("직원 수", min_value=1)
            annual_revenue = st.number_input("연매출액(백만원)", min_value=0)
            
            # 사업계획서 생성 시작
            if st.button("사업계획서 생성"):
                messages = [
                    {"role": "system", "content": "정부지원사업 사업계획서 작성 전문가입니다."},
                    {"role": "user", "content": f"""
                    공고 내용: {document}
                    
                    회사 정보:
                    - 회사명: {company_name}
                    - 주소: {company_address}
                    - 회사형태: {company_type} 
                    - 직원수: {employee_count}명
                    - 연매출: {annual_revenue}백만원
                    
                    위 정보를 바탕으로 30페이지 분량의 상세한 사업계획서를 작성해주세요.
                    """}
                ]
                
                response_text = ""
                for chunk in stream:
                    if chunk.choices[0].delta.content is not None:
                        response_text += chunk.choices[0].delta.content
                        st.markdown(response_text)
                
                # 사업계획서 다운로드 버튼 추가
                st.download_button(
                    label="사업계획서 다운로드",
                    data=response_text,
                    file_name="사업계획서.md",
                    mime="text/markdown"
                )
