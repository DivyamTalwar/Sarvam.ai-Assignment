import streamlit as st
import subprocess
import os

st.set_page_config(
    page_title="Sarvam Load Test Dashboard",
    page_icon="🚀",
    layout="centered"
)

st.title("Sarvam API Load Testing Dashboard")
st.write("A simple dashboard to trigger and monitor Locust load tests on the Sarvam Transliteration API.")

st.link_button("View Live Google Sheet Report", "https://docs.google.com/spreadsheets/d/1XlR-l99Z8Pz-k3753z8p05G5-y6_nK44xQ4z_n_mX_Q/edit?usp=sharing")

st.sidebar.header("Test Configuration")

api_key = os.getenv("SARVAM_API_KEY")
if not api_key:
    st.sidebar.error("`SARVAM_API_KEY` environment variable is not set!")
    st.sidebar.info("Please set it in your terminal before launching Streamlit:\n`export SARVAM_API_KEY='your-key'`")
    st.stop()
else:
    st.sidebar.success("`SARVAM_API_KEY` is configured.")

concurrency = st.sidebar.number_input("Concurrent Users (-u)", min_value=1, max_value=1000, value=10)
spawn_rate = st.sidebar.number_input("Spawn Rate (-r)", min_value=1, max_value=100, value=2)
run_time = st.sidebar.text_input("Run Time (-t)", value="2m", help="e.g., 30s, 5m, 1h")

if st.sidebar.button("▶️ Start Load Test"):
    st.info(f"🚀 Starting test with {concurrency} users, {spawn_rate} spawn rate for {run_time}...")
    
    report_name = f"reports/dashboard_run_u{concurrency}_r{spawn_rate}"
    
    command = [
        "locust",
        "-f", "locustfile.py",
        "--headless",
        "-u", str(concurrency),
        "-r", str(spawn_rate),
        "--run-time", run_time,
        "--csv", report_name
    ]
    
    try:
        with st.spinner(f"Test in progress... This will take approx. {run_time}."):
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()

        if process.returncode == 0:
            st.success("Test finished successfully!")
            st.code(stdout, language="bash")
            st.balloons()
            st.info(f"Report saved to `{report_name}_stats.csv`. Don't forget to upload the data to the Google Sheet!")
        else:
            st.error("Test failed!")
            st.subheader("Standard Output:")
            st.code(stdout, language="bash")
            st.subheader("Error Output:")
            st.code(stderr, language="bash")
            
    except FileNotFoundError:
        st.error("Error: `locust` command not found. Is Locust installed in your environment?")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
