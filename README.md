Cyber Complaint Analysis System
App link- https://cyber-complaint-analyzer-bstxa9spbhnpuqr2vvxq4o.streamlit.app/
📌 Overview

A web-based tool that analyzes unstructured cybercrime complaints and converts them into structured insights. It helps identify the type of fraud, extract key entities, and detect repeat patterns to support faster investigation.

🎯 Problem

Cybercrime complaints are often unstructured and handled manually, making it difficult to:

Quickly identify the type of fraud
Extract important details
Detect repeat offenders
💡 Solution

This system processes complaint text and:

Classifies the type of cybercrime
Extracts key entities (phone, email, URL, UPI)
Detects repeated patterns across complaints
Supports bulk analysis via CSV
Features
Multi-label classification (Banking, Phishing, UPI, etc.)
Entity extraction using regex
Repeat detection (basic risk analysis)
Bulk complaint processing (CSV upload)
Simple analytics dashboard
🛠️ Tech Stack
Python
Streamlit
Pandas
Regex
🚀 How to Run Locally
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
pip install -r requirements.txt
streamlit run app.py
📂 CSV Format

Your CSV file should contain a column named:

complaint
🧠 Example Use Cases
Assisting law enforcement in initial complaint analysis
Identifying repeat fraud patterns
Organizing large volumes of complaint data
Future Scope
Integration with real cybercrime databases/APIs
Machine learning for improved classification
Advanced analytics dashboard
Automated alerting for high-risk complaints
⚠️ Disclaimer

This is a prototype built for learning and demonstration purposes. It uses rule-based logic and may not reflect real-world accuracy.

👩‍💻 Author

Sapna
BTech Cybersecurity Student
