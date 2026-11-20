import os
import json
import streamlit as st
import pandas as pd
from dotenv import load_dotenv

# Load local environment variables from .env file (if present)
load_dotenv()

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="AI Career Roadmap & Skill Gap Finder",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Custom Styling for Modern, Clean Interface
# ---------------------------------------------------------
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    .metric-badge {
        padding: 12px 18px;
        border-radius: 10px;
        background: #F1F5F9;
        border: 1px solid #CBD5E1;
        text-align: center;
    }
    .week-card {
        background-color: #F8FAFC;
        border-left: 5px solid #2563EB;
        padding: 16px 20px;
        border-radius: 0 10px 10px 0;
        margin-bottom: 14px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .project-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 20px;
        height: 100%;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    .project-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #1E40AF;
        margin-bottom: 8px;
    }
    .tech-pill {
        display: inline-block;
        background-color: #EEF2FF;
        color: #4338CA;
        padding: 3px 9px;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-right: 4px;
        margin-top: 4px;
        border: 1px solid #C7D2FE;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Helper Functions: Gemini API Call & JSON Parser
# ---------------------------------------------------------
def call_gemini_api(api_key: str, current_skills: str, target_role: str, hours_per_week: int) -> dict:
    """
    Calls Google Gemini API to analyze skill gaps and produce an 8-week structured roadmap.
    Supports both `google-genai` and legacy `google.generativeai`.
    """
    prompt = f"""
You are a senior tech career mentor and engineering hiring manager.
Compare the student's current skills against the target job role, identify the skill gap, and build a tailored 8-week learning plan based on their available study time.

Student Profile:
- Current Skills: {current_skills}
- Target Job Role: {target_role}
- Available Study Time: {hours_per_week} hours per week (Total over 8 weeks: {hours_per_week * 8} hours)

Respond strictly with a valid JSON object matching this exact schema:
{{
  "readiness_score": <integer from 0 to 100 representing estimated current readiness>,
  "executive_summary": "<2-3 sentence strategic advice on the transition>",
  "skill_gap_analysis": [
    {{
      "domain_category": "<e.g. Core Languages, Frameworks, Databases, Tools>",
      "skills_you_have": "<Skills the student already knows in this category, or 'None'>",
      "skills_to_learn": "<Required skills to learn for target role>",
      "priority": "High" | "Medium" | "Low"
    }}
  ],
  "eight_week_roadmap": [
    {{
      "week_number": 1,
      "theme": "<Theme / Focus for Week 1>",
      "key_topics": ["<Topic 1>", "<Topic 2>", "<Topic 3>"],
      "weekly_milestone": "<Concrete mini hands-on task or deliverable for this week>"
    }},
    {{
      "week_number": 2,
      "theme": "<Theme / Focus for Week 2>",
      "key_topics": ["<Topic 1>", "<Topic 2>", "<Topic 3>"],
      "weekly_milestone": "<Concrete mini hands-on task or deliverable for this week>"
    }},
    {{
      "week_number": 3,
      "theme": "<Theme / Focus for Week 3>",
      "key_topics": ["<Topic 1>", "<Topic 2>", "<Topic 3>"],
      "weekly_milestone": "<Concrete mini hands-on task or deliverable for this week>"
    }},
    {{
      "week_number": 4,
      "theme": "<Theme / Focus for Week 4>",
      "key_topics": ["<Topic 1>", "<Topic 2>", "<Topic 3>"],
      "weekly_milestone": "<Concrete mini hands-on task or deliverable for this week>"
    }},
    {{
      "week_number": 5,
      "theme": "<Theme / Focus for Week 5>",
      "key_topics": ["<Topic 1>", "<Topic 2>", "<Topic 3>"],
      "weekly_milestone": "<Concrete mini hands-on task or deliverable for this week>"
    }},
    {{
      "week_number": 6,
      "theme": "<Theme / Focus for Week 6>",
      "key_topics": ["<Topic 1>", "<Topic 2>", "<Topic 3>"],
      "weekly_milestone": "<Concrete mini hands-on task or deliverable for this week>"
    }},
    {{
      "week_number": 7,
      "theme": "<Theme / Focus for Week 7>",
      "key_topics": ["<Topic 1>", "<Topic 2>", "<Topic 3>"],
      "weekly_milestone": "<Concrete mini hands-on task or deliverable for this week>"
    }},
    {{
      "week_number": 8,
      "theme": "<Theme / Focus for Week 8: Capstone & Portfolio Polish>",
      "key_topics": ["<Topic 1>", "<Topic 2>", "<Topic 3>"],
      "weekly_milestone": "<Concrete mini hands-on task or deliverable for this week>"
    }}
  ],
  "portfolio_projects": [
    {{
      "title": "<Project 1 Title>",
      "description": "<2 sentences explaining what the project does and the problem solved>",
      "tech_stack": ["<Tech 1>", "<Tech 2>", "<Tech 3>"],
      "resume_impact": "<What skill this project demonstrates to recruiters>"
    }},
    {{
      "title": "<Project 2 Title>",
      "description": "<2 sentences explaining what the project does and the problem solved>",
      "tech_stack": ["<Tech 1>", "<Tech 2>", "<Tech 3>"],
      "resume_impact": "<What skill this project demonstrates to recruiters>"
    }},
    {{
      "title": "<Project 3 Title>",
      "description": "<2 sentences explaining what the project does and the problem solved>",
      "tech_stack": ["<Tech 1>", "<Tech 2>", "<Tech 3>"],
      "resume_impact": "<What skill this project demonstrates to recruiters>"
    }}
  ]
}}

Requirements:
- Ensure the roadmap contains exactly 8 weeks (weeks 1 to 8).
- Ensure portfolio_projects contains exactly 3 projects tailored to {target_role}.
- Output ONLY the raw JSON object, without markdown code fences or conversational text.
"""

    # Method 1: Try new `google-genai` SDK
    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        for model_name in ["gemini-2.5-flash", "gemini-1.5-flash"]:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )
                if response.text:
                    return parse_json_response(response.text)
            except Exception:
                continue
    except ImportError:
        pass
    except Exception:
        pass

    # Method 2: Try legacy `google.generativeai` SDK
    try:
        import google.generativeai as legacy_genai
        legacy_genai.configure(api_key=api_key)
        model = legacy_genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return parse_json_response(response.text)
    except Exception as e:
        raise RuntimeError(f"Gemini API Error: {e}")

