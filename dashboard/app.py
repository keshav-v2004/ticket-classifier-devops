import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import os
import time

st.set_page_config(page_title="Support Portal", layout="wide")

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# Point to the FastAPI backend
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

# --- Routing System ---
st.sidebar.title("Navigation")
role = st.sidebar.radio("Select Portal:", ["Customer Portal", "Admin Dashboard"])
st.sidebar.markdown("---")

# ==========================================
# VIEW 1: THE CUSTOMER PORTAL
# ==========================================
if role == "Customer Portal":
    st.title("Customer Support")
    st.write("Describe your issue below. Our intelligent routing system will direct it to the right team immediately.")
    
    # Notice we don't ask the user for a priority level anymore!
    text = st.text_area("How can we help you today?", height=150, placeholder="E.g., I was double charged for my subscription this month...")
    
    if st.button("Submit Ticket", type="primary"):
        if not text.strip():
            st.warning("Please enter a description of your issue before submitting.")
        else:
            with st.spinner("Analyzing and routing your ticket..."):
                try:
                    res = requests.post(f"{API_URL}/predict", json={"ticket_text": text}).json()
                    st.success(f"Ticket submitted successfully! Your reference ID is **{res['ticket_id']}**.")
                    st.info("Our team has received your request and will follow up via email shortly.")
                except requests.exceptions.ConnectionError:
                    st.error("API Error. Ensure your backend FastAPI server is running.")
                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")

# ==========================================
# VIEW 2: THE ADMIN DASHBOARD
# ==========================================
elif role == "Admin Dashboard":
    st.title("Support Team Workspace")

    if "admin_authenticated" not in st.session_state:
        st.session_state["admin_authenticated"] = False

    if not st.session_state["admin_authenticated"]:
        st.subheader("Admin Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                st.session_state["admin_authenticated"] = True
                st.success("Logged in successfully.")
                st.rerun()
            else:
                st.error("Invalid username or password.")
        st.stop()

    tab1, tab2 = st.tabs(["Live Statistics", "Resolution Desk"])
    
    # --- TAB 1: STATISTICS ---
    with tab1:
        st.header("System Overview")
        if st.button("Refresh Live Stats"):
            try:
                stats = requests.get(f"{API_URL}/stats").json()
                st.metric("Total Tickets Processed", stats.get("total_tickets", 0))
                
                if stats.get("category_counts"):
                    df_cats = pd.DataFrame(list(stats["category_counts"].items()), columns=['Category', 'Count'])
                    fig = px.bar(df_cats, x='Category', y='Count', color='Category', title="Ticket Volume by Category")
                    st.plotly_chart(fig, use_container_width=True)
            except requests.exceptions.ConnectionError:
                st.error("API is unreachable. Ensure your backend FastAPI server is running.")
                
    # --- TAB 2: RESOLUTION DESK ---
    with tab2:
        st.header("Active Ticket Queue")
        
        # Load data into session state to prevent UI resetting
        if st.button("Load/Refresh Queue"):
            try:
                st.session_state['history'] = requests.get(f"{API_URL}/history").json()
            except:
                st.error("Could not fetch history.")

        if 'history' in st.session_state and st.session_state['history']:
            history = st.session_state['history']
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.subheader("Inbox")
                df = pd.DataFrame(history)
                # Show a simplified table for the queue
                st.dataframe(df[['ticket_id', 'category', 'urgency']], use_container_width=True, hide_index=True)
                
                ticket_ids = [t['ticket_id'] for t in history]
                selected_id = st.selectbox("Select Ticket ID to Resolve:", ticket_ids)
                
            with col2:
                st.subheader("Resolution Action Desk")
                if selected_id:
                    # Find the specific ticket data
                    ticket = next(t for t in history if t['ticket_id'] == selected_id)

                    # Display ticket insights without AI confidence
                    st.markdown(f"**Category:** `{ticket.get('category', 'N/A').upper()}` | **Urgency:** `{ticket.get('urgency', 'N/A').upper()}`")
                    
                    st.info(f"**Customer Message:**\n\n{ticket.get('ticket_text', 'N/A')}")
                    
                    st.markdown("### Auto-Generated Response Draft")
                    edited_draft = st.text_area("Review and Edit before sending:", value=ticket.get('draft_response', 'No draft available.'), height=150)
                    
                    # Action Button
                    if st.button("Approve & Send Email", type="primary"):
                        try:
                            # 1. Trigger the delete endpoint on the FastAPI backend
                            requests.delete(f"{API_URL}/ticket/{selected_id}")
                            
                            # 2. Remove it from the local Streamlit state immediately
                            st.session_state['history'] = [t for t in st.session_state['history'] if t['ticket_id'] != selected_id]
                            
                            # 3. Confirm and refresh
                            st.success(f"Response sent! Ticket {selected_id} resolved and removed from queue.")
                            time.sleep(2)
                            st.rerun() 
                        except Exception as e:
                            st.error(f"Failed to resolve ticket. Error: {e}")
        else:
            st.info("No active tickets in the queue. You are all caught up!")