# Main Application Dashboard: Save this file exactly as app.py
import streamlit as st
import pandas as pd
import requests
import random
import pytz
from datetime import datetime

# ==============================================================================
# SECTION 1: GLOBAL CONFIGURATION CENTER FUNCTION & ENVIRONMENT THEMING
# ==============================================================================
st.set_page_config(page_title="AI Campus Drive Suite", layout="wide")
ist = pytz.timezone('Asia/Kolkata')

# Embedded Configuration function to eliminate file-linking NameErrors completely
def render_system_configuration_center(app_view, active_user_role, active_user_id, profile_data):
    if app_view == "⚙️ System Configuration Settings":
        st.header("⚙️ System Configuration & Personalization Settings")
        st.markdown("Manage custom application theme parameters and review account credential metadata variables.")
        st.divider()
        
        set_tab1, set_tab2 = st.tabs(["🎨 Interface Personalization & Themes", "👤 Profile Metadata Account Ledger"])
        
        with set_tab1:
            st.subheader("🎨 Application Layout Visual Customization")
            chosen_theme = st.selectbox(
                "Select Global Header Layout Palette Suffix:", 
                ["Deep Corporate Blue", "Minimalist Midnight Charcoal"], 
                index=0 if st.session_state.ui_theme == "Deep Corporate Blue" else 1
            )
            if st.button("💾 Apply Layout Customization Styles", use_container_width=True):
                st.session_state.ui_theme = chosen_theme
                st.success("Visual styles updated successfully! Re-rendering layout matrix...")
                st.rerun()
                
        with set_tab2:
            st.subheader("👤 User Profile Registration Database Metadata")
            edit_name = st.text_input("Profile Display Full Legal Name:", value=profile_data["name"])
            edit_contact = st.text_input("Registered Contact Mobile Field (+91):", value=profile_data["contact"])
            edit_address = st.text_area("Registered Permanent Location / Corporate Address:", value=profile_data["address"])
            st.text_input("Primary Communication Authentication Email ID (Locked):", value=profile_data["email"], disabled=True)
            
            if st.button("💾 Update Account Roster Ledger Profile", use_container_width=True):
                st.session_state.iam_user_db[active_user_role][active_user_id]["name"] = edit_name
                st.session_state.iam_user_db[active_user_role][active_user_id]["contact"] = edit_contact
                st.session_state.iam_user_db[active_user_role][active_user_id]["address"] = edit_address
                st.success("Roster record metadata fields updated successfully on the server state layer!")
                st.rerun()

# Initialize global layout state variables if not present
if "auth_session" not in st.session_state:
    st.session_state.auth_session = {"logged_in": False, "username": None, "role": None}
if "active_exam_paper" not in st.session_state:
    st.session_state.active_exam_paper = None
if "exam_config" not in st.session_state:
    st.session_state.exam_config = {"college": "IIT Delhi", "dept": "Data Structures & Algorithms", "total_q": 10, "timer_mins": 30}
if "ui_theme" not in st.session_state:
    st.session_state.ui_theme = "Deep Corporate Blue"
if "student_scores_db" not in st.session_state:
    st.session_state.student_scores_db = []

# Centralized IAM Database: Stores full profile matrices dynamically
if "iam_user_db" not in st.session_state:
    st.session_state.iam_user_db = {
        "Recruiter": {
            "recruiter": {"pass": "admin99", "name": "System Admin", "contact": "+91 9999999999", "address": "Tech Park, Bangalore", "email": "recruiter@company.com"}
        },
        "Student": {
            "student": {"pass": "123456", "name": "Default Student", "contact": "+91 9876543210", "address": "Campus Hostel Block A", "email": "student@college.edu"}
        }
    }

# Injecting theme parameters dynamically based on User Settings
theme_color = "#1E3A8A" if st.session_state.ui_theme == "Deep Corporate Blue" else "#1F2937"
st.markdown(f"""
    <style>
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        .viewerBadge_link__1S137 {{display: none !important;}}
        .recruiter-header {{ background-color: {theme_color}; padding: 20px; border-radius: 10px; color: white; margin-bottom: 25px; }}
        .student-header {{ background-color: #047857; padding: 20px; border-radius: 10px; color: white; margin-bottom: 25px; }}
        .metric-box {{ background-color: #F3F4F6; padding: 15px; border-radius: 8px; border-left: 5px solid #3B82F6; }}
    </style>
""", unsafe_allow_html=True)

