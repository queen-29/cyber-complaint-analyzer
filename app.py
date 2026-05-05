import streamlit as st
import re
import pandas as pd


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
    
    url = re.findall(r'(https?://[^\s]+|www\.[^\s]+|[a-zA-Z0-9-]+\.[a-zA-Z]{2,})', text)
    url = [u.strip('.,') for u in url]

    upi = re.findall(r'\b[\w.-]+@[\w.-]+\b', text)
    upi = [u for u in upi if u not in email]

    return {
        "Phone Numbers": phone,
        "Emails": email,
        "URLs": url,
        "UPI IDs": upi
    }

def classify(text):
    text = text.lower()

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

# -------- LEFT: Input --------
with col1:
    st.subheader("📝 Enter Complaint")
    complaint = st.text_area("Type complaint here", height=200)
    analyze_btn = st.button("Analyze Complaint")

    st.write("---")
    st.subheader("📂 Bulk Upload")
    uploaded_file = st.file_uploader("Upload CSV with 'complaint' column", type=["csv"])

# -------- RIGHT: Output --------
with col2:
    if analyze_btn:
        if complaint:
            category = classify(complaint)
            entities = extract_entities(complaint)

            st.session_state.history.append({
                "entities": entities,
                "category": category
            })

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
                    all_values.extend(item["entities"][key])

                for val in current_values:
                    count = all_values.count(val)
                    if count > 0:
                        is_high_risk = True
                        st.warning(f"{key[:-1]} {val} seen in {count} previous complaints")

            if is_high_risk:
                st.error("🚨 High Risk Complaint")
            else:
                st.success("No prior records found")

        else:
            st.warning("Please enter a complaint")

# -------- BULK PROCESSING --------
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    if "complaint" in df.columns:
        st.success("File uploaded successfully")

        results = []

        for text in df["complaint"]:
            category = classify(str(text))
            entities = extract_entities(str(text))

            st.session_state.history.append({
                "entities": entities,
                "category": category
            })

            results.append({
                "Complaint": text,
                "Category": category,
                "Phones": entities["Phone Numbers"],
                "Emails": entities["Emails"],
                "URLs": entities["URLs"],
                "UPIs": entities["UPI IDs"]
            })

        st.subheader("📊 Bulk Analysis Results")
        st.dataframe(results)

        # Download button
        csv = pd.DataFrame(results).to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Results",
            data=csv,
            file_name='analysis_results.csv',
            mime='text/csv'
        )

    else:
        st.error("CSV must contain 'complaint' column")

# -------- DASHBOARD --------
st.write("---")
st.subheader("📊 System Overview")

total_cases = len(st.session_state.history)
st.write(f"Total Complaints: {total_cases}")

# Most common entities
all_phones, all_emails, all_upi = [], [], []

for item in st.session_state.history:
    all_phones.extend(item["entities"]["Phone Numbers"])
    all_emails.extend(item["entities"]["Emails"])
    all_upi.extend(item["entities"]["UPI IDs"])

if all_phones:
    st.write(f"📞 Most Reported Phone: {max(set(all_phones), key=all_phones.count)}")
if all_emails:
    st.write(f"📧 Most Reported Email: {max(set(all_emails), key=all_emails.count)}")
if all_upi:
    st.write(f"💳 Most Reported UPI: {max(set(all_upi), key=all_upi.count)}")

# -------- Chart --------
st.write("---")
st.markdown("## 📊 Analytics Dashboard")

st.subheader("📊 Crime Distribution")

categories = [item["category"] for item in st.session_state.history]

if categories:
    df_chart = pd.DataFrame(categories, columns=["Category"])
    chart_data = df_chart["Category"].value_counts()

    st.bar_chart(chart_data)



# -------- Risk Summary --------
st.subheader("🚨 Risk Summary")

all_values = []
for item in st.session_state.history:
    all_values.extend(item["entities"]["Phone Numbers"])
    all_values.extend(item["entities"]["Emails"])
    all_values.extend(item["entities"]["UPI IDs"])

repeat_count = sum(1 for val in set(all_values) if all_values.count(val) > 1)

st.write(f"Repeat Entities: {repeat_count}")

if repeat_count > 0:
    st.error("Multiple repeat offenders detected")
else:
    st.success("No major repeat patterns")
