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
    index=["All Synced", "Pending Follow-up"].index(p_data["Trades_Status"])
)

st.sidebar.markdown("---")
if st.sidebar.button("➕ Create Blank Project Profile"):
    new_name = f"New Client Profile {len(project_list) + 1}"
    st.session_state.project_registry[new_name] = {
        "Name": new_name, "Email": "", "Phone": "", "Address": "",
        "Stage": "Yet to Quote", "Trades_Status": "All Synced",
        "Trades": {"Painter": ""}, "Products": [], "Reminders": []
    }
    st.session_state.active_project_key = new_name
    st.rerun()


# --- MAIN HUB INTERFACES ---
tabs = st.tabs(["📊 1. Command Dashboard", "🎙️ 2. AI Voice Intake", "📦 3. Scope & Products", "📅 4. Sequential Timeline", "✉️ 5. Comms & Reminders"])

# --- TAB 1: COMMAND DASHBOARD ---
with tabs[0]:
    st.header("📈 Contractor Operations Dashboard")
    st.markdown("Real-time operational snapshots across your entire project portfolio pipeline.")
    
    # 📊 DYNAMIC METRIC AGGREGATION CALCULATIONS
    total_handling = len(st.session_state.project_registry)
    yet_to_quote = sum(1 for p in st.session_state.project_registry.values() if p["Stage"] == "Yet to Quote")
    quote_sent = sum(1 for p in st.session_state.project_registry.values() if p["Stage"] == "Quote Sent")
    trade_follow_up = sum(1 for p in st.session_state.project_registry.values() if p["Trades_Status"] == "Pending Follow-up")
    pending_payment = sum(1 for p in st.session_state.project_registry.values() if p["Stage"] == "Completed (Pending Payment)")
    
    # Render KPIs row
    col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns(5)
    col_m1.metric("📁 Handled Projects", total_handling)
    col_m2.metric("📝 Yet to Quote", yet_to_quote)
    col_m3.metric("📨 Quotes Dispatched", quote_sent)
    col_m4.metric("🛠️ Trade Follow-ups", trade_follow_up)
    col_m5.metric("💰 Pending Payments", pending_payment)
    
    st.markdown("---")
    
    # 📅 SEPARATE BLOCK: TODAY'S DYNAMIC FOLLOW-UPS
    st.subheader(f"📅 Critical Action Items Due Today ({today_str})")
    
    today_reminders_found = False
    
    # Scan through every single project record to extract timestamps matching today
    for proj_name, data in st.session_state.project_registry.items():
        for reminder in data["Reminders"]:
            if f"[{today_str}]" in reminder:
                today_reminders_found = True
                clean_reminder_text = reminder.replace(f"[{today_str}]", "").strip()
                
                # Render clean notification box for today's workflows
                col_alert, col_action = st.columns([5, 1])
                with col_alert:
                    st.warning(f"**{proj_name}**: {clean_reminder_text}")
                with col_action:
                    if st.button("Mark Complete", key=f"dash_clear_{proj_name}_{hash(reminder)}"):
                        data["Reminders"].remove(reminder)
                        st.success("Task completed!")
                        st.rerun()
                        
    if not today_reminders_found:
        st.success("🎉 Incredible job! You have zero open follow-up actions scheduled for today.")

    st.markdown("---")
    
    # 📂 PORTFOLIO STAGE BREAKDOWN TABLE VIEW
    st.subheader("📋 Pipeline Breakdown Directory")
    summary_data = []
    for k, v in st.session_state.project_registry.items():
        summary_data.append({
            "Project Client": k,
            "Current Pipeline Stage": v["Stage"],
            "Subcontractor Status": v["Trades_Status"],
            "Active Reminders Count": len(v["Reminders"])
        })
    st.table(summary_data)

# --- TAB 2: GLOBAL AI VOICE ASSISTANT ---
with tabs[1]:
    st.header("🎤 Real-Time Site Audio Command Intake")
    st.markdown("Tap the microphone button below to log notes, shift workflows, or drop reminders hands-free.")
    
    audio_record = mic_recorder(
        start_prompt="🎤 Start Audio Command Stream",
        stop_prompt="🛑 Disengage Microphone",
        key='global_command_mic'
    )
    
    if audio_record:
        st.audio(audio_record['bytes'])
        st.info("Parsing voice intent signals...")
        
        # Scenario Simulation Selector
        voice_mode = st.radio(
            "Select Simulated Voice Intent to execute:",
            ["Switch to an existing project workspace", "Inject a reminder into a project", "Instantiate a brand new project completely"]
        )
        
        st.markdown("---")
        
        if voice_mode == "Switch to an existing project workspace":
            transcript = "Hey app, pull up the project data for Sarah Jenkins right now please."
            st.code(f"Transcript: \"{transcript}\"", language="text")
            st.session_state.active_project_key = "Sarah Jenkins"
            st.success("🤖 Context Command Recognized: Shifted focus to **Sarah Jenkins**!")
            st.rerun()
            
        elif voice_mode == "Inject a reminder into a project":
            transcript = "Remind me tomorrow to check if the painter finished the ceiling inside John Doe's house."
            st.code(f"Transcript: \"{transcript}\"", language="text")
            
            new_rem = f"[{tomorrow_str}] CRITICAL REMINDER: Confirm if painter finished ceiling panels."
            if new_rem not in st.session_state.project_registry["John Doe"]["Reminders"]:
                st.session_state.project_registry["John Doe"]["Reminders"].append(new_rem)
            st.success("🤖 Intent Extracted: Logged a tomorrow reminder targeting **John Doe's** ledger.")
            
        elif voice_mode == "Instantiate a brand new project completely":
            transcript = "Create a new profile for Mike Evans. Email is mike@evansbuilt.com, address is 99 Blue Jay Way."
            st.code(f"Transcript: \"{transcript}\"", language="text")
            
            st.session_state.project_registry["Mike Evans"] = {
                "Name": "Mike Evans", "Email": "mike@evansbuilt.com", "Phone": "Unassigned", "Address": "99 Blue Jay Way",
                "Stage": "Yet to Quote", "Trades_Status": "All Synced",
                "Trades": {"Painter": "painter@trades.com"}, "Products": [{"Item": "Initial Site Material Allocation", "Cost": 500.00}],
                "Reminders": ["Schedule initial video walkthrough quote inspection."]
            }
            st.session_state.active_project_key = "Mike Evans"
            st.success("🤖 Entity Extracted: Spawned brand new pipeline target **Mike Evans**!")
            st.rerun()

