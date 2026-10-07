# System Configuration Core: Save this file exactly as config_center.py
import streamlit as st

def render_system_configuration_center(app_view, active_user_role, active_user_id, profile_data):
    if app_view == "⚙️ System Configuration Settings":
        st.header("⚙️ System Configuration & Personalization Settings")
        st.markdown("Manage custom application theme parameters and review account credential metadata variables.")
        st.divider()
        
        set_tab1, set_tab2 = st.tabs(["🎨 Interface Personalization & Themes", "👤 Profile Metadata Account Ledger"])
        
        with set_tab1:
            st.subheader("🎨 Application Layout Visual Customization")
            chosen_theme = st.selectbox(
                "Select Global Header Layout Palette Suffix:", 
                ["Deep Corporate Blue", "Minimalist Midnight Charcoal"], 
                index=0 if st.session_state.ui_theme == "Deep Corporate Blue" else 1
            )
            if st.button("💾 Apply Layout Customization Styles", use_container_width=True):
                st.session_state.ui_theme = chosen_theme
                st.success("Visual styles updated successfully! Re-rendering layout matrix...")
                st.rerun()
                
        with set_tab2:
            st.subheader("👤 User Profile Registration Database Metadata")
            
            edit_name = st.text_input("Profile Display Full Legal Name:", value=profile_data["name"])
            edit_contact = st.text_input("Registered Contact Mobile Field (+91):", value=profile_data["contact"])
            edit_address = st.text_area("Registered Permanent Location / Corporate Address:", value=profile_data["address"])
            st.text_input("Primary Communication Authentication Email ID (Locked):", value=profile_data["email"], disabled=True)
            
            if st.button("💾 Update Account Roster Ledger Profile", use_container_width=True):
                st.session_state.iam_user_db[active_user_role][active_user_id]["name"] = edit_name
                st.session_state.iam_user_db[active_user_role][active_user_id]["contact"] = edit_contact
                st.session_state.iam_user_db[active_user_role][active_user_id]["address"] = edit_address
                st.success("Roster record metadata fields updated successfully on the server state layer!")
                st.rerun()
