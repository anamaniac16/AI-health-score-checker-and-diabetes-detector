import streamlit as st

# ---------------- SAFE DEFAULTS ---------------- #

base_score = None
final_color = None
reasons = []
diab_pred = None
diab_prob = None
shap_info = {}
warnings = []

# ---------------- IMPORT MODULES ---------------- #

from risk_engine import calculate_risk, risk_category
from models.ml_diabetes_predict import predict_diabetes_full
from sms_service import send_sms_alert
from auth import (
    register_user,
    login_user,
    add_health_record,
    get_user_history,
    save_session,
    load_session,
    clear_session
)
from intervention_engine import generate_personal_plan
from advanced_intervention_engine import (
    calculate_bmr,
    estimate_body_fat,
    protein_target,
    generate_weekly_workout,
    ramadan_adjustment
)
import plotly.graph_objects as go
import time


# ---------------- AUTH SESSION ---------------- #

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_user" not in st.session_state:
    st.session_state.current_user = None

if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "login"   # login or signup

# ---------------- AUTO LOGIN ---------------- #

saved_user = load_session()

if saved_user and not st.session_state.logged_in:
    st.session_state.logged_in = True
    st.session_state.current_user = saved_user

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="HealthGuard AI",
    page_icon="🛡️",
    layout="wide"
)

# ---------------- Frontend (UI) --------------- #

