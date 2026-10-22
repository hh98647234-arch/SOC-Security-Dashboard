import streamlit as st
import pandas as pd
st.set_page_config(page_title="SOC Dashboard", layout="wide")
st.title("SOC security monitoring Dashboard")
st.title("security operation center - monitoring panel")
logs = pd.read_csv("Security_logs.csv")
logs.columns = logs.columns.str.strip()
logs["Severity"] = logs["Severity"].str.strip().str.title()
logs["Event"] = logs["Event"].astype(str).str.strip()
col1, col2, col3 = st.columns(3)
col1.metric("Total Events", len(logs))
col2.metric("High Alerts", (logs["Severity"] == "High").sum())
col3.metric("Critical Alerts", (logs["Severity"] == "Critical").sum())
st.subheader("Security Event Logs")
st.dataframe(logs, use_container_width=True)
st.subheader("Alerts by Severity")
st.bar_chart(logs["Severity"].value_counts())
st.subheader("Filter Security Alerts")
selected_severity = st.selectbox(
    "Selected Severity",
    ["All", "Low", "High", "Critical"]
)
if selected_severity == "All":
    filtered_logs = logs
else:
    filtered_logs = logs[
        logs["Severity"] == selected_severity
    ]
st.dataframe(filtered_logs, width="stretch")
st.subheader("Automatic Security Alerts")
critical_logs = logs[logs["Severity"] == "Critical"]
if not critical_logs.empty:
    st.error("Critical Security Alert Detected!")
    st.dataframe(critical_logs, width="stretch")
else:
    st.success("No Critiacal Alerts Detected")
st.subheader("Suspicious IP Detected")
failed_logins = logs[logs["Event"] == "Failed Login"]
ip_counts = failed_logins["IP Address"].value_counts()
suspicious_ips = ip_counts[ip_counts >= 2]
if not suspicious_ips.empty:
    st.warning("Suspicious IP Detected!")
    st.dataframe(suspicious_ips)
else:
    st.success("No Suspicious IP Detected")
st.subheader("Failed Login Attack Detection")
failed_attempts = logs[
    logs["Event"] == "Failed Login"
]
st.write("Colums:", logs.columns.tolist())
attempt_counts = failed_attempts["IP Address"].value_counts()
brute_force_ips = attempt_counts[attempt_counts >= 3]
if not brute_force_ips.empty:
    st.error("Possible Brute Force Attack Detected!")
    st.dataframe(brute_force_ips)
else:
    st.success("No Brute Force Attack Detected")
st.subheader("Security Attacks Timeline")
logs["Timestamp"] = pd.date_range(
    start="2026-10-22 10:00",
    periods=len(logs),
    freq="min"
)
timeline = logs.groupby("Timestamp").size()
st.line_chart(timeline)
st.subheader("Security Log Monitoring")
if st.button("Refresh Security Logs"):
    st.rerun()
st.info("Click the button to refresh security logs.")
st.subheader("Failed Login Attack Detection")
failed_logins = logs[logs["Event"] == "Failed Login"]
login_counts = failed_logins["IP Address"].value_counts()
suspicious_ips = login_counts[login_counts >= 3]
if not suspicious_ips.empty:
    st.error("Possible Brute Force Attack Detected!")
    st.dataframe(suspicious_ips)
else:
    st.success("No Brute Force Attack Detected")
st.subheader("Attack Risk Score")
risk_points = {
    "Low": 1,
    "High": 5,
    "Critical": 10
}
total_risk = logs["Severity"].map(risk_points).fillna(0).sum()
max_risk = len(logs) * 10
risk_score = round((total_risk / max_risk) * 100) if max_risk else 0 
st.metric("Security Risk Score", f"{risk_score}%")
if risk_score >= 70:
    st.error("HIGH RISK - Immediate Investigation Required!")
elif risk_score >= 40:
    st.warning("MEDIUM RISK - Monitoring Security Events")
else:
    st.success("LOW RISK - Security Status Normal")
st.progress(risk_score)
st.subheader("Security Alerts Summary")
alert_counts = logs["Severity"].value_counts()
low_count = alert_counts.get("Low", 0)
high_count = alert_counts.get("High", 0)
critical_count = alert_counts.get("Critical", 0)
col1, col2, col3 = st.columns(3)
col1.metric("Low Risk Event", low_count)
col2.metric("High Risk Event", high_count)
col3.metric("Critical Events", critical_count)
st.subheader("Security Alerts Distertubion")
st.bar_chart(alert_counts)
st.subheader("Download Security Report")
csv_report = logs.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Download Security Report",
    data=csv_report,
    file_name="SOC_security_report.csv",
    mime="text/csv"
)

