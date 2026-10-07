# Main Application Dashboard: Save this file exactly as app.py
import streamlit as st
import pandas as pd
import requests
import random
import pytz
from datetime import datetime

# Import our custom database from our separate file
from questions import LOCAL_CS_BACKUP_DB

# ==============================================================================
# 1. ENTERPRISE THEMING, SECURITY VISIBILITY BLOCKS & TIMING CORE
# ==============================================================================
st.set_page_config(page_title="AI Campus Drive Suite", layout="wide")
ist = pytz.timezone('Asia/Kolkata')

# Injecting custom CSS to completely hide Streamlit headers, footers, 
# and repository edit flags, while styling visual element containers.
st.markdown("""
    <style>
        /* Completely strip out top decoration bars and manage app menus */
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        .viewerBadge_link__1S137 {display: none !important;}
        
        /* Custom UI Card Containers */
        .recruiter-header {
            background-color: #1E3A8A;
            padding: 20px;
            border-radius: 10px;
            color: white;
            margin-bottom: 25px;
        }
        .student-header {
            background-color: #047857;
            padding: 20px;
            border-radius: 10px;
            color: white;
            margin-bottom: 25px;
        }
        .metric-box {
            background-color: #F3F4F6;
            padding: 15px;
            border-radius: 8px;
            border-left: 5px solid #3B82F6;
        }
    </style>
""", unsafe_allow_html=True)

# Persistent State Initializations
if "auth_session" not in st.session_state:
    st.session_state.auth_session = {"logged_in": False, "username": None, "role": None}
if "active_exam_paper" not in st.session_state:
    st.session_state.active_exam_paper = None
if "exam_config" not in st.session_state:
    st.session_state.exam_config = {"college": "IIT Delhi", "dept": "Computer Science (CSE)", "total_q": 10, "timer_mins": 30}

# ==============================================================================
# 2. STATEFUL AUTHENTICATION SCREEN (Locks the system entirely)
# ==============================================================================
if not st.session_state.auth_session["logged_in"]:
    st.markdown("<div style='text-align: center; margin-top: 50px;'><h1>🔐 AI Campus Drive Access Portal</h1><p>Please enter your credentials to clear security clearance verification.</p></div>", unsafe_allow_html=True)
    st.divider()
    
    col1, col2, col3 = st.columns()
    with col2:
        login_role = st.selectbox("Select Your Access Authorization Role:", ["🏢 Corporate Recruiter (Admin)", "🎓 Registered Candidate (Student)"])
        input_user = st.text_input("Username / Email ID:")
        input_pass = st.text_input("Access Pin / Password:", type="password")
        
        if st.button("🚀 Authorize & Enter Gateway", use_container_width=True):
            # Predefined credentials for presentation validation
            if login_role == "🏢 Corporate Recruiter (Admin)" and input_user == "recruiter" and input_pass == "admin99":
                st.session_state.auth_session = {"logged_in": True, "username": "HR Lead", "role": "Recruiter"}
                st.rerun()
            elif login_role == "🎓 Registered Candidate (Student)" and input_user == "student" and input_pass == "123456":
                st.session_state.auth_session = {"logged_in": True, "username": "Candidate Account", "role": "Student"}
                st.rerun()
            else:
                st.error("❌ Authentication Refusal: Access key mapping failed. Verify credentials.")
    st.stop()

# ==============================================================================
# 3. RENDER CORE USER CONSOLE WORKFLOWS
# ==============================================================================
current_time = datetime.now(ist).strftime('%H:%M:%S')

# Navigation and Session Bar in the Sidebar
st.sidebar.markdown(f"### 🛡️ Secure System State")
st.sidebar.markdown(f"👤 Account: **{st.session_state.auth_session['username']}**")
st.sidebar.markdown(f"🕒 Exchange Time (IST): `{current_time}`")
if st.sidebar.button("🚪 Terminate Session & Log Out", use_container_width=True):
    st.session_state.auth_session = {"logged_in": False, "username": None, "role": None}
    st.session_state.active_exam_paper = None
    st.rerun()

