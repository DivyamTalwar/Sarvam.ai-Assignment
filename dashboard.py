import streamlit as st
import subprocess
import os

st.set_page_config(
    page_title="Sarvam Load Test Dashboard",
    page_icon="🚀",
    layout="centered"
)

st.title("🚀 Sarvam API Load Testing Dashboard")
st.write("A simple dashboard to trigger and monitor Locust load tests on the Sarvam Transliteration API.")
st.link_button("View Live Google Sheet Report", "https://docs.google.com/spreadsheets/d/1js20yHXr_c3Dkxti9tkjoXQbtlf8NKBOe1LMBTX4I3o/edit?usp=sharing")

st.sidebar.header("Test Configuration")
try:
    api_key = st.secrets["SARVAM_API_KEY"]
    st.sidebar.success("`SARVAM_API_KEY` loaded successfully from Streamlit secrets.")
except KeyError:
    st.sidebar.error("`SARVAM_API_KEY` not found in Streamlit secrets!")
    st.sidebar.info(
        "Please add your API key to your Streamlit secrets. "
        "For local development, create a file at `.streamlit/secrets.toml` with:\n\n"
        '`SARVAM_API_KEY = "your_key_here"`'
    )
    st.stop()
concurrency = st.sidebar.number_input("Concurrent Users (-u)", min_value=1, value=10)
spawn_rate = st.sidebar.number_input("Spawn Rate (-r)", min_value=1, value=2)
run_time = st.sidebar.text_input("Run Time (-t)", value="2m")

if st.sidebar.button("▶️ Start Load Test"):
    st.info(f"🚀 Starting test with {concurrency} users...")
    report_name = f"reports/dashboard_run_u{concurrency}_r{spawn_rate}"
    command = ["locust", "-f", "locustfile.py", "--headless", "-u", str(concurrency), "-r", str(spawn_rate), "--run-time", run_time, "--csv", report_name]

    with st.spinner(f"Test in progress... This will take approx. {run_time}."):
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()

    if process.returncode == 0:
        st.success("✅ Test finished successfully!")
        st.code(stdout, language="bash")
        st.balloons()
    else:
        st.error("❌ Test failed!")
        st.code(stderr, language="bash")