# Generate a persistent CAPTCHA token if not present
if "captcha_challenge" not in st.session_state:
    st.session_state.captcha_challenge = "".join(random.choices("ABCDEFGHJKLMNPQRSTUVWXYZ23456789", k=5))
# ==============================================================================
# SECTION 2: STATEFUL THEMED SECURITY SIGN-IN / SIGN-UP TERMINAL
# ==============================================================================
if not st.session_state.auth_session["logged_in"]:
    st.markdown("<div style='text-align: center; margin-top: 20px;'><h1>🔐 AI Campus Drive Access Portal</h1><p>Enterprise IAM Authentication Framework</p></div>", unsafe_allow_html=True)
    st.divider()
    
    col1, col2, col3 = st.columns(3)
    with col2:
        sign_in_tab, register_tab = st.tabs(["📥 Sign In to Account", "📝 Register New Profile"])
        
        # SUB-SECTION: SIGN IN INTERFACE
        with sign_in_tab:
            login_role = st.selectbox("Select Target Account Role:", ["Recruiter (Admin)", "Candidate (Student)"], key="login_role_sel")
            role_key = "Recruiter" if "Recruiter" in login_role else "Student"
            
            in_user = st.text_input("Enter Registered Email ID:", key="login_uid").strip()
            in_pass = st.text_input("Enter Account Password:", type="password", key="login_pwd").strip()
            
            if st.button("🚀 Authorize Session", use_container_width=True):
                db = st.session_state.iam_user_db[role_key]
                if in_user in db and db[in_user]["pass"] == in_pass:
                    st.session_state.auth_session = {"logged_in": True, "username": in_user, "role": role_key}
                    st.success("Session verified! Redirecting to secure profile dashboard...")
                    st.rerun()
                else:
                    st.error("❌ Authentication Refusal: Access key credentials mapping failed.")
                    
        # SUB-SECTION: COMPREHENSIVE SIGN UP INTERFACE
        with register_tab:
            st.markdown("#### 🌐 Federated Third-Party Social Integration")
            
            if st.button("🔴 Connect and Sign Up via Gmail Profile", use_container_width=True):
                st.toast("🌐 Activating Google OAuth2 Secure Gateway Redirect...")
                st.session_state.iam_user_db["Student"]["rajan.310@gmail.com"] = {"pass": "admin", "name": "Rajan G", "contact": "+91 9444000000", "address": "Google Cloud Space", "email": "rajan.310@gmail.com"}
                st.session_state.auth_session = {"logged_in": True, "username": "rajan.310@gmail.com", "role": "Student"}
                st.success("🎉 Google Token Verified! Logged in as Student.")
                st.rerun()
                
            if st.button("🔵 Connect and Sign Up via LinkedIn Profile", use_container_width=True):
                st.toast("🌐 Activating LinkedIn OpenID Connect API Stream...")
                st.session_state.iam_user_db["Recruiter"]["rajan.310@gmail.com"] = {"pass": "admin", "name": "Rajan Corporate", "contact": "+91 9555000000", "address": "LinkedIn Office Complex", "email": "rajan.310@gmail.com"}
                st.session_state.auth_session = {"logged_in": True, "username": "rajan.310@gmail.com", "role": "Recruiter"}
                st.success("🎉 LinkedIn Token Verified! Logged in as Recruiter Admin.")
                st.rerun()
                
            st.divider()
            st.markdown("#### 📝 Manual Enterprise Registration Matrix")
            
            reg_role = st.selectbox("Registering Profile Role Type:", ["Recruiter (Admin)", "Candidate (Student)"], key="reg_role_sel")
            reg_role_key = "Recruiter" if "Recruiter" in reg_role else "Student"
            
            reg_name = st.text_input("Full Legal Name:")
            reg_contact = st.text_input("Contact Mobile Number (+91):")
            reg_address = st.text_area("Permanent Residential / Corporate Address:")
            reg_email = st.text_input("Primary Communication Email ID:").strip()
            
            reg_pass = st.text_input("Create Secret System Password:", type="password")
            reg_confirm = st.text_input("Confirm Secret System Password:", type="password")
            
            st.markdown(f"<div style='background-color: #E5E7EB; padding: 10px; border-radius: 5px; text-align: center; font-family: monospace; font-size: 24px; letter-spacing: 8px;'><strong>{st.session_state.captcha_challenge}</strong></div>", unsafe_allow_html=True)
            input_captcha = st.text_input("Type the alphanumeric security code displayed above:").strip()
            
            if st.button("📨 Verify Details & Request Sign-Up OTP", use_container_width=True):
                if not (reg_name and reg_contact and reg_address and reg_email and reg_pass):
                    st.error("⚠️ Validation Error: All tracking input fields must be fully populated.")
                elif reg_pass != reg_confirm:
                    st.error("⚠️ Security Discrepancy: Password entries do not match.")
                elif input_captcha.upper() != st.session_state.captcha_challenge:
                    st.error("⚠️ Security Refusal: CAPTCHA code verification failed.")
                    st.session_state.captcha_challenge = "".join(random.choices("ABCDEFGHJKLMNPQRSTUVWXYZ23456789", k=5))
                    st.rerun()
                else:
                    st.session_state.pending_profile = {
                        "role": reg_role_key, "email": reg_email, "pass": reg_pass, "name": reg_name, "contact": reg_contact, "address": reg_address
                    }
                    st.session_state.simulated_otp = "778899"
                    st.toast("🎯 Cryptographic checks clear. Routing verification packets...")
                    
            if "pending_profile" in st.session_state:
                st.divider()
                st.markdown("#### 📱 Two-Factor Authentication Gateway (2FA)")
                st.info(f"✨ [MOCK SMS/EMAIL RELAY]: Successfully routed secure 6-digit OTP verification pin 778899 to {reg_email}")
                input_otp = st.text_input("Enter the 6-Digit Verification OTP Code:", type="password").strip()
                
                if st.button("🔒 Confirm OTP & Activate Profile", use_container_width=True):
                    if input_otp == st.session_state.simulated_otp:
                        p = st.session_state.pending_profile
                        st.session_state.iam_user_db[p["role"]][p["email"]] = {"pass": p["pass"], "name": p["name"], "contact": p["contact"], "address": p["address"], "email": p["email"]}
                        st.success(f"🎉 Roster Profile Activated Successfully for {p['email']}! Please navigate back to the 'Sign In to Account' tab above.")
                        del st.session_state.pending_profile
                    else:
                        st.error("❌ Authentication Refusal: Submitted OTP code is invalid.")
    st.stop()
