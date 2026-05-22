import streamlit as st
from PIL import Image
import datetime
from streamlit_mic_recorder import mic_recorder

# --- APP CONFIGURATION ---
st.set_page_config(page_title="RenovateAI Pro - Enterprise Hub", layout="wide", page_icon="🏗️")

st.title("🏗️ RenovateAI Pro: Enterprise Workspace")
st.caption("A voice-intelligent workspace to manage multiple clients, track sequential trades, and trigger automated follow-ups.")

# --- GET TODAY'S DATE ---
today_str = datetime.date.today().strftime("%Y-%m-%d")
tomorrow_str = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

# --- INITIALIZE DATABASE REGISTER (SESSION STATE WITH PIPELINE STAGES) ---
if 'project_registry' not in st.session_state:
    st.session_state.project_registry = {
        "John Doe": {
            "Name": "John Doe",
            "Email": "client@example.com",
            "Phone": "555-0199",
            "Address": "123 Main St",
            "Stage": "Quote Sent",  # Options: Yet to Quote, Quote Sent, Active Construction, Completed (Pending Payment), Closed Paid
            "Trades_Status": "Pending Follow-up", # Options: All Synced, Pending Follow-up
            "Trades": {"Painter": "painter@trades.com", "Electrician": "sparky@trades.com", "Carpenter": "carpenter@trades.com"},
            "Products": [
                {"Item": "Premium Low-VOC Wall Paint", "Cost": 850.00},
                {"Item": "Slim Recessed LED Spotlights", "Cost": 450.00},
                {"Item": "Replacement Window Units", "Cost": 2200.00},
                {"Item": "Smart Electronic Door Lock", "Cost": 350.00}
            ],
            "Reminders": [
                f"[{today_str}] Send revised breakdown to John.",
                f"[{tomorrow_str}] Call John to finalize window measurements."
            ]
        },
        "Sarah Jenkins": {
            "Name": "Sarah Jenkins",
            "Email": "sarah.j@outlook.com",
            "Phone": "416-555-3211",
            "Address": "742 Evergreen Terrace",
            "Stage": "Yet to Quote",
            "Trades_Status": "All Synced",
            "Trades": {"Painter": "painter@trades.com", "Drywaller": "drywall@expert.com"},
            "Products": [
                {"Item": "Drywall Sheets & Compound", "Cost": 600.00},
                {"Item": "Custom Crown Moldings", "Cost": 1200.00}
            ],
            "Reminders": [
                f"[{today_str}] Message dry waller regarding Sarah's job timeline.",
                "Send deposit receipt confirmation."
            ]
        },
        "Mike Evans": {
            "Name": "Mike Evans",
            "Email": "mike@evansbuilt.com",
            "Phone": "647-555-0900",
            "Address": "99 Blue Jay Way",
            "Stage": "Completed (Pending Payment)",
            "Trades_Status": "All Synced",
            "Trades": {"Painter": "painter@trades.com"},
            "Products": [{"Item": "Initial Site Material Allocation", "Cost": 3500.00}],
            "Reminders": [f"[{today_str}] Call Mike for final project sign-off cheque settlement."]
        }
    }

if 'active_project_key' not in st.session_state:
    st.session_state.active_project_key = "John Doe"

# Safety check: Ensure the active key actually exists in our registry
if st.session_state.active_project_key not in st.session_state.project_registry:
    st.session_state.active_project_key = list(st.session_state.project_registry.keys())[0]

# Shortcut reference to active project data
p_data = st.session_state.project_registry[st.session_state.active_project_key]


# --- SIDEBAR: MULTI-PROJECT NAVIGATION & PROFILE CONTROL ---
st.sidebar.header("📁 Workspace Focus Switcher")

project_list = list(st.session_state.project_registry.keys())
selected_proj = st.sidebar.selectbox("Select Active Project Workspace:", project_list, index=project_list.index(st.session_state.active_project_key))
st.session_state.active_project_key = selected_proj
p_data = st.session_state.project_registry[st.session_state.active_project_key] # Re-bind shortcut

st.sidebar.markdown("---")
st.sidebar.subheader("👤 Profile Parameters")
p_data["Name"] = st.sidebar.text_input("Client Name", value=p_data["Name"])
p_data["Email"] = st.sidebar.text_input("Client Email", value=p_data["Email"])
p_data["Phone"] = st.sidebar.text_input("Client Phone", value=p_data["Phone"])
p_data["Address"] = st.sidebar.text_input("Property Address", value=p_data["Address"])

st.sidebar.subheader("⚙️ Project Stage Manager")
p_data["Stage"] = st.sidebar.selectbox(
    "Current Project Stage:", 
    ["Yet to Quote", "Quote Sent", "Active Construction", "Completed (Pending Payment)", "Closed Paid"],
    index=["Yet to Quote", "Quote Sent", "Active Construction", "Completed (Pending Payment)", "Closed Paid"].index(p_data["Stage"])
)
p_data["Trades_Status"] = st.sidebar.selectbox(
    "Trades Status Notification:", 
    ["All Synced", "Pending Follow-up"],
    index=