def parse_json_response(text: str) -> dict:
    """Parses JSON text robustly, stripping markdown markers if present."""
    cleaned = text.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]
    elif cleaned.startswith("```"):
        cleaned = cleaned[3:]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
    cleaned = cleaned.strip()
    return json.loads(cleaned)

def generate_markdown_download(data: dict, current_skills: str, target_role: str, hours: int) -> str:
    """Creates a clean downloadable Markdown document of the generated roadmap."""
    md = f"# 🗺️ 8-Week Career Roadmap: {target_role}\n\n"
    md += f"- **Current Skills:** {current_skills}\n"
    md += f"- **Target Role:** {target_role}\n"
    md += f"- **Time Commitment:** {hours} hours/week (Total: {hours * 8} hours)\n"
    md += f"- **Estimated Starting Readiness:** {data.get('readiness_score', 0)}%\n\n"
    md += f"## 📌 Executive Summary\n{data.get('executive_summary', '')}\n\n"
    
    md += "## 📊 Skill Gap Analysis\n"
    md += "| Category | Skills You Have | Skills to Learn | Priority |\n"
    md += "| :--- | :--- | :--- | :---: |\n"
    for item in data.get("skill_gap_analysis", []):
        md += f"| {item.get('domain_category')} | {item.get('skills_you_have')} | {item.get('skills_to_learn')} | {item.get('priority')} |\n"
    md += "\n"

    md += "## 📅 8-Week Week-by-Week Learning Plan\n"
    for w in data.get("eight_week_roadmap", []):
        md += f"### Week {w.get('week_number')}: {w.get('theme')}\n"
        md += f"- **Key Topics:** {', '.join(w.get('key_topics', []))}\n"
        md += f"- **Milestone Project:** {w.get('weekly_milestone')}\n\n"

    md += "## 💼 3 Mini Portfolio Projects\n"
    for i, p in enumerate(data.get("portfolio_projects", []), 1):
        md += f"### {i}. {p.get('title')}\n"
        md += f"- **Description:** {p.get('description')}\n"
        md += f"- **Tech Stack:** {', '.join(p.get('tech_stack', []))}\n"
        md += f"- **Resume Impact:** {p.get('resume_impact')}\n\n"

    return md