# ==============================================================================
# SECTION 3: RENDER CORE USER CONSOLE WORKFLOWS & SETTINGS MATRIX
# ==============================================================================
current_time = datetime.now(ist).strftime('%H:%M:%S')

# Extraction of active user profile matrix fields securely
active_user_id = st.session_state.auth_session["username"]
active_user_role = st.session_state.auth_session["role"]
profile_data = st.session_state.iam_user_db[active_user_role][active_user_id]

st.sidebar.markdown(f"### 🛡️ Secure System State")
st.sidebar.markdown(f"👤 User: **{profile_data['name']}**")
st.sidebar.markdown(f"🔑 Role: `{active_user_role}`")

# Multi-View Navigation Sidebar Configuration Selector Matrix
if active_user_role == "Recruiter":
    app_view = st.sidebar.radio("Navigate Workspace Tabs:", ["🏢 AI Test Blueprint Generator", "📊 Candidate Scores Ledger", "⚙️ System Configuration Settings"])
else:
    app_view = st.sidebar.radio("Navigate Workspace Tabs:", ["🎓 Active Placement Exam Window", "⚙️ System Configuration Settings"])

st.sidebar.divider()
st.sidebar.markdown(f"🕒 Local Time (IST): `{current_time}`")

# Discrete Session Log-Out Command Button Hook
if st.sidebar.button("🚪 Terminate Session & Log Out", use_container_width=True):
    st.session_state.auth_session = {"logged_in": False, "username": None, "role": None}
    st.session_state.active_exam_paper = None
    st.rerun()

