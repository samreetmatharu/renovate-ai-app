import streamlit as st
from PIL import Image
import datetime

# --- APP CONFIGURATION ---
st.set_page_config(page_title="RenovateAI - Contractor Assistant", layout="wide", page_icon="🏗️")

st.title("🏗️ RenovateAI: End-to-End Project Assistant")
st.caption("Upload project media, generate quotes, manage trades, and automate client communication.")

# --- SIDEBAR: CONTACT MANAGEMENT ---
st.sidebar.header("📁 Project Contacts")
client_name = st.sidebar.text_input("Client Name", "John Doe")
client_email = st.sidebar.text_input("Client Email", "client@example.com")

st.sidebar.markdown("---")
st.sidebar.subheader("🛠️ Trade Contacts")
painter_contact = st.sidebar.text_input("Painter Email/Phone", "painter@trades.com")
electrician_contact = st.sidebar.text_input("Electrician Email/Phone", "sparky@trades.com")
carpenter_contact = st.sidebar.text_input("Carpenter Email/Phone", "carpenter@trades.com")

# --- INITIALIZE VARIABLES GLOBALLY ---
# Moving these up here prevents the NameError when swapping tabs!
if 'quoted_price' not in st.session_state:
    st.session_state.quoted_price = 11200
if 'tax_rate' not in st.session_state:
    st.session_state.tax_rate = True

total_with_tax = st.session_state.quoted_price * 1.13 if st.session_state.tax_rate else st.session_state.quoted_price

# --- MAIN INTERFACE ---
tabs = st.tabs(["📸 1. Scope & Estimate", "📅 2. Timeline & Trades", "✉️ 3. Client Comms"])

# --- TAB 1: SCOPE & ESTIMATE ---
with tabs[0]:
    st.header("Upload Project Media")
    uploaded_file = st.file_uploader("Upload a room photo or video walk-through", type=["jpg", "jpeg", "png", "mp4", "mov"])
    
    if uploaded_file is not None:
        if uploaded_file.type in ["image/jpeg", "image/png"]:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Space", width=400)
        else:
            st.video(uploaded_file)
            
        st.success("Media successfully processed by AI Engine!")
        
    st.markdown("---")
    st.subheader("📝 Generated Proposal Details")
    
    # Linked to session state to keep variables persistent across tabs
    st.number_input("Estimated Total Cost ($)", value=10670, key="est_cost")
    st.number_input("Final Quote to Client ($)", value=11200, key="quoted_price")
    st.checkbox("Include HST (13%)", value=True, key="tax_rate")
    
    # Recalculate based on live inputs
    total_with_tax = st.session_state.quoted_price * 1.13 if st.session_state.tax_rate else st.session_state.quoted_price
    st.metric(label="Total Client Face Price (Inc. Tax)", value=f"${total_with_tax:,.2f}")

# --- TAB 2: TIMELINE & TRADES ---
with tabs[1]:
    st.header("Sequential Project Timeline")
    start_date = st.date_input("Project Start Date", datetime.date.today())
    
    schedule = [
        {"Day": 1, "Task": "Site Protection & Prep", "Trade": "Apprentice/Handyman", "Contact": "Internal"},
        {"Day": 2, "Task": "Window Replacement", "Trade": "Carpenter", "Contact": carpenter_contact},
        {"Day": 3, "Task": "Spotlight & Smart Lock Swap", "Trade": "Electrician", "Contact": electrician_contact},
        {"Day": 4, "Task": "Ceiling Priming & Base Paint", "Trade": "Painter", "Contact": painter_contact},
        {"Day": 5, "Task": "Wall Priming & Prep", "Trade": "Painter", "Contact": painter_contact},
        {"Day": 6, "Task": "Wall Finish Coats & Trim", "Trade": "Painter", "Contact": painter_contact},
        {"Day": 7, "Task": "Paint Curing Buffer (No Action)", "Trade": "None", "Contact": "N/A"},
        {"Day": 8, "Task": "Deep Clean & Handover", "Trade": "Cleaner", "Contact": "Internal"},
    ]
    
    st.table(schedule)
    
    st.subheader("📲 Trade Dispatches")
    selected_day = st.selectbox("Select day to dispatch trade notice:", [f"Day {d['Day']}: {d['Task']}" for d in schedule])
    
    if st.button("🚀 Dispatch Instructions to Trade"):
        st.info(f"Notification queued for dispatching to the designated trade handler.")

# --- TAB 3: CLIENT COMMS ---
with tabs[2]:
    st.header("Automated Client Communications")
    
    st.subheader("1. Project Proposal")
    proposal_text = f"""Subject: Renovation Proposal for Your Space - Action Required

Hi {client_name},

Thank you for walking me through your space. Based on our evaluation, we have put together a comprehensive, sequential construction timeline to execute your painting, electrical, and window updates smoothly.

Total Investment: ${total_with_tax:,.2f} (including applicable taxes)
Estimated Duration: 8 Working Days (Sequential Execution)

Please review the attached project schedule breakdown. Reply directly to this email to sign off and secure your calendar slot.

Best regards,
[Your Company Name]"""
    
    st.text_area("Review Proposal Email Layout", value=proposal_text, height=200)
    if st.button("📧 Send Proposal to Client"):
        st.success(f"Proposal sent seamlessly to {client_email}!")
        
    st.markdown("---")
    
    st.subheader("2. Daily Progress Update")
    update_day = st.slider("Select Current Day Complete", 1, 8, 2)
    
    update_text = f"""Subject: Project Update: Day {update_day} Complete!

Hi {client_name},

Here is your daily update on your home renovation. Today, our team successfully completed:
- {schedule[update_day-1]['Task']} (Handled by our expert {schedule[update_day-1]['Trade']})

Tomorrow, we transition strictly to the next phase: {schedule[update_day]['Task']}.

Thank you for your patience as we transform your space!

Best regards,
[Your Company Name]"""

    st.text_area("Review Progress Email Layout", value=update_text, height=180)
    if st.button("📱 Send Progress Update"):
        st.success(f"Day {update_day} update sent to {client_name}!")

    st.markdown("---")

    st.subheader("3. Project Completion & Review Request")
    review_text = f"""Subject: We'd love your feedback, {client_name}! ⭐⭐⭐⭐⭐

Hi {client_name},

The paint is dry, the tools are packed, and your gorgeous new bright space is officially yours! It was an absolute pleasure transforming your entryway and living room.

If you are thrilled with your crisp new coffered ceilings, bright walls, and upgraded features, would you mind taking 60 seconds to leave us a 5-star review? Your support helps small businesses like ours thrive.

Leave a Review Here: [Insert Your Google/Houzz Review Link]

Thank you again for choosing us!

Best regards,
[Your Company Name]"""

    st.text_area("Review Request Email Layout", value=review_text, height=200)
    if st.button("⭐ Send Review Request Email"):
        st.success(f"Review link successfully dispatched to {client_email}!")
