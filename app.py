import streamlit as st
import re
import pandas as pd

st.set_page_config(page_title="Cyber Complaint Analyzer", layout="wide")

# -------- Session --------
if "history" not in st.session_state:
    st.session_state.history = []

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
    categories = []

    if "otp" in text or "bank" in text or "money" in text:
        categories.append("Banking")

    if "job" in text:
        categories.append("Job Scam")

    if "instagram" in text or "facebook" in text or "hacked" in text:
        categories.append("Social Scam")

    if "upi" in text or "payment" in text:
        categories.append("UPI Fraud")

    if "http" in text or "www" in text or "link" in text:
        categories.append("Phishing")

    if not categories:
        categories.append("Other")

    return list(set(categories))  # remove duplicates safely

# -------- UI --------
st.title("🚔 Cyber Complaint Analysis System")
st.write("---")

col1, col2 = st.columns(2)

# -------- Input --------
with col1:
    complaint = st.text_area("Enter Complaint", height=200)
    analyze = st.button("Analyze")

    st.write("---")
    uploaded_file = st.file_uploader("Upload CSV (column: complaint)", type=["csv"])

# -------- Output --------
with col2:
    if analyze and complaint:
        category = classify(complaint)
        entities = extract_entities(complaint)

        st.session_state.history.append({
            "category": category,
            "entities": entities
        })

        st.subheader("Category")
        st.success(", ".join(category))

        st.subheader("Extracted Entities")
        for k, v in entities.items():
            st.write(f"{k}: {v}")

        # Risk Detection
        st.subheader("Risk Analysis")
        is_risk = False

        for key in ["Phone Numbers", "Emails", "UPI IDs"]:
            current = entities[key]
            past = []

            for item in st.session_state.history[:-1]:
                past.extend(item["entities"][key])

            for val in current:
                if val in past:
                    is_risk = True
                    st.warning(f"{val} seen before")

        if is_risk:
            st.error("High Risk Complaint")
        else:
            st.success("No repeat pattern found")

# -------- Bulk --------
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    if "complaint" in df.columns:
        results = []

        for text in df["complaint"]:
            category = classify(str(text))
            entities = extract_entities(str(text))

            st.session_state.history.append({
                "category": category,
                "entities": entities
            })

            results.append({
                "Complaint": text,
                "Category": ", ".join(category),
                "Phones": entities["Phone Numbers"],
                "Emails": entities["Emails"],
                "URLs": entities["URLs"],
                "UPIs": entities["UPI IDs"]
            })

        st.subheader("Bulk Results")
        st.dataframe(results)

        csv = pd.DataFrame(results).to_csv(index=False).encode('utf-8')
        st.download_button("Download Results", csv, "results.csv")

# -------- Dashboard --------
st.write("---")
st.markdown("## 📊 Analytics Dashboard")

categories = []

for item in st.session_state.history:
    categories.extend(item["category"])

if categories:
    df_chart = pd.DataFrame({"Category": categories})
    chart_data = df_chart["Category"].value_counts()

    total = chart_data.sum()

    st.subheader("Crime Distribution")

    for cat, count in chart_data.items():
        percent = (count / total) * 100
        st.write(f"**{cat}** — {count} ({percent:.1f}%)")
        st.progress(count / total)

# -------- Summary --------
st.write("---")

all_values = []

for item in st.session_state.history:
    all_values.extend(item["entities"]["Phone Numbers"])
    all_values.extend(item["entities"]["Emails"])
    all_values.extend(item["entities"]["UPI IDs"])

repeat_count = sum(1 for v in set(all_values) if all_values.count(v) > 1)

st.subheader("🚨 Risk Summary")
st.write(f"Repeat Entities: {repeat_count}")

if repeat_count > 0:
    st.error("Multiple repeat offenders detected")
else:
    st.success("No major patterns detected")