# ---------------------------------------------------------
# Sidebar Configuration
# ---------------------------------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/color/96/compass.png", width=64)
    st.title("Configuration")

    env_key = os.getenv("GEMINI_API_KEY", "")
    api_key_input = st.text_input(
        "Google Gemini API Key",
        value=env_key,
        type="password",
        help="Free key from https://aistudio.google.com/"
    )

    if not api_key_input:
        st.warning("⚠️ Enter your Gemini API key to run.")
        st.markdown("[Get Free Gemini API Key](https://aistudio.google.com/)")
    else:
        st.success("✅ API Key configured!")

    st.markdown("---")
    st.markdown("### 📌 About Problem #4")
    st.markdown(
        "**AI Career Roadmap & Skill Gap Finder** compares a student's existing skillset "
        "against an industry role, producing an actionable 8-week week-by-week study roadmap and 3 portfolio projects."
    )
    st.markdown("**Tools:** Streamlit + Gemini API + Pandas")

# ---------------------------------------------------------
# Main Application UI
# ---------------------------------------------------------
st.markdown('<div class="main-header">🗺️ AI Career Roadmap & Skill Gap Finder</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Bridge the gap between what you know today and what top tech companies hire for tomorrow.</div>', unsafe_allow_html=True)

# Sample Presets for Fast 1-Click Testing
PRESETS = {
    "Data Scientist": {
        "skills": "C, basic Python, HTML, basic SQL, Excel",
        "role": "Data Scientist",
        "hours": 12
    },
    "Full-Stack Web Developer": {
        "skills": "Basic JavaScript, HTML, CSS, basic C++",
        "role": "Full-Stack Web Developer (MERN)",
        "hours": 15
    },
    "AI / ML Engineer": {
        "skills": "Python, Linear Algebra, basic Git",
        "role": "Machine Learning Engineer",
        "hours": 14
    }
}

col_preset1, col_preset2 = st.columns([1, 3])
with col_preset1:
    selected_preset = st.selectbox("Quick Sample Presets:", ["Custom", "Data Scientist", "Full-Stack Web Developer", "AI / ML Engineer"])

if selected_preset != "Custom" and st.button("⚡ Load Preset Data"):
    preset = PRESETS[selected_preset]
    st.session_state["current_skills"] = preset["skills"]
    st.session_state["target_role"] = preset["role"]
    st.session_state["hours_per_week"] = preset["hours"]

# Input Form
with st.container():
    col1, col2 = st.columns([1.2, 1], gap="medium")

    with col1:
        st.markdown("### 1. Your Background & Goal")
        current_skills = st.text_area(
            "What skills do you currently have?",
            value=st.session_state.get("current_skills", "C, basic Python, HTML"),
            placeholder="e.g. C, basic Python, HTML, Git, basic SQL",
            height=110,
            help="List programming languages, tools, frameworks, or concepts you're familiar with."
        )

        target_role = st.text_input(
            "Target Job Role:",
            value=st.session_state.get("target_role", "Data Scientist"),
            placeholder="e.g. Data Scientist, Cloud DevOps Engineer, Backend Python Developer"
        )

    with col2:
        st.markdown("### 2. Time Commitment")
        hours_per_week = st.slider(
            "Hours per week available to study:",
            min_value=4,
            max_value=35,
            value=st.session_state.get("hours_per_week", 12),
            step=1,
            help="How many hours can you realistically dedicate every week?"
        )
        total_hours = hours_per_week * 8
        st.info(f"⏱️ **Total Commitment:** {hours_per_week} hrs/week × 8 weeks = **{total_hours} total hours**.")

st.markdown("---")
generate_btn = st.button("🚀 Generate My Custom 8-Week Roadmap", type="primary", use_container_width=True)

# ---------------------------------------------------------
# Generation & Results Display
# ---------------------------------------------------------
if generate_btn:
    api_key_to_use = api_key_input.strip() if api_key_input else os.getenv("GEMINI_API_KEY", "").strip()

    if not api_key_to_use:
        st.error("❌ Please provide a Gemini API Key in the left sidebar to generate your roadmap.")
    elif not current_skills.strip():
        st.error("❌ Please enter your current skills.")
    elif not target_role.strip():
        st.error("❌ Please specify your target job role.")
    else:
        with st.spinner(f"🤖 Gemini AI is analyzing skill gaps for '{target_role}' and designing your 8-week plan..."):
            try:
                data = call_gemini_api(api_key_to_use, current_skills, target_role, hours_per_week)
                st.session_state["roadmap_result"] = data
                st.session_state["active_skills"] = current_skills
                st.session_state["active_role"] = target_role
                st.session_state["active_hours"] = hours_per_week
                st.balloons()
            except Exception as e:
                st.error(f"Generation failed: {e}")

