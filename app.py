import streamlit as st
import PyPDF2
import pandas as pd
import json
from openai import OpenAI

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="AI Resume Screener", layout="wide")

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=50)
    st.title("Settings")
    api_key = st.text_input("Enter OpenAI API Key:", type="password")
    st.info("Get your API key from [OpenAI](https://platform.openai.com/account/api-keys)")
    st.markdown("---")
    st.write("### How it works")
    st.write("1. Enter the Job Description.")
    st.write("2. Upload PDF Resumes.")
    st.write("3. Click 'Analyze'.")
    st.write("4. See ranked candidates with AI feedback.")

# --- MAIN UI ---
st.title("📄 AI Resume Screening Agent")
st.markdown("### Rank and Analyze Candidates Instantly")

# 1. Job Description Input
st.subheader("1. Job Description")
jd_text = st.text_area(
    "Paste the Job Description (JD) here:",
    height=150,
    placeholder="e.g., Senior Python Developer with 5 years experience in Django..."
)

# 2. Resume Upload
st.subheader("2. Upload Resumes")
uploaded_files = st.file_uploader(
    "Upload PDF Resumes", type=["pdf"], accept_multiple_files=True
)

# --- CORE FUNCTIONS ---

def extract_text_from_pdf(uploaded_file):
    """Extract text from PDF"""
    try:
        reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        return None

def analyze_resume_with_openai(api_key, resume_text, jd_text, file_name):
    """Send prompt to OpenAI GPT and parse JSON response"""
    client = OpenAI(api_key=api_key)
    prompt = f"""
Act as an expert HR Recruiter.

Job Description: "{jd_text}"

Resume Text: "{resume_text}"

Evaluate this candidate and return JSON with keys:
{{
    "Name": "Candidate Name",
    "Match_Score": "0-100",
    "Key_Strengths": ["strength1", "strength2"],
    "Missing_Skills": ["skill1", "skill2"],
    "Summary": "Brief 2-line summary of fit"
}}
Return only JSON.
"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        text_response = response.choices[0].message.content
        # clean JSON
        clean_json = text_response.replace("```json", "").replace("```", "").strip()
        data = json.loads(clean_json)
        data['Filename'] = file_name
        return data
    except Exception as e:
        st.error(f"Error analyzing {file_name}: {str(e)}")
        return None

def analyze_resumes(files, jd):
    if not api_key:
        st.error("Please enter your OpenAI API Key in the sidebar.")
        return None

    results = []
    progress_bar = st.progress(0)
    status_text = st.empty()

    for index, file in enumerate(files):
        status_text.text(f"Analyzing {file.name}...")
        resume_text = extract_text_from_pdf(file)
        if resume_text:
            data = analyze_resume_with_openai(api_key, resume_text, jd, file.name)
            if data:
                results.append(data)
        progress_bar.progress((index + 1) / len(files))

    status_text.text("Analysis Complete!")
    return pd.DataFrame(results)

# --- EXECUTION ---
if st.button("Analyze Candidates"):
    if not jd_text:
        st.warning("Please paste a Job Description.")
    elif not uploaded_files:
        st.warning("Please upload at least one resume.")
    else:
        with st.spinner("Analyzing resumes with OpenAI GPT..."):
            df = analyze_resumes(uploaded_files, jd_text)
            if df is not None and not df.empty:
                # reorder columns
                cols = ['Name', 'Match_Score', 'Summary', 'Key_Strengths', 'Missing_Skills', 'Filename']
                df = df[cols]
                df['Match_Score'] = pd.to_numeric(df['Match_Score'])
                df = df.sort_values(by='Match_Score', ascending=False)

                st.success("Analysis Successful!")
                st.markdown("### 🏆 Candidate Leaderboard")
                st.dataframe(df)

                # download CSV
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "📥 Download Report as CSV",
                    data=csv,
                    file_name="recruitment_report.csv",
                    mime="text/csv"
                )
            else:
                st.error("Could not analyze resumes. Check API key or PDF format.")
