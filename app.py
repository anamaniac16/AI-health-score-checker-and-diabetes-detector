import streamlit as st

# ---------------- IMPORT MODULES ----------------
from risk_engine import calculate_risk, risk_category
from models.ml_diabetes_predict import predict_diabetes
from sms_service import send_sms_alert

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="HealthGuard AI",
    page_icon="🛡️",
    layout="wide"
)

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

# ---------------- USER INPUT ----------------
st.subheader("👤 Patient Information")

col1, col2 = st.columns(2)

with col1:
    name = st.text_input("Patient Name")
    age = st.number_input("Age", 1, 120)
    bmi = st.number_input("BMI", 10.0, 60.0)
    hypertension = st.selectbox("Hypertension", [0, 1])

with col2:
    HbA1c_level = st.number_input("HbA1c Level", 3.0, 15.0)
    blood_glucose_level = st.number_input("Blood Glucose Level", 50, 500)
    heart_disease = st.selectbox("Heart Disease", [0, 1])

smoking_history = st.selectbox("Smoking History", ["never", "former", "current"])

st.subheader("👨‍👩‍👧 Caretaker Contact (Emergency Only)")
caretaker_phone = st.text_input("Caretaker Phone Number")

enable_sms = st.checkbox("Enable Emergency SMS Alert (Demo Mode)")

smoking_map = {"never": 0, "former": 1, "current": 2}

# ---------------- BUTTON ----------------
if st.button("🔍 Check Health Risk"):

    # ---------------- USER DATA ----------------
    user_data = {
        "age": age,
        "bmi": bmi,
        "HbA1c_level": HbA1c_level,
        "blood_glucose_level": blood_glucose_level,
        "hypertension": hypertension,
        "heart_disease": heart_disease,
        "smoking_history": smoking_map[smoking_history]
    }

    # ---------------- BASE HEALTH RISK ----------------
    base_score, reasons = calculate_risk(user_data)
    base_category = risk_category(base_score)
    base_color = base_category.split()[0]

    # ---------------- DIABETES ML ----------------
    diab_pred, diab_prob = predict_diabetes(user_data)

    if diab_pred == 1:
        diabetes_risk = "Red"
    elif diab_prob >= 60:
        diabetes_risk = "Orange"
    elif diab_prob >= 30:
        diabetes_risk = "Yellow"
    else:
        diabetes_risk = "Green"

    # ---------------- FINAL RISK ESCALATION ----------------
    risk_order = ["Green", "Yellow", "Orange", "Red"]
    final_color = base_color

    if risk_order.index(diabetes_risk) > risk_order.index(base_color):
        final_color = diabetes_risk

    # ---------------- OUTPUT ----------------
    st.markdown("---")
    st.subheader("📊 Health Risk Summary")

    colA, colB = st.columns(2)
    with colA:
        st.metric("Risk Score", base_score)
    with colB:
        st.metric("Final Risk Category", final_color)

    st.write("**Key Health Risk Factors:**")
    for r in reasons:
        st.write("•", r)

    # ---------------- DIABETES RESULT ----------------
    st.markdown("---")
    st.subheader("🧬 Diabetes Prediction (ML)")

    if diab_pred == 1:
        st.error(f"Diabetes Detected (Probability: {diab_prob}%)")
    else:
        st.info(f"No Diabetes Detected (Risk Probability: {diab_prob}%)")

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
                "https://images.unsplash.com/photo-1594737625785-c2b1c2c6e6c8?w=800",
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
    elif final_color == "Red":
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
            st.json(response)
        else:
            st.info("ℹ️ SMS alert disabled or phone number missing")

        st.warning("Do not delay. Emergency response saves lives.")

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption(
    "🛡️ HealthGuard AI | Hackathon Prototype | "
    "Prevention • Prediction • Emergency"
)
