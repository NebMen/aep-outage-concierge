import streamlit as st
from src.data_loader import load_topology
from src.calculator import calculate_restoration_time
from src.concierge import generate_customer_alert

# Cache the data load so the app remains blazingly fast on every interaction
@st.cache_data
def get_data():
    return load_topology('data/raw/matched_upstream.txt')

topology = get_data()

# UI Setup
st.set_page_config(page_title="AI Outage Concierge", layout="centered")
st.title("⚡ AI Outage Concierge")
st.markdown("**Predict. Explain. Prepare. Communicate.**")

# Step 1: Customer Context
st.subheader("1. Customer Lookup")
premise_id = st.text_input("Enter Anonymized Premise ID (e.g., 551102222):")

if premise_id:
    if premise_id in topology:
        st.success("✅ Premise ID Found in Network Topology")
        
        upstream_eq = topology[premise_id]
        
        # Display upstream equipment map
        st.write(f"**Upstream Network Dependencies ({len(upstream_eq)} nodes):**")
        eq_types = [eq['asset_type'] for eq in upstream_eq]
        st.code(" -> ".join(eq_types))
        
        st.markdown("---")
        
        # Step 2: The Judge's Interactive Simulator
        st.subheader("2. Restoration Simulator (Judge Controls)")
        st.info("Change the damage scenario below to see how restoration times dynamically update based on labor constraints and structure dependencies.")
        
        damage_scenario = st.selectbox(
            "Simulate Damage Event:",
            ["Select...", "Minor: Blown Fuse", "Moderate: Downed Wire & Pole", "Severe: Destroyed Transformer Cluster"]
        )
        
        if damage_scenario != "Select...":
            # Map the scenario to specific materials to replace
            if damage_scenario == "Minor: Blown Fuse":
                assets = ["Fuse"]
            elif damage_scenario == "Severe: Destroyed Transformer Cluster":
                assets = ["Transformer (Medium)", "Bracket", "Crossarm", "Fuse"]
            else:
                assets = ["Pole (Medium)", "Crossarm"]
                
          
            # Transparency requirement for the challenge

            time_range = calculate_restoration_time(assets)
            
            st.metric(label="Estimated Restoration Time", value=time_range)
            
            st.caption(f"**AI Reasoning:** Estimate calculated based on replacement of {', '.join(assets)}. Includes baseline labor hours multiplied by a 4.5x indirect labor factor for travel, access, and safety briefings.")
            
            # --- LLM INTEGRATION ---
            st.markdown("---")
            st.subheader("3. Proactive Customer Communication")
            
            with st.spinner("Drafting personalized alert..."):
                alert_message = generate_customer_alert(premise_id, time_range, assets)
                st.info(alert_message)
            
    else:
        st.warning("Premise ID not found. Please try another ID from the dataset.")

    