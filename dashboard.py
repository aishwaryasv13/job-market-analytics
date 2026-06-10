import pandas as pd
import plotly.express as px
import streamlit as st

# ── Page config ──────────────────────────────────────────────
st.set_page_config(
    page_title="Job Market Analytics",
    page_icon="📊",
    layout="wide"
)

# ── Load Data ─────────────────────────────────────────────────
DATA_DIR = "C:/Users/Aishwarya/Desktop/job-market-project/output/"

@st.cache_data
def load_data():
    postings      = pd.read_csv(DATA_DIR + "postings_clean.csv",        low_memory=False)
    skills        = pd.read_csv(DATA_DIR + "analytics_top_skills.csv")
    salary_city   = pd.read_csv(DATA_DIR + "analytics_salary_by_city.csv")
    salary_title  = pd.read_csv(DATA_DIR + "analytics_salary_by_title.csv")
    remote        = pd.read_csv(DATA_DIR + "analytics_remote_vs_onsite.csv")
    jobs_city     = pd.read_csv(DATA_DIR + "analytics_jobs_by_city.csv")
    experience    = pd.read_csv(DATA_DIR + "analytics_jobs_by_experience.csv")
    industries    = pd.read_csv(DATA_DIR + "analytics_top_industries.csv")
    benefits      = pd.read_csv(DATA_DIR + "analytics_top_benefits.csv")
    return postings, skills, salary_city, salary_title, remote, jobs_city, experience, industries, benefits

postings, skills, salary_city, salary_title, remote, jobs_city, experience, industries, benefits = load_data()

# ── Header ────────────────────────────────────────────────────
st.title("📊 Job Market Analytics Dashboard")
st.markdown("Based on **3.38 million LinkedIn job postings** (April 2024)")
st.divider()

# ── KPI Cards ─────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Job Postings",   f"{len(postings):,}")
k2.metric("Avg Annual Salary",    f"${postings['clean_salary'].mean():,.0f}")
k3.metric("Remote Jobs",          f"{remote[remote['is_remote']==1]['percentage'].values[0]}%")
k4.metric("Cities Covered",       f"{postings['city'].nunique():,}")

st.divider()

# ── Row 1: Skills & Industries ────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("Most Demanded Skills")
    fig = px.bar(
        skills.sort_values('job_count'),
        x='job_count', y='skill_abr',
        orientation='h',
        color='job_count',
        color_continuous_scale='Blues',
        labels={'job_count': 'Job Count', 'skill_abr': 'Skill'}
    )
    fig.update_layout(showlegend=False, coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader(" Top Hiring Industries")
    fig = px.bar(
        industries.sort_values('job_count'),
        x='job_count', y='industry_name',
        orientation='h',
        color='job_count',
        color_continuous_scale='Greens',
        labels={'job_count': 'Job Count', 'industry_name': 'Industry'}
    )
    fig.update_layout(showlegend=False, coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

# ── Row 2: Salary by City & Remote vs Onsite ─────────────────
col3, col4 = st.columns(2)

with col3:
    st.subheader("Average Salary by City")
    fig = px.bar(
        salary_city.sort_values('avg_salary'),
        x='avg_salary', y='city',
        orientation='h',
        color='avg_salary',
        color_continuous_scale='Oranges',
        labels={'avg_salary': 'Avg Annual Salary', 'city': 'City'}
    )
    fig.update_layout(showlegend=False, coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

with col4:
    st.subheader("Remote vs Onsite")
    fig = px.pie(
        remote,
        values='job_count',
        names='label',
        color_discrete_sequence=['#636EFA', '#EF553B'],
        hole=0.4
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig, use_container_width=True)

# ── Row 3: Jobs by City & Experience ─────────────────────────
col5, col6 = st.columns(2)

with col5:
    st.subheader("Top Hiring Cities")
    fig = px.bar(
        jobs_city.sort_values('job_count'),
        x='job_count', y='city',
        orientation='h',
        color='job_count',
        color_continuous_scale='Purples',
        labels={'job_count': 'Job Count', 'city': 'City'}
    )
    fig.update_layout(showlegend=False, coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

with col6:
    st.subheader("Jobs by Experience Level")
    fig = px.bar(
        experience.sort_values('job_count'),
        x='job_count', y='formatted_experience_level',
        orientation='h',
        color='job_count',
        color_continuous_scale='Reds',
        labels={'job_count': 'Job Count', 'formatted_experience_level': 'Experience Level'}
    )
    fig.update_layout(showlegend=False, coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

# ── Row 4: Benefits & Salary by Title ────────────────────────
col7, col8 = st.columns(2)

with col7:
    st.subheader("Most Common Benefits")
    fig = px.bar(
        benefits.sort_values('job_count'),
        x='job_count', y='type',
        orientation='h',
        color='job_count',
        color_continuous_scale='Teal',
        labels={'job_count': 'Job Count', 'type': 'Benefit'}
    )
    fig.update_layout(showlegend=False, coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

with col8:
    st.subheader("Top Paying Job Titles")
    fig = px.bar(
        salary_title.head(15).sort_values('avg_salary'),
        x='avg_salary', y='title',
        orientation='h',
        color='avg_salary',
        color_continuous_scale='Mint',
        labels={'avg_salary': 'Avg Annual Salary', 'title': 'Job Title'}
    )
    fig.update_layout(showlegend=False, coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

st.divider()
st.caption("Data source: LinkedIn Job Postings 2023–2024 | Kaggle")