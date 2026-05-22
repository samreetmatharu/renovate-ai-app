import streamlit as st
from PIL import Image
import datetime
from streamlit_mic_recorder import mic_recorder

# --- APP CONFIGURATION ---
st.set_page_config(page_title="RenovateAI - Contractor Assistant", layout="wide", page_icon="🏗️")

st.title("🏗️ RenovateAI: End-to-End Project Assistant")
st.caption("Speak or upload media to build intelligent quotes, manage databases, and automate your workflow.")

# --- INITIALZE DATABASE SYSTEM (SESSION STATE) ---
if 'client_db' not in st.session_state:
    st.session_state.client_db = {"Name": "John Doe", "Email": "client@example.com", "Phone": "555-0199", "Address": "123 Main St"}

if 'trade_db' not in st.session_state:
    st.session_state.trade_db = {
        "Painter": "painter@trades.com",
        "Electrician": "sparky@trades.com",
        "Carpenter": "carpenter@trades.com"
    }

if 'products_list' not in st.session_state:
    st.session_state.products_list = [
        {"Item": "Premium Low-VOC Wall Paint", "Cost": 850.00},
        {"Item": "Slim Recessed LED Spotlights", "Cost": 450.00},
        {"Item": "Replacement Window Units", "Cost": 2200.00},
        {"Item": "Smart Electronic Door Lock", "Cost": 350.00}
    ]

# --- SIDEBAR: DATABASE VIEWER & CONTROLS ---
st.sidebar.header("📁 Active Project Contacts")
client_name = st.sidebar.text_input("Client Name", value=st.session_state.client_db["Name"])
client_email = st.sidebar.text_input("Client Email", value=st.session_state.client_db["Email"])
client_phone = st.sidebar.text_input("Client Phone", value=st.session_state.client_db["Phone"])
client_address = st.sidebar.text_input("Property Address", value=st.session_state.client_db["Address"])

st.sidebar.markdown("---")
st.sidebar.subheader("🛠️ Active Project Trades")
painter_contact = st.sidebar.text_input("Painter Contact", value=st.session_state.trade_db["Painter"])
electrician_contact = st.sidebar.text_input("Electrician Contact", value=st.session_state.trade_db["Electrician"])
carpenter_contact = st.sidebar.text_input("Carpenter Contact", value=st.session_state.trade_db["Carpenter"])

# Save edits back to state
st.session_state.client_db = {"Name": client_name, "Email": client_email, "Phone": client_phone, "Address": client_address}
st.session_state.trade_db = {"Painter": painter_contact, "Electrician": electrician_contact, "Carpenter": carpenter_contact}

# --- MAIN INTERFACE ---
tabs = st.tabs(["🎙️ 1. Voice & Media Intake", "📦 2. Scope & Products", "📅 3. Timeline & Trades", "✉️ 4. Client Comms"])

# --- TAB 1: VOICE & MEDIA INTAKE ---
with tabs[0]:
    st.header("Site Walkthrough Recording")
    st.markdown("Tap the microphone button below and speak naturally about the client, the trades needed, and product details.")
    
    # 🎙️ BROWSER MICROPHONE RECORDER
    audio_record = mic_recorder(
        start_prompt="🎤 Start Voice Note",
        stop_prompt="🛑 Stop Recording",
        key='site_mic'
    )
    
    if audio_record:
        st.audio(audio_record['bytes'])
        st.info("Converting Speech to Text via AI Engine...")
        
        # Simulated Voice Note Transcript based on what you want it to process
        simulated_transcript = (
            "Hey, create a new project for Sarah Jenkins. Her email is sarah.j@outlook.com, phone number is 416-555-3211. "
            "The house is at 742 Evergreen Terrace. We need a new Drywaller for this job, their number is drywall@expert.com. "
            "Also add custom crown moldings to the product list costing 1200 dollars."
        )
        
        st.markdown("### 📝 AI Generated Transcript:")
        st.code(simulated_transcript, language="text")
        
        # Intelligent Processing & Auto-Database Creation Trigger
        st.success("🤖 AI Parsing Engine Actions Executed:")
        
        # 1. Check & Create Client
        st.session_state.client_db = {
            "Name": "Sarah Jenkins",
            "Email": "sarah.j@outlook.com",
            "Phone": "416-555-3211",
            "Address": "742 Evergreen Terrace"
        }
        st.write("✔️ **Created New Client:** Sarah Jenkins saved to workspace.")
        
        # 2. Check & Create Trade
        st.session_state.trade_db["Drywaller"] = "drywall@expert.com"
        st.write("✔️ **Created New Trade Slot:** 'Drywaller' (drywall@expert.com) registered.")
        
        # 3. Add Custom Product
        if not any(d['Item'] == 'Custom Crown Moldings' for d in st.session_state.products_list):
            st.session_state.products_list.append({"Item": "Custom Crown Moldings", "Cost": 1200.00})
            st.write("✔️ **Added Product:** 'Custom Crown Moldings' ($1,200.00) injected into pricing breakdown.")
            
        st.warning("🔄 Sidebar details and product lists updated dynamically! Please check the tabs above.")

    st.markdown("---")
    st.header("Visual Media Upload")
    uploaded_file = st.file_uploader("Upload optional room photo or video walk-through", type=["jpg", "jpeg", "png", "mp4", "mov"])
    if uploaded_file is not None:
        st.success("Media successfully linked to this client profile!")