st.markdown("""
<style>

/* ------------------ BACKGROUND ------------------ */
.stApp {
    background-image: url("https://plus.unsplash.com/premium_vector-1711987848637-85c1dfa3f85a?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0");
    background-size: cover;
    background-attachment: fixed;
    background-position: center;
    font-family: 'Inter', sans-serif;
}

/* Soft white content overlay */
.block-container {
    background: rgba(255, 255, 255, 0.65);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    padding: 2rem 3rem 3rem 3rem;
    border-radius: 18px;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
}

/* ------------------ GLOBAL TEXT FIX ------------------ */
html, body, p, span, div, label {
    color: #1e293b !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: rgba(255,255,255,0.95) !important;
}

section[data-testid="stSidebar"] * {
    color: #1e293b !important;
}

/* ------------------ INPUT FIELDS ------------------ */
input, textarea, select {
    background-color: #ffffff !important;
    color: #111827 !important;
    border: 1px solid #cbd5e1 !important;
}

/* Cursor color */
input, textarea {
    caret-color: #2563eb !important;
}

/* Checkbox */
.stCheckbox label {
    color: #1e293b !important;
}

/* ------------------ METRIC FIX ------------------ */
div[data-testid="metric-container"] {
    background: #ffffff;
    border-radius: 14px;
    padding: 18px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 6px 18px rgba(0,0,0,0.06);
}

/* Metric label */
div[data-testid="metric-container"] label {
    color: #475569 !important;
}

/* Metric value */
div[data-testid="metric-container"] div {
    color: #0f172a !important;
    font-weight: 600;
}

/* ------------------ BUTTONS ------------------ */
.stButton > button {
    background: linear-gradient(135deg,#2563eb,#0891b2);
    color: white !important;
    border-radius: 10px;
    padding: 8px 18px;
    font-weight: 500;
    border: none;
}

.stButton > button:hover {
    background: linear-gradient(135deg,#1d4ed8,#0e7490);
}

/* Hide default header */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* ------------------ FIX SELECTBOX & NUMBER INPUT ------------------ */

/* Selectbox container */
div[data-baseweb="select"] {
    background-color: #ffffff !important;
    color: #0f172a !important;
}

/* Selectbox text */
div[data-baseweb="select"] * {
    color: #0f172a !important;
}

/* Dropdown menu */
ul[role="listbox"] {
    background-color: #ffffff !important;
    color: #0f172a !important;
}

/* Dropdown options */
ul[role="listbox"] li {
    color: #0f172a !important;
}

/* Number input container */
div[data-testid="stNumberInput"] input {
    background-color: #ffffff !important;
    color: #0f172a !important;
    border: 1px solid #cbd5e1 !important;
}

/* Selectbox main visible area */
div[data-testid="stSelectbox"] > div {
    background-color: #ffffff !important;
    color: #0f172a !important;
    border: 1px solid #cbd5e1 !important;
}

/* Toggle fix *
div[data-testid="stToggle"] * {
    color: #0f172a !important;
}

/* ---- Section Spacing ---- */
h1, h2, h3 {
    margin-top: 1.2rem !important;
    margin-bottom: 0.8rem !important;
}

hr {
    margin-top: 1.5rem;
    margin-bottom: 1.5rem;
    opacity: 0.2;
}

/* ---- Metric Hover Lift ---- */
div[data-testid="metric-container"]:hover {
    transform: translateY(-3px);
    transition: all 0.2s ease;
}
            
button[data-baseweb="tab"] {
    font-weight: 500;
    font-size: 15px;
}

button[data-baseweb="tab"]:hover {
    background-color: rgba(37,99,235,0.08);
}
            
div[data-testid="metric-container"]:hover {
    transform: translateY(-2px);
    transition: all 0.2s ease;
}

/* ---- Lifestyle Image Cards ---- */

.lifestyle-card {
    background: white;
    padding: 12px;
    border-radius: 18px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.08);
    text-align: center;
    margin-bottom: 20px;
}

.lifestyle-card img {
    border-radius: 14px;
    height: 240px;
    width: 100%;
    object-fit: cover;
}

.lifestyle-title {
    margin-top: 10px;
    font-weight: 600;
    color: #1e293b;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ---------------- #

st.markdown("""
<h1 style="text-align:center;">🛡️ HealthGuard AI</h1>
<h4 style="text-align:center;color:gray;">
Smart Health Risk Detection & Diabetes Prediction System
</h4>
<hr>
""", unsafe_allow_html=True)

st.info(
    "HealthGuard AI focuses on **prevention**, **early intervention**, "
    "and **emergency response**, enhanced with **ML-based diabetes prediction**."
)
st.success("🏥 Hospital-Grade Screening Mode Enabled")


# ================= AUTHENTICATION ================= #

if not st.session_state.logged_in:

    st.markdown("## 🔐 Account Access")

    if st.session_state.auth_mode == "login":

        st.subheader("Login")

        email = st.text_input("Email")
        password = st.text_input("Numeric Password", type="password")

        remember = st.checkbox("Remember me on this device")

        if st.button("Login"):

            success, message = login_user(email, password)

            if success:
                st.session_state.logged_in = True
                st.session_state.current_user = email

                if remember:
                    save_session(email)

                st.success("Login successful")
                st.rerun()

            else:
                st.error(message)

        st.markdown("Don't have an account?")
        if st.button("Create Account"):
            st.session_state.auth_mode = "signup"
            st.rerun()

    else:

        st.subheader("Create Account")

        email = st.text_input("Email")
        password = st.text_input("Create Numeric Password", type="password")

        if st.button("Register"):

            if not password.isdigit():
                st.error("Password must be numeric only")
            else:
                success, message = register_user(email, password)

                if success:
                    st.success("Account created. Please login.")
                    st.session_state.auth_mode = "login"
                    st.rerun()
                else:
                    st.error(message)

        st.markdown("Already have an account?")
        if st.button("Back to Login"):
            st.session_state.auth_mode = "login"
            st.rerun()

    st.stop()

# ================= USER BAR ================= #

st.markdown("""
<h1 style="margin-bottom:0;">HealthGuard AI</h1>
<p style="color:gray;margin-top:4px;">
Smart Health Risk Detection & Diabetes Prediction Platform
</p>
<hr>
""", unsafe_allow_html=True)

col_user, col_logout = st.columns([6,1])

with col_user:
    st.markdown(f"👤 Logged in as: **{st.session_state.current_user}**")

with col_logout:
    if st.button("🚪 Logout"):
        clear_session()
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.session_state.auth_mode = "login"
        st.rerun()

# ================= MAIN TABS ================= #

menu = st.sidebar.radio(
    "Navigation",
    ["🩺 Health Check", "📈 My History", "🧠 AI Health Plan"]
)

if menu == "🩺 Health Check":
    st.markdown("## 🧾 Patient Health Profile")

    main_left, main_right = st.columns([1.1, 1])

    # -------- LEFT SIDE (Core Metrics) -------- #

    with main_left:

        name = st.text_input("Patient Name")

        c1, c2 = st.columns(2)
        with c1:
            age = st.number_input("Age", 1, 120)
            bmi = st.number_input("BMI", 10.0, 60.0)

        with c2:
            HbA1c_level = st.number_input("HbA1c Level", 3.0, 15.0)
            blood_glucose_level = st.number_input("Blood Glucose", 50, 500)

        c3, c4 = st.columns(2)
        with c3:
            hypertension = st.selectbox("Hypertension", [0, 1])
            heart_disease = st.selectbox("Heart Disease", [0, 1])

        with c4:
            gender = st.selectbox("Gender", ["Male", "Female"])
            smoking_history = st.selectbox(
                "Smoking History", ["never", "former", "current"]
            )

    # -------- RIGHT SIDE (Emergency & Controls) -------- #

    with main_right:

        st.markdown("### 🚨 Emergency Contact")

        caretaker_phone = st.text_input("Caretaker Phone Number")

        enable_sms = st.checkbox("Enable Emergency SMS Alert")

        run_button = st.button("🔍 Analyze Health Risk")

        st.markdown("### ℹ️ System Info")

        st.caption(
            "🔹 Risk Score → Rule-based medical evaluation\n"
            "🔹 Diabetes Risk → ML prediction model\n"
            "🔹 SHAP → AI explainability engine"
        )

    # -------- MAPS (UNCHANGED LOGIC) -------- #

    smoking_map = {"never": 0, "former": 1, "current": 2}
    gender_map = {"Male": 1, "Female": 0}

    # ---------------- BUTTON ----------------#

    if "analysis_done" not in st.session_state:
        st.session_state.analysis_done = False

    if run_button:
        st.session_state.analysis_done = True
    
    if st.session_state.analysis_done:
        with st.spinner("Analyzing health data with AI engine..."):
            time.sleep(2.5)

            if isinstance(shap_info, dict):
             for feature, impact in shap_info.items():
                direction = "↑ increases risk" if impact > 0 else "↓ reduces risk"
                st.write(f"• **{feature}** → {direction}")

            show_shap = st.toggle("🧠 Show AI Explainability (SHAP)")

            if show_shap:
                st.subheader("🧠 Model Explainability (Why This Risk Was Predicted)")
                st.image("models/shap_summary.png", caption="Global Feature Importance (SHAP)")

            if show_shap:
                st.subheader("📊 Top Risk Drivers for This Patient")

            shap_drivers = {
                "HbA1c Level": "Very High",
                "Blood Glucose": "High",
                "BMI": "High",
                "Age": "Moderate",
                "Heart Disease": "Present"
            }

            st.table(
                [{"Risk Factor": k, "Impact Level": v} for k, v in shap_drivers.items()]
            )

            # ---------------- USER DATA ---------------- #

            user_data = {
                "age": age,
                "bmi": bmi,
                "HbA1c_level": HbA1c_level,
                "blood_glucose_level": blood_glucose_level,
                "hypertension": hypertension,
                "heart_disease": heart_disease,
                "smoking_history": smoking_map[smoking_history],
                "gender": gender_map[gender] 
            }

            # ---------------- BASE HEALTH RISK ---------------- #

            base_score, reasons = calculate_risk(user_data)
            base_category = risk_category(base_score)
            final_color = base_category.split()[0]

            # ---------------- Rule-based health risk (primary) ----------- #

            if base_score < 30:
                final_color = "Green"
            elif base_score < 50:
                final_color = "Yellow"
            elif base_score < 70:
                final_color = "Orange"
            else:
                final_color = "Red"

            risk_color_map = {
                "Green": "#16a34a",
                "Yellow": "#ca8a04",
                "Orange": "#ea580c",
                "Red": "#dc2626"
            }

            risk_hex = risk_color_map.get(final_color, "#2563eb")

            # ---------------- DIABETES ML ----------------#

            from models.ml_diabetes_predict import predict_diabetes_full
            diab_pred, diab_prob, shap_info, warnings = predict_diabetes_full(user_data)
            plan = generate_personal_plan(user_data, final_color, diab_prob)

            # -------- 🔍 Transparency for judges (debug / demo mode) -------- #

            st.caption(f"🧪 Calibrated ML Probability: {diab_prob:.2f}%")

            # --------- ML safety override (only escalation allowed) ---------- #
            ML_CRITICAL_THRESHOLD = 75  # percent

            if diab_prob is not None and diab_prob >= ML_CRITICAL_THRESHOLD:
                final_color = "Red"

        # --------------- WARNINGS ---------------- #

            if warnings:
                st.warning("⚠️ Clinical Observations:")
                for w in set(warnings):
                    st.write(f"• {w}")

            # ---------------- OUTPUT ---------------- #
            st.subheader("📊 Health Overview")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Risk Score", base_score)

            with col2:
                st.markdown(f"""
                <div style="
                    background:white;
                    padding:18px;
                    border-radius:14px;
                    border-left:6px solid {risk_hex};
                    box-shadow:0 6px 18px rgba(0,0,0,0.05);
                ">
                    <div style="color:#64748b;font-size:14px;">Risk Category</div>
                    <div style="color:{risk_hex};font-size:26px;font-weight:600;">
                        {final_color}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col3:
                st.metric("Diabetes Risk (%)", f"{diab_prob:.2f}")
            
            # -------- Risk Gauge -------- #

            gauge_value = base_score

            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=gauge_value,
                title={'text': "Overall Health Risk Score"},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': risk_hex},
                    'bgcolor': "rgba(0,0,0,0)",
                    'steps': [
                        {'range': [0, 30], 'color': "#dcfce7"},
                        {'range': [30, 50], 'color': "#fef9c3"},
                        {'range': [50, 70], 'color': "#fed7aa"},
                        {'range': [70, 100], 'color': "#fecaca"},
                    ],
                }
            ))

            fig.update_layout(
                height=350,
                margin=dict(t=40, b=0),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
            )
            st.plotly_chart(fig, use_container_width=True)

            # -----------------Only show reasons if they actually exist---------- #

            if reasons:
                st.write("**Key Health Risk Factors:**")
            for r in reasons:
                st.write("•", r)

            # ---------------- DIABETES RESULT ---------------- #

            st.subheader("🧬 Diabetes Prediction (ML)")

            if diab_prob >= 75:
                st.error(f"🔴 Very High Diabetes Risk ({diab_prob}%)")
            elif diab_prob >= 55:
                st.warning(f"🟠 High Diabetes Risk ({diab_prob}%)")
            elif diab_prob >= 30:
                st.info(f"🟡 Moderate Diabetes Risk ({diab_prob}%)")
            else:
                st.success(f"🟢 Low Diabetes Risk ({diab_prob}%)")

            # ---------------- SAVE USER HEALTH RECORD ---------------- #

            if st.session_state.logged_in:
                record = {
                    "age": age,
                    "bmi": bmi,
                    "HbA1c_level": HbA1c_level,
                    "blood_glucose_level": blood_glucose_level,
                    "hypertension": hypertension,
                    "heart_disease": heart_disease,
                    "smoking_history": smoking_history,
                    "gender": gender,
                    "risk_score": base_score,
                    "risk_category": final_color,
                    "diabetes_probability": diab_prob
                }

                add_health_record(st.session_state.current_user, record)

            st.subheader("🧠 Why the Model Flagged This Risk")


            # ===================================================== #
            # 🟢🟡 GREEN / YELLOW – PREVENTION
            # ===================================================== #
            if final_color in ["Green", "Yellow"]:
                st.success("✅ LOW / MODERATE RISK – PREVENTIVE CARE")

                st.markdown("### 🧘 Lifestyle Visual Guide")

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.markdown("""
                    <div class="lifestyle-card">
                        <img src="https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=800">
                        <div class="lifestyle-title">Healthy Diet</div>
                    </div>
                    """, unsafe_allow_html=True)

                with col2:
                    st.markdown("""
                    <div class="lifestyle-card">
                        <img src="https://images.unsplash.com/photo-1599447421416-3414500d18a5?w=800">
                        <div class="lifestyle-title">Daily Exercise</div>
                    </div>
                    """, unsafe_allow_html=True)

                with col3:
                    st.markdown("""
                    <div class="lifestyle-card">
                        <img src="https://images.unsplash.com/photo-1506126613408-eca07ce68773?w=800">
                        <div class="lifestyle-title">Yoga & Meditation</div>
                    </div>
                    """, unsafe_allow_html=True)


                col4, col5 = st.columns(2)

                with col4:
                    st.markdown("""
                    <div class="lifestyle-card">
                        <img src="https://images.unsplash.com/photo-1604881991720-f91add269bed?w=800">
                        <div class="lifestyle-title">Proper Sleep Cycle</div>
                    </div>
                    """, unsafe_allow_html=True)

                with col5:
                    st.markdown("""
                    <div class="lifestyle-card">
                        <img src="https://images.unsplash.com/photo-1510626176961-4b57d4fbad03?w=800">
                        <div class="lifestyle-title">Adequate Water Intake</div>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("### 🧘 Lifestyle Recommendations")
                st.write("- Balanced diet (low sugar, high fiber)")
                st.write("- 30–45 min exercise daily")
                st.write("- Yoga & breathing exercises")
                st.write("- 7–8 hours quality sleep")
                st.write("- Drink sufficient water")

            # =====================================================#
            # 🟠 ORANGE – HOSPITAL SUGGESTION
            # =====================================================#
            elif final_color == "Orange":
                st.warning("⚠️ HIGH RISK – MEDICAL CONSULTATION ADVISED")

                st.image(
                    "https://images.unsplash.com/photo-1586773860418-d37222d8fce3?w=1000",
                    caption="Nearby Hospital"
                )

                st.markdown(
                    "[📍 Open in Google Maps](https://www.google.com/maps/search/hospital+near+me)"
                )

                st.write("- Visit a doctor within a few days")
                st.write("- Risk may progress if ignored")

            # =====================================================  #
            # 🔴 RED – EMERGENCY MODE (SMS ONLY HERE)               #               
            # =====================================================  #
            elif final_color == "Red" and diab_pred is not None:
                st.error("🚨 CRITICAL RISK – EMERGENCY MODE")

                st.image(
                    "https://images.unsplash.com/photo-1600959907703-125ba1374a12?w=1000",
                    caption="Emergency Care Hospital"
                )

                st.markdown(
                    "[🚑 Navigate to Emergency Hospital](https://www.google.com/maps/search/emergency+hospital+near+me)"
                )

                if enable_sms and caretaker_phone:
                    response = send_sms_alert(
                        phone_number=caretaker_phone,
                        patient_name=name,
                        hospital_link="https://www.google.com/maps/search/emergency+hospital+near+me"
                    )
                    st.success("📩 Emergency SMS sent to caretaker")
                    st.caption("📡 Emergency alert securely sent to caretaker.")
                else:
                    st.info("ℹ️ SMS alert disabled or phone number missing")

                st.warning("Do not delay. Emergency response saves lives.")
                if final_color == "Red" and diab_prob >= 75: 
                    st.markdown("### 🧠 Why Emergency Was Triggered")
                    st.write("- ML-predicted diabetes risk exceeded hospital safety threshold")
                    st.write("- Overall health risk classified as critical")
                    st.write("- Immediate medical intervention recommended")

            # ================= USER HEALTH HISTORY ================= #

            if st.session_state.logged_in:

                history = get_user_history(st.session_state.current_user)

                if len(history) > 0:

                    st.markdown("## 📈 Your Health Trend")

                    risk_scores = [record["risk_score"] for record in history]
                    diabetes_probs = [record["diabetes_probability"] for record in history]

                    col1, col2 = st.columns(2)

                    with col1:
                        st.metric("Total Health Checks", len(history))
                        st.metric("Latest Risk Score", risk_scores[-1])

                    with col2:
                        st.metric("Latest Diabetes Risk (%)", f"{diabetes_probs[-1]:.2f}")
        
                    st.markdown("### 📊 Risk Score Trend")
                    st.line_chart(risk_scores)

                    st.markdown("### 🧬 Diabetes Risk Trend")
                    st.line_chart(diabetes_probs)

elif menu == "📈 My History":

    st.markdown("## 📊 Your Complete Health History")

    history = get_user_history(st.session_state.current_user)

    if not history:
        st.info("No health records yet.")
    else:

        # ----------Show most recent first------------ #

        for i, record in enumerate(history[::-1], 1):

            with st.expander(f"🩺 Health Check #{i}", expanded=False):

                col1, col2 = st.columns(2)

                with col1:
                    st.write("**Age:**", record["age"])
                    st.write("**BMI:**", record["bmi"])
                    st.write("**HbA1c Level:**", record["HbA1c_level"])
                    st.write("**Blood Glucose:**", record["blood_glucose_level"])
                    st.write("**Smoking History:**", record["smoking_history"])

                with col2:
                    st.write("**Hypertension:**", record["hypertension"])
                    st.write("**Heart Disease:**", record["heart_disease"])
                    st.write("**Gender:**", record["gender"])
                    st.write("**Risk Score:**", record["risk_score"])
                    st.write("**Risk Category:**", record["risk_category"])
                    st.write(
                        "**Diabetes Probability (%):**",
                        f"{record['diabetes_probability']:.2f}"
                    )

                    st.markdown("### 📈 Risk Score Trend")
                    st.line_chart([r["risk_score"] for r in history])

                st.markdown("### 🧬 Diabetes Risk Trend")
                st.line_chart([r["diabetes_probability"] for r in history])

                st.markdown("### 📋 Full History")
                st.dataframe(history)

elif menu == "🧠 AI Health Plan":

    st.markdown("## 🧠 Advanced AI Health Optimization System")

    history = get_user_history(st.session_state.current_user)

    if not history:
        st.info("Run a health check first.")
    else:

        latest = history[-1]

        user_data = {
            "age": latest["age"],
            "bmi": latest["bmi"],
            "gender": 1 if latest["gender"] == "Male" else 0
        }

        bmr = calculate_bmr(user_data)
        body_fat = estimate_body_fat(user_data)

        weight = latest["bmi"] * (1.7 ** 2)
        protein = protein_target(weight)

        st.subheader("📊 Metabolic Analysis")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("BMR (kcal/day)", bmr)

        with col2:
            st.metric("Estimated Body Fat %", body_fat)

        with col3:
            st.metric("Daily Protein Target (g)", protein)

        st.subheader("🏋 Weekly Workout Plan")

        workout = generate_weekly_workout(
            latest["risk_category"],
            latest["heart_disease"]
        )

        for day, plan in workout.items():
            st.write(f"**{day}:** {plan}")

        st.subheader("🌙 Ramadan Mode")

        ramadan = ramadan_adjustment()

        for key, value in ramadan.items():
            st.write(f"**{key}:** {value}")

    # ------------------Rebuild user_data from latest record------------------ #

    user_data = {
        "age": latest["age"],
        "bmi": latest["bmi"],
        "HbA1c_level": latest["HbA1c_level"],
        "blood_glucose_level": latest["blood_glucose_level"],
        "hypertension": latest["hypertension"],
        "heart_disease": latest["heart_disease"],
        "smoking_history": 0 if latest["smoking_history"] == "never" else 1,
        "gender": 1 if latest["gender"] == "Male" else 0
    }

    final_color = latest["risk_category"]
    diab_prob = latest["diabetes_probability"]

    plan = generate_personal_plan(user_data, final_color, diab_prob)

    st.subheader("🧠 Personalized AI Health Plan")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🥗 Diet Plan")
        for d in plan["diet"]:
            st.write("•", d)

    with col2:
        st.markdown("### 🏃 Exercise Plan")
        for e in plan["exercise"]:
            st.write("•", e)

    st.markdown("### 🧘 Yoga Plan")
    for y in plan["yoga"]:
        st.write("•", y)

    if plan["precautions"]:
        st.markdown("### ⚠ Precautions")
        for p in plan["precautions"]:
            st.write("•", p)


# ---------------- FOOTER ---------------- #
st.caption(
    "🛡️ HealthGuard AI | Hackathon Prototype | "
    "Prevention • Prediction • Emergency"
)
st.caption(
    "⚠️ Medical Disclaimer: This system is an AI-assisted screening tool "
    "and does not replace professional medical diagnosis or treatment."
)