# --- TAB 3: SCOPE & MULTIPLE PRODUCTS ---
with tabs[2]:
    st.header(f"Product Costs Ledger: {st.session_state.active_project_key}")
    
    updated_products = []
    if len(p_data["Products"]) == 0:
        st.warning("No line items initialized yet for this quote.")
    else:
        for i, product in enumerate(p_data["Products"]):
            col1, col2 = st.columns([3, 1])
            with col1:
                item_name = st.text_input(f"Product Description #{i+1}", value=product["Item"], key=f"p_name_{st.session_state.active_project_key}_{i}")
            with col2:
                item_cost = st.number_input(f"Cost ($) #{i+1}", value=float(product["Cost"]), step=50.0, key=f"p_cost_{st.session_state.active_project_key}_{i}")
            updated_products.append({"Item": item_name, "Cost": item_cost})
        
        p_data["Products"] = updated_products

    if st.button("➕ Add Custom Product Line Item"):
        p_data["Products"].append({"Item": "New Product Item Description", "Cost": 0.00})
        st.rerun()

    st.markdown("---")
    subtotal = sum(p["Cost"] for p in p_data["Products"])
    labor_markup = st.number_input("Contractor Profit/Labor Markup Ratio (%)", value=20)
    total_quote = subtotal * (1 + (labor_markup / 100))
    final_client_price = total_quote * 1.13
    
    col_stat1, col_stat2 = st.columns(2)
    col_stat1.metric("Materials Subtotal Base", f"${subtotal:,.2f}")
    col_stat2.metric("Gross Target Cost (Inc. 13% HST)", f"${final_client_price:,.2f}")

# --- TAB 4: SEQUENTIAL TIMELINE ---
with tabs[3]:
    st.header(f"Sequential Execution Schedule: {st.session_state.active_project_key}")
    start_date = st.date_input("Target Commencement Date", datetime.date.today())
    
    schedule = [{"Day": 1, "Task": "Site Isolation & Masking Prep", "Trade": "Handyman Staff"}]
    day_count = 2
    for trade in p_data["Trades"].keys():
        schedule.append({"Day": day_count, "Task": f"Primary Phase Operations for {trade} Work", "Trade": trade})
        day_count += 1
    schedule.append({"Day": day_count, "Task": "Deep Site Cleanup & Client Walkthrough Verification", "Trade": "Internal Cleaning crew"})
    
    st.table(schedule)

# --- TAB 5: CLIENT COMMS & REMINDERS ---
with tabs[4]:
    st.header(f"Communications Suite: {st.session_state.active_project_key}")
    
    st.subheader("📅 All Active Action Item Reminders for this Profile")
    if len(p_data["Reminders"]) == 0:
        st.info("No active text or call alerts set for this project profile.")
    else:
        for idx, reminder in enumerate(p_data["Reminders"]):
            col_rem, col_del = st.columns([5, 1])
            col_rem.warning(f"🔔 {reminder}")
            if col_del.button("❌ Clear", key=f"del_rem_{idx}"):
                p_data["Reminders"].remove(reminder)
                st.rerun()
                
    new_manual_rem = st.text_input("Manually log a reminder alert (Format '[YYYY-MM-DD] Your text' to pinning it to Dashboard):")
    if st.button("💾 Save Reminder"):
        if new_manual_rem:
            p_data["Reminders"].append(new_manual_rem)
            st.rerun()

    st.markdown("---")
    st.subheader("📝 Proposal Outreach Layout")
    proposal_text = f"""Subject: Comprehensive Project Execution Proposal for {p_data['Name']}

Hi {p_data['Name']},

Thank you for walking me through your project at {p_data['Address']}. 

The total project investment will come out to ${final_client_price:,.2f} inclusive of necessary materials, trade resource scheduling, execution labor, and applicable taxes.

Best regards,
[Your Contracting Company Name]"""
    st.text_area("Review Live Email Output Block", value=proposal_text, height=200)