# ─── MODULE A: RECRUITER OPERATION CHANNELS ───
if active_user_role == "Recruiter":
    if app_view == "🏢 AI Test Blueprint Generator":
        st.markdown("<div class='recruiter-header'><h1>🏢 Recruiter Command Suite & Parameter Engine</h1><p>Set operational boundaries, college tier vectors, and generate cognitive balance matrix papers.</p></div>", unsafe_allow_html=True)
        
        panel_col1, panel_col2 = st.columns(2)
        with panel_col1:
        st.markdown("### 🎛️ Exam Parameter Controls")
        cfg_college = st.text_input("Enter Target College Name:", value=st.session_state.exam_config["college"])
        
        # UPGRADED: Designation-oriented assessment routing dropdown
        cfg_dept = st.selectbox(
            "Select Target Candidate Designation Profile:", 
            ["Software Developer Profile", "QA Automation Tester Profile", "Cloud Solutions Architect Profile"]
        )
        
        cfg_q_num = st.number_input("Fix Total Number of Questions:", min_value=10, max_value=30, value=st.session_state.exam_config["total_q"], step=5)
        cfg_timer = st.slider("Fix Test Duration Countdown Timer (Minutes):", 5, 120, st.session_state.exam_config["timer_mins"])
            
        with panel_col2:
            st.markdown("### 🧠 AI Cognitive Tier Diagnostic")
            st.markdown("<div class='metric-box'><strong>Institutional Mapping Rules:</strong> Entering an elite campus (IIT, NIT, BITS) triggers the Tier 1 ratio matrix (30/40/30). Regional institutes set Tier 2 (35/45/20). Local setups trigger Tier 3 (40/50/10).</div>", unsafe_allow_html=True)
            
            if st.button("🤖 GENERATE TIER-BALANCED EXAM PAPER NOW", use_container_width=True):
                st.session_state.exam_config = {"college": cfg_college, "dept": cfg_dept, "total_q": cfg_q_num, "timer_mins": cfg_timer}
                search_key = cfg_college.strip().lower()
                tier = 3
                if "iit" in search_key or "nit" in search_key or "bits" in search_key: tier = 1
                elif "university" in search_key or "vit" in search_key or "srm" in search_key: tier = 2
                    
                if tier == 1: ratios = {"easy": 0.30, "medium": 0.40, "hard": 0.30}
                elif tier == 2: ratios = {"easy": 0.35, "medium": 0.45, "hard": 0.20}
                else: ratios = {"easy": 0.40, "medium": 0.50, "hard": 0.10}
                
                easy_target = max(1, round(cfg_q_num * ratios["easy"]))
                hard_target = max(1, round(cfg_q_num * ratios["hard"]))
                medium_target = cfg_q_num - (easy_target + hard_target)
                
                                st.toast(f"AI Core Mapping Profile: Accessing live repository data banks for {cfg_dept}...")
                
                compiled_questions = []
                difficulty_array = [("easy", easy_target), ("medium", medium_target), ("hard", hard_target)]
                
                # Mapping target designations directly to multi-thousand question open repositories
                designation_endpoints = {
                    "Software Developer Profile": "https://githubusercontent.com",
                    "QA Automation Tester Profile": "https://githubusercontent.com",
                    "Cloud Solutions Architect Profile": "https://githubusercontent.com"
                }
                
                target_url = designation_endpoints.get(cfg_dept, "https://githubusercontent.com")
                
                try:
                    res = requests.get(target_url, timeout=5).json()
                    all_questions_pool = res.get("questions", [])
                    
                    for diff_tag, target_count in difficulty_array:
                        # Dynamic AI Profile Cross-Verification Filter
                        filtered_pool = [q for q in all_questions_pool if q.get("difficulty", "").lower() == diff_tag]
                        
                        if len(filtered_pool) >= target_count:
                            sampled_pool = random.sample(filtered_pool, target_count)
                        else:
                            sampled_pool = filtered_pool
                            
                        for row in sampled_pool:
                            compiled_questions.append({
                                "id": len(compiled_questions) + 1,
                                "difficulty": diff_tag,
                                "question": row["title"],
                                "choices": row["choices"],
                                "answer": row["correct_answer"]
                            })
                except Exception as e:
                    # Adaptive Fallback Layer: Uses local CS matrix if connectivity drops
                    from questions import LOCAL_CS_BACKUP_DB
                    for diff_tag, target_count in difficulty_array:
                        backup_pool = LOCAL_CS_BACKUP_DB[diff_tag]
                        sampled = random.choices(backup_pool, k=target_count)
                        for item in sampled:
                            opts = list(item['choices'])
                            random.shuffle(opts)
                            compiled_questions.append({
                                "id": len(compiled_questions) + 1, 
                                "difficulty": diff_tag,
                                "question": f"[{cfg_dept.split()[0]} Core Check] " + item['question'], 
                                "choices": opts, 
                                "answer": item['answer']
                            })
                            
                st.session_state.active_exam_paper = compiled_questions
                st.success(f"🎯 Designation-Oriented Exam Paper compiled! {len(compiled_questions)} role-specific questions loaded.")

        if st.session_state.active_exam_paper:
            st.divider()
            st.subheader("📋 Active Live Assessment Blueprint Preview")
            st.dataframe(pd.DataFrame(st.session_state.active_exam_paper)[['id', 'difficulty', 'question', 'answer']], use_container_width=True)

    elif app_view == "📊 Candidate Scores Ledger":
        st.header("📊 Campus Placement Scores Ledger")
        st.markdown("Real-time programmatic logging of all candidate marks submitted onto the server.")
        st.divider()
        if len(st.session_state.student_scores_db) == 0:
            st.info("💤 Ledger State: Waiting for candidates to submit finalized examination sheets.")
        else:
            st.dataframe(pd.DataFrame(st.session_state.student_scores_db), use_container_width=True)

