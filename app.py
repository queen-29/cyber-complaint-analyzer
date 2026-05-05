import streamlit as st
import re

# -------- Page Config --------
st.set_page_config(
    page_title="Cyber Complaint Analyzer",
    page_icon="🚔",
    layout="wide"
)

# -------- Session Storage --------
if "history" not in st.session_state:
    st.session_state.history = []

# -------- Header --------
st.markdown("<h1 style='text-align: center;'>🚔 Cyber Complaint Analysis System</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>AI-assisted tool for analyzing cybercrime complaints</p>", unsafe_allow_html=True)
st.write("---")

# -------- Functions --------
def extract_entities(text):
    phone = re.findall(r'\b\d{10}\b', text)
    email = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', text)
    url = re.findall(r'(https?://\S+)', text)
    upi = re.findall(r'\b[\w.-]+@[\w.-]+\b', text)

    return {
        "Phone Numbers": phone,
        "Emails": email,
        "URLs": url,
        "UPI IDs": upi
    }

def classify(text):
    text = text.lower()

    # Hinglish normalization
    text = text.replace("paise", "money")
    text = text.replace("kat gaye", "deducted")
    text = text.replace("hack hogya", "hacked")
    text = text.replace("mila", "received")
    text = text.replace("fraud hua", "fraud")

    if ("otp" in text or "bank" in text or "money" in text):
        return "Banking Fraud"
    elif "job" in text or "interview" in text:
        return "Fake Job Scam"
    elif "instagram" in text or "facebook" in text or "hacked" in text:
        return "Social Media Scam"
    elif "upi" in text or "payment" in text:
        return "UPI Fraud"
    elif "link" in text or "http" in text:
        return "Phishing"
    else:
        return "Other"

# -------- Layout --------
col1, col2 = st.columns(2)

# -------- Left: Input --------
with col1:
    st.subheader("📝 Enter Complaint")
    complaint = st.text_area("Type complaint here", height=200)
    analyze_btn = st.button("Analyze Complaint")

# -------- Right: Output --------
with col2:
    if analyze_btn:
        if complaint:
            category = classify(complaint)
            entities = extract_entities(complaint)

            # Store complaint
            st.session_state.history.append(entities)

            st.subheader("📌 Category")
            st.success(category)

            st.subheader("🔍 Extracted Entities")
            for key, value in entities.items():
                st.write(f"**{key}:** {value}")

            # -------- Risk Analysis --------
            st.subheader("⚠️ Risk Analysis")

            is_high_risk = False

            for key in ["Phone Numbers", "Emails", "UPI IDs"]:
                current_values = entities[key]

                all_values = []
                for item in st.session_state.history[:-1]:
                    all_values.extend(item[key])

                for val in current_values:
                    count = all_values.count(val)
                    if count > 0:
                        is_high_risk = True
                        st.warning(f"{key[:-1]} {val} seen in {count} previous complaints")

            if is_high_risk:
                st.error("🚨 High Risk Complaint (linked to previous cases)")
            else:
                st.success("No prior records found")

        else:
            st.warning("Please enter a complaint")

# -------- Dashboard --------
st.write("---")
st.subheader("📊 System Overview")

total_cases = len(st.session_state.history)
st.write(f"Total Complaints Analyzed: {total_cases}")

all_phones = []
for item in st.session_state.history:
    all_phones.extend(item["Phone Numbers"])

if all_phones:
    most_common = max(set(all_phones), key=all_phones.count)
    st.write(f"Most Reported Phone: {most_common}")
