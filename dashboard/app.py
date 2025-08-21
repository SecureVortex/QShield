import streamlit as st
import requests
import os

API_URL = "http://localhost:8000"
API_KEY = os.environ.get("QSHIELD_API_KEY", "dev-secret")
HEADERS = {"x-api-key": API_KEY}

st.set_page_config(layout="wide")
st.title("QShield: Quantum Entropy Security Dashboard")

# Endpoint status
def check_status():
    try:
        resp = requests.get(f"{API_URL}/healthz", timeout=2)
        return resp.status_code == 200
    except Exception:
        return False

status = check_status()
st.sidebar.markdown("### Backend Status")
if status:
    st.sidebar.success("🟢 Online")
else:
    st.sidebar.error("🔴 Offline")

# Controls for entropy
st.header("Quantum Entropy")
n = st.number_input("Number of bytes", min_value=1, max_value=64, value=32)

if "entropy_history" not in st.session_state:
    st.session_state["entropy_history"] = []

if st.button("Get Quantum Entropy"):
    resp = requests.get(f"{API_URL}/entropy?n={n}", headers=HEADERS)
    if resp.status_code == 200:
        entropy = resp.json()["entropy"]
        source = resp.json().get("source", "unknown")
        st.session_state["entropy_history"].append((entropy, source))
        if source == "quantum":
            st.success(f"Entropy: {entropy} (Source: Quantum RNG 🌐)")
        else:
            st.warning(f"Entropy: {entropy} (Source: Local Fallback 🖥️)")
    else:
        st.error("Failed to fetch entropy from API.")

# History controls
if st.button("Clear Entropy History"):
    st.session_state["entropy_history"] = []

st.write("### Entropy History")
for i, (entropy, source) in enumerate(st.session_state["entropy_history"], 1):
    st.write(f"{i}. {entropy} [{source}]")

# Chart visualization for entropy byte averages
import numpy as np
if st.session_state["entropy_history"]:
    avg_vals = []
    for val, _ in st.session_state["entropy_history"]:
        arr = np.frombuffer(bytes.fromhex(val), dtype=np.uint8)
        avg_vals.append(arr.mean())
    st.line_chart(avg_vals, height=150, use_container_width=True)

# Anomaly Detection
st.header("Anomaly Detection")
thresh = st.slider("Anomaly threshold", 0.0, 0.5, 0.2, 0.01)
if "anomaly_history" not in st.session_state:
    st.session_state["anomaly_history"] = []

if st.button("Detect Anomaly"):
    resp = requests.get(f"{API_URL}/detect?n={n}&threshold={thresh}", headers=HEADERS)
    if resp.status_code == 200:
        data = resp.json()
        st.session_state["anomaly_history"].append(data)
        st.info(f"Anomaly: {data['anomaly_detected']} (score={data['anomaly_score']:.3f}, threshold={data['threshold']})")
    else:
        st.error("Failed to detect anomaly.")

if st.button("Clear Anomaly History"):
    st.session_state["anomaly_history"] = []

st.write("### Anomaly Detection History")
for i, d in enumerate(st.session_state["anomaly_history"], 1):
    st.write(f"{i}. Score: {d['anomaly_score']:.3f} | Threshold: {d['threshold']} | Anomaly: {d['anomaly_detected']}")

if st.session_state["anomaly_history"]:
    st.line_chart([d['anomaly_score'] for d in st.session_state["anomaly_history"]], height=150, use_container_width=True)

# Quantum Attack Simulation
st.header("Quantum Attack Simulation")
strength = st.slider("Attack strength", 0.0, 1.0, 0.5, 0.01)
if "attack_history" not in st.session_state:
    st.session_state["attack_history"] = []

if st.button("Simulate Attack"):
    resp = requests.get(f"{API_URL}/simulate_attack?strength={strength}", headers=HEADERS)
    if resp.status_code == 200:
        data = resp.json()
        st.session_state["attack_history"].append(data)
        if data['attack_success']:
            st.success(data['description'])
        else:
            st.error(data['description'])
    else:
        st.error("Failed to simulate attack.")

if st.button("Clear Attack History"):
    st.session_state["attack_history"] = []

st.write("### Attack Simulation History")
for i, d in enumerate(st.session_state["attack_history"], 1):
    st.write(f"{i}. Strength: {d['strength']} | Success: {d['attack_success']} | {d['description']}")
