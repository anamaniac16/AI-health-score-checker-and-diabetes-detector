import streamlit as st

# ================== SESSION STATE ==================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_profile" not in st.session_state:
    st.session_state.user_profile = {}

if "page" not in st.session_state:
    st.session_state.page = "login"

# ================== SHAP TOGGLE STATE ==================
if "show_shap" not in st.session_state:
    st.session_state.show_shap = False

# ================== SHAP SAFE STATE ==================
if "shap_info" not in st.session_state:
    st.session_state.shap_info = None

if "show_shap" not in st.session_state:
    st.session_state.show_shap = False

# ================== SAFE DEFAULT ML OUTPUTS ==================
shap_info = None
warnings = None
diab_pred = None
diab_prob = None

# ================== VALUE MAPS ==================
smoking_map = {"never": 0, "former": 1, "current": 2}
gender_map = {"Male": 1, "Female": 0}

# ================== IMPORT MODULES ==================
from risk_engine import calculate_risk
from models.ml_diabetes_predict import predict_diabetes_full
from sms_service import send_sms_alert

# ================== PAGE CONFIG ==================
st.set_page_config(
    page_title="HealthGuard AI",
    page_icon="🛡️",
    layout="wide"
)

st.markdown("""
<style>
/* ================== RISK CIRCLE ================== */
.risk-circle-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 10px;
}

.risk-circle {
    width: 140px;
    height: 140px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    font-weight: 800;
    font-size: 16px;
    letter-spacing: 1px;
    box-shadow: inset 0 0 0 10px rgba(255,255,255,0.08),
                0 20px 40px rgba(0,0,0,0.45);
    animation: pulse 2.5s infinite ease-in-out;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
/* ===== COLOR STATES ===== */
.risk-green {
    background: radial-gradient(circle at top, #22c55e, #14532d);
    color: #ecfdf5;
}

.risk-yellow {
    background: radial-gradient(circle at top, #facc15, #92400e);
    color: #fffbeb;
}

.risk-orange {
    background: radial-gradient(circle at top, #fb923c, #9a3412);
    color: #fff7ed;
}

.risk-red {
    background: radial-gradient(circle at top, #ef4444, #7f1d1d);
    color: #fee2e2;
}

/* ===== SOFT PULSE ===== */
@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.05); }
    100% { transform: scale(1); }
}
</style>
""", unsafe_allow_html=True)

# ================== GLOBAL STYLING ==================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b, #312e81);
    color: #e5e7eb;
    font-family: 'Inter', 'Segoe UI', sans-serif;
}

h1, h2, h3 {
    color: #e0e7ff;
    font-weight: 700;
}

div[data-testid="stVerticalBlock"] > div {
    background: rgba(255,255,255,0.06);
    border-radius: 16px;
    padding: 18px;
    margin-bottom: 18px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.35);
    backdrop-filter: blur(10px);
    transition: all 0.3s ease;
}

div[data-testid="stVerticalBlock"] > div:hover {
    transform: translateY(-6px);
    box-shadow: 0 20px 40px rgba(37,99,235,0.3);
}