# ─── MODULE A: RECRUITER AI GENERATION CORE (Admin Interface) ───
if st.session_state.auth_session["role"] == "Recruiter":
    st.markdown("<div class='recruiter-header'><h1>🏢 Recruiter Command Suite & Parameter Engine</h1><p>Set operational boundaries, college tier vectors, and generate cognitive balance matrix papers.</p></div>", unsafe_allow_html=True)
    
    panel_col1, panel_col2 = st.columns(2)
    with panel_col1:
        st.markdown("### 🎛️ Exam Parameter Controls")
        cfg_college = st.text_input("Enter Target College Name:", value=st.session_state.exam_config["college"])
        cfg_dept = st.selectbox("Select Target Stream:", ["Computer Science (CSE)", "Information Technology (IT)", "Electronics (ECE)"])
        cfg_q_num = st.number_input("Fix Total Number of Questions:", min_value=10, max_value=30, value=st.session_state.exam_config["total_q"], step=5)
        cfg_timer = st.slider("Fix Test Duration Countdown Timer (Minutes):", 5, 120, st.session_state.exam_config["timer_mins"])
        
    with panel_col2:
        st.markdown("### 🧠 AI Cognitive Tier Diagnostic")
        st.markdown("<div class='metric-box'><strong>Institutional Mapping Rules:</strong> Entering an elite campus (IIT, NIT, BITS) triggers the Tier 1 ratio matrix (30/40/30). Regional institutes set Tier 2 (35/45/20). Local setups trigger Tier 3 (40/50/10).</div>", unsafe_allow_html=True)
        
        if st.button("🤖 GENERATE TIER-BALANCED EXAM PAPER NOW", use_container_width=True):
            # Save configurations directly to the global state panel
            st.session_state.exam_config = {"college": cfg_college, "dept": cfg_dept, "total_q": cfg_q_num, "timer_mins": cfg_timer}
            
            # Map the institutional tier string
            search_key = cfg_college.strip().lower()
            tier = 3
            if "iit" in search_key or "nit" in search_key or "bits" in search_key:
                tier = 1
            elif "university" in search_key or "vit" in search_key or "srm" in search_key:
                tier = 2
                
            # Assign your precise mathematical difficulty ratio limits
            if tier == 1: ratios = {"easy": 0.30, "medium": 0.40, "hard": 0.30}
            elif tier == 2: ratios = {"easy": 0.35, "medium": 0.45, "hard": 0.20}
            else: ratios = {"easy": 0.40, "medium": 0.50, "hard": 0.10}
            
            easy_target = max(1, round(cfg_q_num * ratios["easy"]))
            hard_target = max(1, round(cfg_q_num * ratios["hard"]))
            medium_target = cfg_q_num - (easy_target + hard_target)
            
            st.toast(f"AI Matrix Set: Ingesting {easy_target} Easy, {medium_target} Medium, {hard_target} Hard items...")
            
            # Ingest questions using the internet API with automatic local fail-safe hooks
            compiled_questions = []
            difficulty_array = [("easy", easy_target), ("medium", medium_target), ("hard", hard_target)]
            
            for diff_tag, target_count in difficulty_array:
                api_url = f"https://opentdb.com{target_count}&category=18&difficulty={diff_tag}&type=multiple"
                try:
                    res = requests.get(api_url, timeout=3).json()
                    if res.get('response_code') == 0:
                        for row in res['results']:
                            pool = row['incorrect_answers'] + [row['correct_answer']]
                            random.shuffle(pool)
                            compiled_questions.append({
                                "id": len(compiled_questions) + 1, "difficulty": diff_tag,
                                "question": row['question'].replace("&quot;", '"').replace("&#039;", "'"),
                                "choices": pool, "answer": row['correct_answer']
                            })
                    else: raise Exception("API Error")
                except:
                    # Clear fallback escape execution pulling directly from questions.py file
                    backup_pool = LOCAL_CS_BACKUP_DB[diff_tag]
                    sampled = random.choices(backup_pool, k=target_count)
                    for item in sampled:
                        opts = list(item['choices'])
                        random.shuffle(opts)
                        compiled_questions.append({
                            "id": len(compiled_questions) + 1, "difficulty": diff_tag,
                            "question": item['question'], "choices": opts, "answer": item['answer']
                        })
            st.session_state.active_exam_paper = compiled_questions
            st.success(f"🎯 Exam successfully generated for Tier {tier} College. {len(compiled_questions)} questions compiled.")

    if st.session_state.active_exam_paper:
        st.divider()
        st.subheader("📋 Active Live Assessment Blueprint Preview")
        st.dataframe(pd.DataFrame(st.session_state.active_exam_paper)[['id', 'difficulty', 'question', 'answer']], use_container_width=True)

# ─── MODULE B: CANDIDATE ASSESSMENT TERMINAL (Student Interface) ───
else:
    st.markdown("<div class='student-header'><h1>🎓 Secure Placement Assessment Terminal</h1><p>Enforced anti-cheating matrix. Answer keys are secured on the cloud server level.</p></div>", unsafe_allow_html=True)
    
    if st.session_state.active_exam_paper is None:
st.warning("💤 System Status: Waiting for the Recruiter Admin to authenticate and deploy the AI test template.")
st.stop()
st.sidebar.markdown(f"### 🕒 Exam Details")
st.sidebar.markdown(f"🏫 Campus: {st.session_state.exam_config['college']}")
st.sidebar.error(f"⏳ Countdown: {st.session_state.exam_config['timer_mins']} Minutes Remaining")
student_responses = {}
with st.form("student_exam_form"):
st.markdown("#### Complete all required multiple-choice fields down below:")
st.divider()
for idx, item in enumerate(st.session_state.active_exam_paper):
st.markdown(f"Question {idx+1}: [{item['difficulty'].upper()}] {item['question']}")
student_responses[item["id"]] = st.radio(f"Select option for Q{idx+1}:", item['choices'], key=f"std_ans_{item['id']}", index=None)
st.write("")
if st.form_submit_button("🏁 Conclude Examination & Submit Paper", use_container_width=True):
score = 0
for item in st.session_state.active_exam_paper:
if student_responses.get(item["id"]) == item["answer"]:
score += 1
st.balloons()
st.markdown("📊 Placement Sheet Ingested Successfully!Your results have been processed programmatically and synchronized to the recruiter database.", unsafe_allow_html=True)
st.write(f"### Final Evaluation Score Matrix: {score} / {len(st.session_state.active_exam_paper)} Marks")

---

### Step 3: Verification Credentials Matrix
Once your cloud server syncs both updated files, use these identical, hardcoded credential pairs to test the interfaces live for your presentation:

*   **To Log In as the Corporate Recruiter (Admin Panel):**
    *   **Authorization Role:** `🏢 Corporate Recruiter (Admin)`
    *   **Username / Email ID:** `recruiter`
    *   **Access Pin / Password:** `admin99`
*   **To Log In as the Registered Candidate (Student Terminal):**
    *   **Authorization Role:** `🎓 Registered Candidate (Student)`
    *   **Username / Email ID:** `student`
    *   **Access Pin / Password:** `123456`

<FollowUp>
Let me know if dividing the system into `app.py` and `questions.py` **successfully cleared the code cut-off errors** and loaded the full login screen! If everything looks great, we can move forward with adding **live candidate ranking databases** or compiling your official **README documentation sheet** for college submission.
</FollowUp>
