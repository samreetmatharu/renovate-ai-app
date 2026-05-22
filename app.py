import streamlit as st
from PIL import Image
import datetime
from streamlit_mic_recorder import mic_recorder

# --- APP CONFIGURATION ---
st.set_page_config(page_title="RenovateAI Pro - Multi-Project Hub", layout="wide", page_icon="🏗️")

st.title("🏗️ RenovateAI Pro: Multi-Project Workspace")
st.caption("A voice-intelligent workspace to manage multiple clients, track sequential trades, and trigger automated follow-ups.")

# --- INITIALIZE DATABASE REGISTER (SESSION STATE) ---
if 'project_registry' not in st.session_state:
    st.session_state.project_registry = {
        "John Doe": {
            "Name": "John Doe",
            "Email": "client@example.com",
            "Phone": "555-0199",
            "Address": "123 Main St",
            "Trades": {"Painter": "painter@trades.com", "Electrician": "sparky@trades.com", "Carpenter": "carpenter@trades.com"},
            "Products": [
                {"Item": "Premium Low-VOC Wall Paint", "Cost": 850.00},
                {"Item": "Slim Recessed LED Spotlights", "Cost": 450.00},
                {"Item": "Replacement Window Units", "Cost": 2200.00},
                {"Item": "Smart Electronic Door Lock", "Cost": 350.00}
            ],
            "Reminders": ["Call John to finalize window frame measurements tomorrow."]
        },
        "Sarah Jenkins": {
            "Name": "Sarah Jenkins",
            "Email": "sarah.j@outlook.com",
            "Phone": "416-555-3211",
            "Address": "742 Evergreen Terrace",
            "Trades": {"Painter": "painter@trades.com", "Drywaller": "drywall@expert.com"},
            "Products": [
                {"Item": "Drywall Sheets & Compound", "Cost": 600.00},
                {"Item": "Custom Crown Moldings", "Cost": 1200.00}
            ],
            "Reminders": ["Send deposit receipt confirmation."]
        }
    }

if 'active_project_key' not in st.session_state:
    st.session_state.active_project_key = "John Doe"

# Safety check: Ensure the active key actually exists in our registry
if st.session_state.active_project_key not in st.session_state.project_registry:
    st.session_state.active_project_key = list(st.session_state.project_registry.keys())[0]

# --- SIDEBAR: MULTI-PROJECT NAVIGATION & PROFILE CONTROL ---
st.sidebar.header("📁 Project Portfolio Navigator")

# Project Switcher Dropdown
project_list = list(st.session_state.project_registry.keys())
selected_proj = st.sidebar.selectbox("Select Active Project Workspace:", project_list, index=project_list.index(st.session_state.active_project_key))
st.session_state.active_project_key = selected_proj

# Fetch active project data shortcut reference
p_data = st.session_state.project_registry[st.session_state.active_project_key]

st.sidebar.markdown("---")
st.sidebar.subheader("👤 Active Profile Details")
client_name = st.sidebar.text_input("Client Name", value=p_data["Name"])
client_email = st.sidebar.text_input("Client Email", value=p_data["Email"])
client_phone = st.sidebar.text_input("Client Phone", value=p_data["Phone"])
client_address = st.sidebar.text_input("Property Address", value=p_data["Address"])

# Write modifications back down to data register
p_data["Name"] = client_name
p_data["Email"] = client_email
p_data["Phone"] = client_phone
p_data["Address"] = client_address

st.sidebar.markdown("---")
st.sidebar.subheader("🛠️ Assigned Project Trades")
for trade, contact in list(p_data["Trades"].items()):
    p_data["Trades"][trade] = st.sidebar.text_input(f"{trade} Handler", value=contact)

# Manual addition buttons on the bottom of navigation panel
st.sidebar.markdown("---")
if st.sidebar.button("➕ Create Blank Project Profile"):
    new_name = f"New Client Profile {len(project_list) + 1}"
    st.session_state.project_registry[new_name] = {
        "Name": new_name, "Email": "", "Phone": "", "Address": "",
        "Trades": {"Painter": "", "Electrician": ""}, "Products": [], "Reminders": []
    }
    st.session_state.active_project_key = new_name
    st.rerun()


# --- MAIN HUB INTERFACES ---
tabs = st.tabs(["🎙️ 1. Global AI Voice Assistant", "📦 2. Scope & Products", "📅 3. Sequential Timeline", "✉️ 4. Client Comms & Reminders"])

# --- TAB 1: GLOBAL AI VOICE ASSISTANT ---
with tabs[0]:
    st.header("🎤 Real-Time Site Audio Command Intake")
    st.markdown("""
    **What you can do here:**
    * **Add new projects:** *"Create a new project profile for Mike Evans, phone 647-555-
