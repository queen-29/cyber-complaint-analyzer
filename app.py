import streamlit as st
import re
# Store past data
if "history" not in st.session_state:
    st.session_state.history = []

st.title("Cyber Complaint Analysis System")

complaint = st.text_area("Enter Cyber Complaint")

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

    # Basic Hinglish normalization
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


if st.button("Analyze Complaint"):
    if complaint:
        category = classify(complaint)
        entities = extract_entities(complaint)

        # Store complaint
        st.session_state.history.append(entities)

        st.subheader("Category:")
        st.write(category)

        st.subheader("Extracted Entities:")
        for key, value in entities.items():
            st.write(f"{key}: {value}")

        # 🔍 Repeat Detection
        st.subheader("⚠️ Repeat Detection:")

        for key in ["Phone Numbers", "Emails", "UPI IDs"]:
            all_values = []

            for item in st.session_state.history:
                all_values.extend(item[key])

            for val in set(all_values):
                count = all_values.count(val)
                if count > 1:
                    st.warning(f"{key[:-1]} {val} found in {count} complaints")
    else:
        st.warning("Please enter a complaint")
   