.stButton > button {
    background: linear-gradient(135deg, #2563eb, #db2777);
    color: white;
    border-radius: 12px;
    border: none;
    padding: 10px 22px;
    font-weight: 600;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 25px rgba(219,39,119,0.45);
}
</style>
""", unsafe_allow_html=True)

# ================== HEADER ==================
st.markdown("""
<div style="
    background: linear-gradient(135deg, #1e293b, #312e81);
    border-radius: 20px;
    padding: 36px;
    text-align: center;
    box-shadow: 0 20px 40px rgba(0,0,0,0.4);
">
    <h1>🛡️ HealthGuard AI</h1>
    <p style="color:#c7d2fe;">
        Smart Health Risk Detection & Diabetes Prediction System
    </p>
</div>
""", unsafe_allow_html=True)

st.info(
    "HealthGuard AI focuses on prevention, early intervention, "
    "and emergency response, enhanced with ML-based diabetes prediction."
)

st.success("🏥 Hospital-Grade Screening Mode Enabled")
# ================== LOGIN PAGE ==================
if st.session_state.page == "login":
    st.subheader("🔐 User Login & Profile Setup")

    with st.form("login_form"):
        login_name = st.text_input("Full Name")
        login_age = st.number_input("Age", 1, 120)
        login_gender = st.selectbox("Gender", ["Male", "Female"])
        login_phone = st.text_input("Emergency Caretaker Number")
        login_smoking = st.selectbox(
            "Smoking History", ["never", "former", "current"]
        )
        login_hypertension = st.selectbox("Hypertension", [0, 1])

        submit_login = st.form_submit_button("Login & Save Profile")

        if submit_login:
            st.session_state.user_profile = {
                "name": login_name,
                "age": login_age,
                "gender": login_gender,
                "caretaker_phone": login_phone,
                "smoking_history": login_smoking,
                "hypertension": login_hypertension,
            }
            st.session_state.logged_in = True
            st.session_state.page = "dashboard"
            st.rerun()

# ================== SIDEBAR ==================
if st.session_state.logged_in:
    with st.sidebar:
        st.markdown("### 👤 Logged in as")
        st.markdown(
            f"<b>{st.session_state.user_profile.get('name','')}</b>",
            unsafe_allow_html=True,
        )

        st.markdown("---")

        if st.button("🔁 Retake Health Test"):
            st.session_state.shap_info = None
            st.session_state.show_shap = False
            st.session_state.page = "dashboard"
            st.rerun()

        if st.button("✏️ Edit Profile"):
            st.session_state.page = "edit_profile"
            st.rerun()

        if st.button("➕ Add New User"):
            st.session_state.logged_in = False
            st.session_state.user_profile = {}
            st.session_state.page = "login"
            st.rerun()

        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.page = "login"
            st.rerun()
            # ================== EDIT PROFILE PAGE ==================
if st.session_state.page == "edit_profile":
    st.subheader("✏️ Edit Profile Information")

    with st.form("edit_profile_form"):
        name = st.text_input(
            "Full Name",
            value=st.session_state.user_profile.get("name", "")
        )
        age = st.number_input(
            "Age", 1, 120,
            value=st.session_state.user_profile.get("age", 25)
        )
        gender = st.selectbox(
            "Gender",
            ["Male", "Female"],
            index=0 if st.session_state.user_profile.get("gender") == "Male" else 1
        )
        caretaker = st.text_input(
            "Emergency Caretaker Number",
            value=st.session_state.user_profile.get("caretaker_phone", "")
        )

        save_profile = st.form_submit_button("💾 Save Changes")

        if save_profile:
            st.session_state.user_profile.update({
                "name": name,
                "age": age,
                "gender": gender,
                "caretaker_phone": caretaker,
            })
            st.session_state.page = "dashboard"
            st.rerun()

# ================== DASHBOARD ==================
if st.session_state.page == "dashboard" and st.session_state.logged_in:
    st.subheader("🩺 Health Assessment")

    col1, col2 = st.columns(2)

    with col1:
        bmi = st.number_input("BMI", 10.0, 60.0)
        HbA1c_level = st.number_input("HbA1c Level", 3.0, 15.0)
        hypertension = st.selectbox(
            "Hypertension", [0, 1],
            index=st.session_state.user_profile.get("hypertension", 0)
        )

    with col2:
        blood_glucose_level = st.number_input("Blood Glucose Level", 50, 500)
        heart_disease = st.selectbox("Heart Disease", [0, 1])
        smoking_history = st.selectbox(
            "Smoking History",
            ["never", "former", "current"],
            index=["never", "former", "current"].index(
                st.session_state.user_profile.get("smoking_history", "never")
            )
        )

    enable_sms = st.checkbox("Enable Emergency SMS Alert (Demo Mode)")
    # ================== RUN HEALTH RISK ==================
if st.button("🔍 Check Health Risk"):
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
    st.session_state.last_run = True 
    # ---------- USER DATA (SINGLE SOURCE OF TRUTH) ----------
    user_data = {
        "age": st.session_state.user_profile["age"],
        "bmi": bmi,
        "HbA1c_level": HbA1c_level,
        "blood_glucose_level": blood_glucose_level,
        "hypertension": hypertension,
        "heart_disease": heart_disease,
        "smoking_history": smoking_map[smoking_history],
        "gender": gender_map[st.session_state.user_profile["gender"]],
    }

    # ---------- BASE RISK ----------
base_score, reasons = calculate_risk(user_data)

if base_score < 30:
        final_color = "Green"
elif base_score < 50:
        final_color = "Yellow"
elif base_score < 70:
        final_color = "Orange"
else:
        final_color = "Red"

    # ---------- DIABETES ML ----------
        diab_pred, diab_prob, shap_info, warnings = predict_diabetes_full(user_data)

    # ---------- PERSIST SHAP SAFELY ----------
if shap_info is not None and isinstance(shap_info, dict) and len(shap_info) > 0:
        st.session_state.shap_info = shap_info
else:
        st.session_state.shap_info = None

    # ---------- ML SAFETY OVERRIDE ----------
if diab_prob is not None and diab_prob >= 75:
        final_color = "Red"
        base_score = base_score if "base_score" in locals() else 0
        final_color = final_color if "final_color" in locals() else "Green"
        reasons = reasons if "reasons" in locals() else []

# ================== RISK SUMMARY ==================
st.markdown("---")
st.subheader("📊 Health Risk Summary")

colA, colB = st.columns(2)
with colA:
    st.metric("Risk Score", base_score)
with colB:
    pass
    # ---------- COLOR CIRCLE ----------
risk_class_map = {
    "Green": ("risk-green", "LOW RISK"),
    "Yellow": ("risk-yellow", "MODERATE RISK"),
    "Orange": ("risk-orange", "HIGH RISK"),
    "Red": ("risk-red", "CRITICAL"),
}

css_class, label = risk_class_map.get(
    final_color, ("risk-green", "UNKNOWN")
)

st.markdown(
    f"""
    <div class="risk-circle-wrapper">
        <div class="risk-circle {css_class}">
            {label}
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- REASONS ----------
if reasons:
    st.markdown("### 🧾 Key Health Risk Factors")
    for r in reasons:
        st.write("•", r)

# ================== DIABETES RESULT ==================
st.markdown("---")
st.subheader("🧬 Diabetes Prediction")

if diab_prob is not None:
    if diab_prob >= 75:
        st.error(f"🔴 Very High Diabetes Risk ({diab_prob:.2f}%)")
    elif diab_prob >= 55:
        st.warning(f"🟠 High Diabetes Risk ({diab_prob:.2f}%)")
    elif diab_prob >= 30:
        st.info(f"🟡 Moderate Diabetes Risk ({diab_prob:.2f}%)")
    else:
        st.success(f"🟢 Low Diabetes Risk ({diab_prob:.2f}%)")

# ================== WARNINGS ==================
if warnings:
    st.warning("⚠️ Clinical Observations")
    for w in set(warnings):
        st.write("•", w)
        # ================== AI EXPLAINABILITY (SHAP) ==================
if st.session_state.shap_info:
    st.markdown("---")
    st.subheader("🧠 Why the AI Flagged This Risk")

    for feature, impact in st.session_state.shap_info.items():
        direction = "↑ increases risk" if impact > 0 else "↓ reduces risk"
        st.write(f"• **{feature}** → {direction}")

    # ✅ KEEP THIS TOGGLE
    st.session_state.show_shap = st.toggle(
        "🧠 Show AI Explainability (SHAP)",
        value=st.session_state.show_shap,
    )

    if st.session_state.show_shap:
        st.image(
            "models/shap_summary.png",
            caption="Global Feature Importance (SHAP)",
        )
# Persistent toggle
st.session_state.show_shap = st.toggle(
    "🧠 Show AI Explainability (SHAP)",
    value=st.session_state.show_shap,
)

if st.session_state.show_shap:
    st.image(
        "models/shap_summary.png",
        caption="Global Feature Importance (SHAP)",
    )

st.markdown("---")
st.subheader("🧠 Why the Model Flagged This Risk")

if shap_info:
    for feature, impact in shap_info.items():
        direction = "↑ increases risk" if impact > 0 else "↓ reduces risk"
        st.write(f"• **{feature}** → {direction}")
    # ---------- PERSISTENT TOGGLE ----------
st.session_state.show_shap = st.toggle(
    "🧠 Show AI Explainability (SHAP)",
    value=st.session_state.show_shap,
)

if st.session_state.show_shap:
    st.image(
        "models/shap_summary.png",
        caption="Global Feature Importance (SHAP)",
    )

# =====================================================
# 🟢🟡 GREEN / YELLOW — PREVENTION MODE
# =====================================================
if final_color in ["Green", "Yellow"]:
    st.markdown("---")
    st.success("✅ LOW / MODERATE RISK — PREVENTIVE CARE")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.image(
            "https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=800",
            caption="Healthy Diet",
        )
    with c2:
        st.image(
            "https://images.unsplash.com/photo-1594737625785-c2b1c2c6e6c8?w=800",
            caption="Daily Exercise",
        )
    with c3:
        st.image(
            "https://images.unsplash.com/photo-1599447421416-3414500d18a5?w=800",
            caption="Yoga & Meditation",
        )

    c4, c5 = st.columns(2)
    with c4:
        st.image(
            "https://images.unsplash.com/photo-1506126613408-eca07ce68773?w=800",
            caption="Proper Sleep Cycle",
        )
    with c5:
        st.image(
            "https://images.unsplash.com/photo-1510626176961-4b57d4fbad03?w=800",
            caption="Adequate Water Intake",
        )

    st.markdown("### 🧘 Lifestyle Recommendations")
    st.write("- Balanced diet (low sugar, high fiber)")
    st.write("- 30–45 minutes of exercise daily")
    st.write("- Yoga & breathing exercises")
    st.write("- 7–8 hours of quality sleep")
    st.write("- Drink sufficient water")
    # =====================================================
# 🟠 ORANGE — MEDICAL ATTENTION
# =====================================================
elif final_color == "Orange":
    st.markdown("---")
    st.warning("⚠️ HIGH RISK — MEDICAL CONSULTATION ADVISED")

    st.image(
        "https://images.unsplash.com/photo-1586773860418-d37222d8fce3?w=1000",
        caption="Consult a Doctor",
    )

    st.markdown(
        "[📍 Find Nearby Hospital](https://www.google.com/maps/search/hospital+near+me)"
    )

    st.write("- Schedule a doctor visit soon")
    st.write("- Risk may progress if ignored")

# =====================================================
# 🔴 RED — EMERGENCY MODE
# =====================================================
elif final_color == "Red":
    st.markdown("---")
    st.error("🚨 CRITICAL RISK — EMERGENCY MODE")

    st.image(
        "https://images.unsplash.com/photo-1600959907703-125ba1374a12?w=1000",
        caption="Emergency Medical Care",
    )

    st.markdown(
        "[🚑 Navigate to Emergency Hospital](https://www.google.com/maps/search/emergency+hospital+near+me)"
    )

    if enable_sms:
        send_sms_alert(
            phone_number=st.session_state.user_profile["caretaker_phone"],
            patient_name=st.session_state.user_profile["name"],
            hospital_link="https://www.google.com/maps/search/emergency+hospital+near+me",
        )

        st.success("📩 Emergency SMS sent to caretaker")

    st.warning(
        "Do not delay. Immediate medical attention is critical."
    )
    # ================== STATE CLEANUP ==================
# This prevents old risk results from sticking
# when user clicks "Retake Health Test"
if st.session_state.page == "dashboard":
    if "last_run" not in st.session_state:
        st.session_state.last_run = False

# Clear old outputs when user revisits dashboard
if not st.session_state.last_run:
    for key in [
        "base_score",
        "final_color",
        "reasons",
        "diab_pred",
        "diab_prob",
        "shap_info",
        "warnings",
    ]:
        if key in st.session_state:
            st.session_state[key] = None

# ================== RETAKE BUTTON LOGIC ==================
# This ensures re-run without losing UI or images
if st.session_state.logged_in:
    with st.sidebar:
        st.markdown("---")

        if st.button("🔄 Retake Health Risk"):
            st.session_state.show_shap = False
            st.session_state.last_run = False
            st.session_state.page = "dashboard"
            st.rerun()

# ================== SAFE DEFAULT VISUAL ==================
# Shows hint before user clicks "Check Health Risk"
if st.session_state.page == "dashboard" and not st.session_state.last_run:
    st.info(
        "🩺 Enter your medical values and click **Check Health Risk** "
        "to view your health status, lifestyle guidance, and emergency alerts."
    )

# ================== FOOTER ==================
st.markdown("---")
st.caption(
    "🛡️ HealthGuard AI | Hackathon Prototype | "
    "Prevention • Prediction • Emergency"
)
st.caption(
    "⚠️ Medical Disclaimer: This system is an AI-assisted screening tool "
    "and does not replace professional medical diagnosis or treatment."
)
# ================== SCORE HISTORY ==================
# Store past risk results for analytics
if "history" not in st.session_state:
    st.session_state.history = []

# Save results AFTER a successful run
if (
    st.session_state.page == "dashboard"
    and st.session_state.last_run
    and base_score is not None
):
    st.session_state.history.append(
        {
            "score": base_score,
            "risk": final_color,
            "diabetes_prob": diab_prob,
        }
    )

# ================== ANALYTICS PANEL ==================
if st.session_state.page == "dashboard" and st.session_state.history:
    st.markdown("---")
    st.subheader("📈 Health Risk Analytics")

    scores = [h["score"] for h in st.session_state.history]
    risks = [h["risk"] for h in st.session_state.history]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Checks", len(scores))
    with col2:
        st.metric("Latest Risk Score", scores[-1])
    with col3:
        st.metric(
            "Worst Risk Level",
            max(
                risks,
                key=lambda x: ["Green", "Yellow", "Orange", "Red"].index(x),
            ),
        )

# ================== BAR CHART ==================
st.markdown("### 📊 Risk Score Trend")
st.bar_chart(scores, height=220, use_container_width=True)

# ================== DIABETES PROBABILITY TREND ==================
if any(h["diabetes_prob"] is not None for h in st.session_state.history):
    st.markdown("### 🧬 Diabetes Risk Trend")

    diab_values = [
        h["diabetes_prob"]
        for h in st.session_state.history
        if h["diabetes_prob"] is not None
    ]

    st.line_chart(diab_values, height=220, use_container_width=True)

# ================== CLEAR HISTORY OPTION ==================
if st.session_state.logged_in:
    with st.sidebar:
        if st.button("🧹 Clear Health History"):
            st.session_state.history = []
            st.success("Health history cleared.")
            st.rerun()