# --- TAB 2: SCOPE & MULTIPLE PRODUCTS ---
with tabs[1]:
    st.header("Project Line Items & Product Costs")
    st.markdown("Review, modify, or add custom materials and product prices for this specific quote.")
    
    # Render Dynamic Product Management Table
    updated_products = []
    for i, product in enumerate(st.session_state.products_list):
        col1, col2 = st.columns([3, 1])
        with col1:
            item_name = st.text_input(f"Product/Labor Description #{i+1}", value=product["Item"], key=f"prod_name_{i}")
        with col2:
            item_cost = st.number_input(f"Cost ($) #{i+1}", value=float(product["Cost"]), step=50.0, key=f"prod_cost_{i}")
        updated_products.append({"Item": item_name, "Cost": item_cost})
    
    st.session_state.products_list = updated_products

    # Option to manually append a product row
    if st.button("➕ Add Another Product Line Item"):
        st.session_state.products_list.append({"Item": "New Product Item", "Cost": 0.00})
        st.rerun()

    st.markdown("---")
    
    # Financial Calculations
    subtotal = sum(p["Cost"] for p in st.session_state.products_list)
    labor_markup = st.number_input("Contractor Markup/Labor Multiplier (%)", value=20)
    
    total_quote = subtotal * (1 + (labor_markup / 100))
    tax_rate = st.checkbox("Apply Regional Sales Tax (13% HST)", value=True)
    
    final_client_price = total_quote * 1.13 if tax_rate else total_quote
    
    col_stat1, col_stat2 = st.columns(2)
    col_stat1.metric("Materials Subtotal", f"${subtotal:,.2f}")
    col_stat2.metric("Total Client Face Price (Inc. Markup & Tax)", f"${final_client_price:,.2f}")

# --- TAB 3: TIMELINE & TRADES ---
with tabs[2]:
    st.header("Sequential Project Timeline")
    start_date = st.date_input("Project Start Date", datetime.date.today())
    
    schedule = [
        {"Day": 1, "Task": "Site Protection & Prep", "Trade": "Handyman"},
        {"Day": 2, "Task": "Window Framework & Install", "Trade": "Carpenter"},
        {"Day": 3, "Task": "Spotlight & Smart Lock Installation", "Trade": "Electrician"},
        {"Day": 4, "Task": "Ceiling Priming & Painting Work", "Trade": "Painter"},
        {"Day": 5, "Task": "Drywall Patching & Prep", "Trade": "Drywaller" if "Drywaller" in st.session_state.trade_db else "Painter"},
        {"Day": 6, "Task": "Wall Finish Coats & Fine Details", "Trade": "Painter"},
        {"Day": 7, "Task": "Paint and Compound Curing Window", "Trade": "None"},
        {"Day": 8, "Task": "Deep Post-Construction Clean-up", "Trade": "Cleaner"},
    ]
    
    st.table(schedule)
    
    st.subheader("📲 Trade Dispatches")
    selected_day = st.selectbox("Select day to dispatch trade notice:", [f"Day {d['Day']}: {d['Task']}" for d in schedule])
    if st.button("🚀 Dispatch Instructions to Trade"):
        st.info(f"Notification alert successfully dispatched.")

# --- TAB 4: CLIENT COMMS ---
with tabs[3]:
    st.header("Automated Client Communications")
    current_client = st.session_state.client_db["Name"]
    
    st.subheader("1. Project Proposal")
    proposal_text = f"""Subject: Renovation Proposal for {current_client} - Action Required

Hi {current_client},

Thank you for walking me through your property at {st.session_state.client_db['Address']}. We have put together a comprehensive, sequential construction schedule to execute your home modifications smoothly.

Total Investment: ${final_client_price:,.2f} (including applicable taxes)
Estimated Duration: 8 Working Days

Please reply directly to this notice to sign off and secure your calendar slot.

Best regards,
[Your Company Name]"""
    
    st.text_area("Review Proposal Layout", value=proposal_text, height=200)
    if st.button("📧 Send Proposal to Client"):
        st.success(f"Proposal sent seamlessly to {st.session_state.client_db['Email']}!")
        
    st.markdown("---")
    
    st.subheader("2. Five-Star Review Request")
    review_text = f"""Subject: We'd love your feedback, {current_client}! ⭐⭐⭐⭐⭐

Hi {current_client},

The paint is dry and your gorgeous upgraded space is officially yours! 

If you are thrilled with your project execution, would you mind taking 60 seconds to leave us a 5-star review? 

Leave a Review Here: [Insert Your Business Review Link]

Thank you again for choosing us!

Best regards,
[Your Company Name]"""

    st.text_area("Review Request Layout", value=review_text, height=200)
    if st.button("⭐ Send Review Request Email"):
        st.success(f"Review link successfully dispatched to {st.session_state.client_db['Email']}!")
