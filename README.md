# AI Career Roadmap & Skill Gap Finder 🗺️

> **Task 2: Prototype or Model Creation using AI**  
> **Problem Statement Selected:** #4 - AI Career Roadmap & Skill Gap Finder  
> **Tech Stack:** Python 3.10+, Streamlit, Google Gemini API, Pandas  

---

## 📌 Problem Overview
Students frequently know the job title they desire (e.g., *Data Scientist*, *Full Stack Developer*, *Cloud/DevOps Engineer*), but they face uncertainty regarding:
1. What skills they are missing compared to market expectations.
2. What order to learn those skills in.
3. How to structure their limited weekly study hours effectively over time.
4. What hands-on portfolio projects will actually prove their competence on a resume.

This app solves this problem by taking the student's current skills, target role, and weekly time budget, querying **Google Gemini** with a structured curriculum prompt, and rendering a personalized **8-week learning plan with 3 portfolio projects**.

---

## 🎯 Required Inputs & Outputs (Verification Checklist)

| Criteria | Required in Assignment | Implemented in This App |
| :--- | :--- | :---: |
| **Input 1** | Current skills (e.g. C, basic Python, HTML) | ✅ Multi-line input with 1-click presets |
| **Input 2** | Target job role (e.g. Data Scientist) | ✅ Clean text input |
| **Input 3** | Hours per week available to study | ✅ Interactive slider with dynamic total hour computation |
| **Output 1** | Skills already have vs skills to learn (as a table) | ✅ Rendered as an interactive, styled DataFrame |
| **Output 2** | 8-week week-by-week learning roadmap | ✅ Expandable 8-week cards with key topics & weekly milestones |
| **Output 3** | 3 mini project ideas for the portfolio | ✅ 3 cards with titles, tech stack pills, and recruiter resume impact |
| **Bonus** | Downloadable roadmap file | ✅ "Download Complete Roadmap as Markdown (.md)" button |

---

## 🛠️ Setup & Running Instructions

### 1. Prerequisites
- Python 3.9+ installed.
- Free Gemini API key from [Google AI Studio](https://aistudio.google.com/).

### 2. Install Dependencies
Open your terminal in this directory:
```bash
cd C:\Users\nipun\.gemini\antigravity\scratch\ai-career-roadmap
pip install streamlit google-genai pandas python-dotenv
```

### 3. API Key Configuration
Create a `.env` file (copied from `.env.example`):
```env
GEMINI_API_KEY=your_gemini_api_key_here
```
*(Or enter it directly into the password box in the sidebar when running the app).*

### 4. Run the Streamlit Application
```bash
streamlit run app.py
```
The app will open automatically in your browser at `http://localhost:8501`.

---

## 💡 Quick 1-Click Demo
1. Enter your Gemini API key in the left sidebar.
2. Select **"Data Scientist"** from the *Quick Sample Presets* dropdown and click **"⚡ Load Preset Data"**.
3. Notice that:
   - Current skills: `C, basic Python, HTML, basic SQL, Excel`
   - Target Role: `Data Scientist`
   - Available study time: `12 hours/week`
4. Click **🚀 Generate My Custom 8-Week Roadmap**.
5. Within 5–8 seconds, view:
   - Summary and Readiness Score (e.g., 55%).
   - **Table:** Skills You Have vs Skills to Learn with Priority.
   - **8 Expandable Cards:** Week-by-Week syllabus from Week 1 to Week 8.
   - **3 Project Cards:** Tailored portfolio projects with tech stacks and resume impact.
   - **Download Button:** Export full roadmap as Markdown.
6. Take a screenshot for your submission!

---

## 🎓 Viva / Evaluation Explanation

When presenting this project to your evaluator, explain the architecture in 3 simple points:

1. **Prompt Engineering & Schema Enforcement:**
   - In [`app.py`](file:///C:/Users/nipun/.gemini/antigravity/scratch/ai-career-roadmap/app.py#L74-L186), we use a structured JSON schema requiring `skill_gap_analysis`, `eight_week_roadmap` (exactly 8 weeks), and `portfolio_projects` (exactly 3 projects).
   - This ensures deterministic, machine-parseable output from Gemini rather than random paragraphs of text.

2. **Skill Gap Comparison Logic:**
   - Instead of static hardcoded roadmaps, Gemini performs semantic comparison. If a student knows *C* and *Python*, Gemini recognizes foundational algorithmic proficiency, so it focuses the 8 weeks directly on intermediate data pipelines (Pandas, SQL), machine learning fundamentals (Scikit-Learn), and deployment (Streamlit).

3. **Time-Aware Curriculum Planning:**
   - The prompt explicitly takes the student's weekly study budget (e.g. 12 hours/week) into account so the weekly milestones are realistic and achievable.

---

## 📦 Submission Files
- **Screenshot:** Save as `RollNo_Name_Output.jpg`
- **ZIP File:** Run:
  ```powershell
  .\package_submission.ps1 -RollNo "YOUR_ROLL_NO" -Name "YOUR_NAME"
  ```
  This creates `RollNo_Name_Code.zip` cleanly without your secret `.env` file.