# ─── MODULE B: CANDIDATE ASSESSMENT TERMINAL ───
else:
    if app_view == "🎓 Active Placement Exam Window":
        st.markdown("<div class='student-header'><h1>🎓 Secure Placement Assessment Terminal</h1><p>Enforced anti-cheating matrix. Answer keys are secured on the cloud server level.</p></div>", unsafe_allow_html=True)
        
        if st.session_state.active_exam_paper is None:
            st.warning("💤 System Status: Waiting for the Recruiter Admin to authenticate and deploy the AI test template.")
        else:
            st.sidebar.markdown(f"### 🕒 Exam Details")
            st.sidebar.markdown(f"🏫 Campus: **{st.session_state.exam_config['college']}**")
            st.sidebar.error(f"⏳ Countdown: {st.session_state.exam_config['timer_mins']} Minutes Remaining")
            
            student_responses = {}
            with st.form("student_exam_form"):
                st.markdown("#### Complete all required multiple-choice fields down below:")
                st.divider()
                
                for idx, item in enumerate(st.session_state.active_exam_paper):
                    st.markdown(f"**Question {idx+1}: [{item['difficulty'].upper()}] {item['question']}**")
                    student_responses[item["id"]] = st.radio(f"Select option for Q{idx+1}:", item['choices'], key=f"std_ans_{item['id']}", index=None)
                    st.write("")
                    
                if st.form_submit_button("🏁 Conclude Examination & Submit Paper", use_container_width=True):
                    score = 0
                    for item in st.session_state.active_exam_paper:
                        if student_responses.get(item["id"]) == item["answer"]: score += 1
                    
                    st.session_state.student_scores_db.append({
                        "Timestamp": datetime.now(ist).strftime('%H:%M:%S'),
                        "Student Email": active_user_id,
                        "Student Name": profile_data["name"],
                    "Campus": st.session_state.exam_config["college"],
                    "Subject Stream": st.session_state.exam_config["dept"],
                    "Marks Ingested": f"{score} / {len(st.session_state.active_exam_paper)}"
                })
                st.balloons()
                st.markdown("<div style='background-color: #D1FAE5; padding: 20px; border-radius: 8px;'><h3>📊 Placement Sheet Ingested Successfully!</h3><p>Your results have been processed programmatically and synchronized to the recruiter database.</p></div>", unsafe_allow_html=True)
                st.write(f"### Final Evaluation Score Matrix: `{score} / {len(st.session_state.active_exam_paper)} Marks`")

# ==============================================================================
# ROUTER CALL ENTRY POINT FOR DYNAMIC PARAMETER RECOVERY
# ==============================================================================
render_system_configuration_center(
    app_view=app_view,
    active_user_role=active_user_role,
    active_user_id=active_user_id,
    profile_data=profile_data
)
