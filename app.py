import streamlit as st
import re

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

    if "otp" in text or "bank" in text:
        return "Banking Fraud"
    elif "job" in text or "interview" in text:
        return "Fake Job Scam"
    elif "instagram" in text or "facebook" in text:
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

        st.subheader("Category:")
        st.write(category)

        st.subheader("Extracted Entities:")
        for key, value in entities.items():
            st.write(f"{key}: {value}")
    else:
        st.warning("Please enter a complaint")
