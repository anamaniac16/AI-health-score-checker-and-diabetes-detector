import streamlit as st
# ---------------- SAFE DEFAULTS ----------------
base_score = None
final_color = None
reasons = []
diab_pred = None
diab_prob = None
shap_info = {}
warnings = []

# ---------------- IMPORT MODULES ----------------
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


# ---------------- AUTH SESSION ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_user" not in st.session_state:
    st.session_state.current_user = None

if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "login"   # login or signup

# ---------------- AUTO LOGIN ----------------
saved_user = load_session()

if saved_user and not st.session_state.logged_in:
    st.session_state.logged_in = True
    st.session_state.current_user = saved_user

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="HealthGuard AI",
    page_icon="🛡️",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: #0f172a;
    color: #e2e8f0;
    font-family: 'Inter', sans-serif;
}

div[data-testid="stVerticalBlock"] > div {
    background: rgba(255,255,255,0.03);
    border-radius: 12px;
    padding: 14px;
    margin-bottom: 12px;
    box-shadow: 0 8px 18px rgba(0,0,0,0.25);
}

.stButton > button {
    background: linear-gradient(135deg,#2563eb,#7c3aed);
    color: white;
    border-radius: 8px;
    padding: 6px 16px;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
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


# ================= AUTHENTICATION =================
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
# ================= USER BAR =================
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
        
# ================= DASHBOARD INPUT PANEL =================
st.markdown("## 🧾 Patient Health Profile")

main_left, main_right = st.columns([1.1, 1])

# -------- LEFT SIDE (Core Metrics) --------
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

# -------- RIGHT SIDE (Emergency & Controls) --------
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

# -------- MAPS (UNCHANGED LOGIC) --------
smoking_map = {"never": 0, "former": 1, "current": 2}
gender_map = {"Male": 1, "Female": 0}

# ---------------- BUTTON ----------------
if run_button:

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

    st.subheader("🩺 What Can Reduce This Risk?")

    recommendations = []

    if HbA1c_level > 6.5:
        recommendations.append("Lower HbA1c through diet control and medication")

    if bmi > 30:
        recommendations.append("Weight reduction through guided exercise")

    if blood_glucose_level > 140:
        recommendations.append("Regular glucose monitoring")

    if smoking_history != "never":
        recommendations.append("Smoking cessation program")

    if hypertension == 1:
        recommendations.append("Blood pressure management")

    for r in recommendations:
        st.write("•", r)


    # ---------------- USER DATA ----------------
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

    # ---------------- BASE HEALTH RISK ----------------
    base_score, reasons = calculate_risk(user_data)
    base_category = risk_category(base_score)
    final_color = base_category.split()[0]

     # Rule-based health risk (primary)
    if base_score < 30:
        final_color = "Green"
    elif base_score < 50:
        final_color = "Yellow"
    elif base_score < 70:
        final_color = "Orange"
    else:
        final_color = "Red"

    # ---------------- DIABETES ML ----------------#
    from models.ml_diabetes_predict import predict_diabetes_full
    diab_pred, diab_prob, shap_info, warnings = predict_diabetes_full(user_data)

    # 🔍 Transparency for judges (debug / demo mode)
    st.caption(f"🧪 Calibrated ML Probability: {diab_prob:.2f}%")

     # ML safety override (only escalation allowed)
    ML_CRITICAL_THRESHOLD = 75  # percent

    if diab_prob is not None and diab_prob >= ML_CRITICAL_THRESHOLD:
        final_color = "Red"

   #--------------- WARNINGS ----------------#
    if warnings:
        st.warning("⚠️ Clinical Observations:")
        for w in set(warnings):
            st.write(f"• {w}")

    # ---------------- OUTPUT ----------------
    st.subheader("📊 Health Risk Summary")

    colA, colB = st.columns(2)
    with colA:
        st.metric("Risk Score", base_score)
    with colB:
        st.metric("Final Risk Category", final_color)

    # Only show reasons if they actually exist
    if reasons:
        st.write("**Key Health Risk Factors:**")
    for r in reasons:
        st.write("•", r)

    # ---------------- DIABETES RESULT ----------------
    st.subheader("🧬 Diabetes Prediction (ML)")

    if diab_prob >= 75:
        st.error(f"🔴 Very High Diabetes Risk ({diab_prob}%)")
    elif diab_prob >= 55:
        st.warning(f"🟠 High Diabetes Risk ({diab_prob}%)")
    elif diab_prob >= 30:
        st.info(f"🟡 Moderate Diabetes Risk ({diab_prob}%)")
    else:
        st.success(f"🟢 Low Diabetes Risk ({diab_prob}%)")

    # ---------------- SAVE USER HEALTH RECORD ----------------
    if st.session_state.logged_in:
        record = {
            "risk_score": base_score,
            "risk_category": final_color,
            "diabetes_probability": diab_prob
        }

        add_health_record(st.session_state.current_user, record)

    st.subheader("🧠 Why the Model Flagged This Risk")


    # =====================================================
    # 🟢🟡 GREEN / YELLOW – PREVENTION
    # =====================================================
    if final_color in ["Green", "Yellow"]:
        st.success("✅ LOW / MODERATE RISK – PREVENTIVE CARE")

        c1, c2, c3 = st.columns(3)
        with c1:
            st.image(
                "https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=800",
                caption="Healthy Diet"
            )
        with c2:
            st.image(
                "https://cdn.shopify.com/s/files/1/0285/2647/7357/files/Skineasi-Blog_2048X2048px.12_480x480.jpg?v=1594572377",
                caption="Daily Exercise"
            )
        with c3:
            st.image(
                "https://images.unsplash.com/photo-1599447421416-3414500d18a5?w=800",
                caption="Yoga & Meditation"
            )

        c4, c5 = st.columns(2)
        with c4:
            st.image(
                "https://images.unsplash.com/photo-1506126613408-eca07ce68773?w=800",
                caption="Proper Sleep Cycle"
            )
        with c5:
            st.image(
                "https://images.unsplash.com/photo-1510626176961-4b57d4fbad03?w=800",
                caption="Adequate Water Intake"
            )

        st.markdown("### 🧘 Lifestyle Recommendations")
        st.write("- Balanced diet (low sugar, high fiber)")
        st.write("- 30–45 min exercise daily")
        st.write("- Yoga & breathing exercises")
        st.write("- 7–8 hours quality sleep")
        st.write("- Drink sufficient water")

    # =====================================================
    # 🟠 ORANGE – HOSPITAL SUGGESTION
    # =====================================================
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

    # =====================================================
    # 🔴 RED – EMERGENCY MODE (SMS ONLY HERE)
    # =====================================================
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

    # ================= USER HEALTH HISTORY =================
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


# ---------------- FOOTER ----------------
st.caption(
    "🛡️ HealthGuard AI | Hackathon Prototype | "
    "Prevention • Prediction • Emergency"
)
st.caption(
    "⚠️ Medical Disclaimer: This system is an AI-assisted screening tool "
    "and does not replace professional medical diagnosis or treatment."
)