if "roadmap_result" in st.session_state:
    data = st.session_state["roadmap_result"]
    cur_skills = st.session_state.get("active_skills", current_skills)
    t_role = st.session_state.get("active_role", target_role)
    t_hours = st.session_state.get("active_hours", hours_per_week)

    st.markdown(f"## 🎯 Career Transformation Plan: {t_role}")

    # Top Overview Metrics
    readiness = data.get("readiness_score", 45)
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Starting Readiness", f"{readiness}%")
    with m2:
        st.metric("Total Weeks", "8 Weeks")
    with m3:
        st.metric("Weekly Hours", f"{t_hours} hrs/wk")
    with m4:
        st.metric("Portfolio Projects", "3 Mini Projects")

    st.info(f"💡 **Advisor Note:** {data.get('executive_summary', '')}")

    st.markdown("---")

    # OUTPUT 1: Table of Skills You Have vs Skills to Learn
    st.markdown("### 📊 1. Skills You Have vs Skills to Learn (Skill Gap Analysis)")
    gap_data = data.get("skill_gap_analysis", [])
    if gap_data:
        df = pd.DataFrame(gap_data)
        # Rename columns for clarity
        rename_map = {
            "domain_category": "Domain / Category",
            "skills_you_have": "Skills You Have",
            "skills_to_learn": "Skills to Learn",
            "priority": "Priority"
        }
        df = df.rename(columns=rename_map)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.write("No skill gap records returned.")

    st.markdown("---")

    # OUTPUT 2: 8-Week Week-by-Week Learning Roadmap
    st.markdown("### 📅 2. 8-Week Week-by-Week Learning Roadmap")
    roadmap = data.get("eight_week_roadmap", [])
    
    # Render weeks cleanly with expanders
    for w in roadmap:
        w_num = w.get("week_number", "")
        w_theme = w.get("theme", "")
        w_topics = w.get("key_topics", [])
        w_milestone = w.get("weekly_milestone", "")

        with st.expander(f"📍 **Week {w_num}: {w_theme}**", expanded=(w_num in [1, 2])):
            w_col1, w_col2 = st.columns([1.5, 1])
            with w_col1:
                st.markdown("**Key Topics to Master:**")
                for topic in w_topics:
                    st.markdown(f"- {topic}")
            with w_col2:
                st.markdown("**🏁 Weekly Hands-on Milestone:**")
                st.success(w_milestone)

    st.markdown("---")

    # OUTPUT 3: 3 Mini Portfolio Project Ideas
    st.markdown("### 💼 3. Mini Portfolio Projects for Your Resume")
    st.markdown("Building these three projects proves your practical competencies to hiring managers:")
    
    projects = data.get("portfolio_projects", [])
    p_cols = st.columns(3)
    for idx, p in enumerate(projects[:3]):
        with p_cols[idx]:
            p_title = p.get("title", f"Project {idx+1}")
            p_desc = p.get("description", "")
            p_stack = p.get("tech_stack", [])
            p_impact = p.get("resume_impact", "")

            st.markdown(f"""
            <div class="project-card">
                <div class="project-title">🚀 {p_title}</div>
                <p style="font-size: 0.9rem; color: #4B5563;">{p_desc}</p>
                <div style="margin-top: 10px; margin-bottom: 10px;">
                    {"".join([f'<span class="tech-pill">{t}</span>' for t in p_stack])}
                </div>
                <div style="background: #F0FDF4; border: 1px solid #BBF7D0; padding: 10px; border-radius: 8px; font-size: 0.85rem; color: #166534;">
                    <b>Resume Impact:</b> {p_impact}
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # Download Button for Submission / Offline Study
    md_content = generate_markdown_download(data, cur_skills, t_role, t_hours)
    st.download_button(
        label="📥 Download Complete Roadmap as Markdown (.md)",
        data=md_content,
        file_name=f"{t_role.replace(' ', '_')}_8_Week_Roadmap.md",
        mime="text/markdown",
        use_container_width=True
    )
