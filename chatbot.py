import anthropic
import streamlit as st
import pandas as pd
import os

# ── Configure Claude API ──────────────────────────────────────
import os
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# ── Load Analytics Data ───────────────────────────────────────
DATA_DIR = "C:/Users/Aishwarya/Desktop/job-market-project/output/"

@st.cache_data
def load_context():
    top_skills      = pd.read_csv(DATA_DIR + "analytics_top_skills.csv")
    salary_city     = pd.read_csv(DATA_DIR + "analytics_salary_by_city.csv")
    salary_title    = pd.read_csv(DATA_DIR + "analytics_salary_by_title.csv")
    remote          = pd.read_csv(DATA_DIR + "analytics_remote_vs_onsite.csv")
    jobs_city       = pd.read_csv(DATA_DIR + "analytics_jobs_by_city.csv")
    experience      = pd.read_csv(DATA_DIR + "analytics_jobs_by_experience.csv")
    industries      = pd.read_csv(DATA_DIR + "analytics_top_industries.csv")
    benefits        = pd.read_csv(DATA_DIR + "analytics_top_benefits.csv")

    context = f"""
You are a job market analyst. Answer based ONLY on this LinkedIn jobs data (April 2024, 3.38M postings).

TOP 5 SKILLS: {', '.join(top_skills.head(5)['skill_abr'].tolist())}

TOP 5 CITIES BY SALARY: {', '.join([f"{r['city']}(${r['avg_salary']:,.0f})" for _, r in salary_city.head(5).iterrows()])}

TOP 5 PAYING TITLES: {', '.join([f"{r['title']}(${r['avg_salary']:,.0f})" for _, r in salary_title.head(5).iterrows()])}

REMOTE VS ONSITE: {remote[remote['is_remote']==1]['percentage'].values[0]}% remote, {remote[remote['is_remote']==0]['percentage'].values[0]}% onsite

TOP 5 HIRING CITIES: {', '.join([f"{r['city']}({r['job_count']:,})" for _, r in jobs_city.head(5).iterrows()])}

EXPERIENCE LEVELS: {', '.join([f"{r['formatted_experience_level']}({r['job_count']:,})" for _, r in experience.iterrows()])}

TOP 5 INDUSTRIES: {', '.join([f"{r['industry_name']}({r['job_count']:,})" for _, r in industries.head(5).iterrows()])}

TOP 5 BENEFITS: {', '.join(benefits.head(5)['type'].tolist())}

Be concise and always reference specific numbers from the data.
    """
    return context

context = load_context()

# ── Page Setup ────────────────────────────────────────────────
st.set_page_config(
    page_title="Job Market Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.title("Job Market AI Chatbot")
st.markdown("Ask me anything about the **LinkedIn Job Market (April 2024)** dataset!")
st.divider()

# ── Chat History ──────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display existing chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ── Chat Input ────────────────────────────────────────────────
if prompt := st.chat_input("Ask a question about the job market..."):

    # Show user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate Claude response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            full_prompt = f"{context}\n\nUser question: {prompt}"
            response = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=500,
                messages=[{"role": "user", "content": full_prompt}]
            )
            answer = response.content[0].text
            st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})