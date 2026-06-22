# Prompt -> LLM -> SQL Query : DONE
# SQL Query -> DB -> Records : DONE
# First we will try it on Simple DB Like SQLite3 DB then we can Scale up to Like SQL-Server DB
# Try with more than 1 Table with Relationship between them. : DONE
# Display the Schema : DONE
# --------------------------------------------------------------------------------------------
import pandas as pd
import streamlit as st

# Import centralized configuration and engines
from src.config import initialize_session_state
from src.auth import render_login_page
from src.ai_engine import get_gemini_response
from src.db_manager import get_records

# Import separated role views (NEW DESIGN Architecture)
from src.admin_view import render_admin_dashboard
from src.user_view import render_user_dashboard

# 1. Page Configuration & Initial Layout Setup
st.set_page_config(page_title="Secure Text-to-SQL Engine", page_icon="🗄️", layout="wide")
initialize_session_state()

# 2. 🔒 Security Guardrail: Enforce Gateway Portal Authentication
if not st.session_state.logged_in:
    render_login_page()
    st.stop()

# ---------------------------------------------------------------------------------------
# 🗄️ Main Enterprise Dashboard Panel
# ---------------------------------------------------------------------------------------

# App Banner Header & Active Session Context Render
st.markdown(
    f"""
    <div style="background-color:#1E293B; padding:15px; border-radius:10px; margin-bottom:25px; display: flex; justify-content: space-between; align-items: center;">
        <div style="color:#F8FAFC; font-size: 24px; font-weight: bold;">🗄️ NexusSQL AI Engine</div>
        <div style="color:#94A3B8; font-size: 16px;">
            👤 User: <b>{st.session_state.username}</b> | 🛡️ Access Level: <span style="color:#10B981; font-weight:bold;">{st.session_state.role.upper()}</span>
        </div>
    </div>
""",
    unsafe_allow_html=True,
)

# Sidebar UI Navigation Controls
with st.sidebar:
    st.header("⚙️ Control Panel")
    if st.button("🚪 Logout", type='secondary', use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""
        st.rerun()
    
    st.markdown("---")
    st.header("🗺️ Database Schema Blueprint")
    st.info("Target schema mappings for query translations:")
    
    with st.expander("👤 Table: Students"):
        st.markdown("- **Id** (INTEGER, PK)\n- **Name** (VARCHAR)\n- **DoB** (TEXT)\n- **Section** (INTEGER)")
    with st.expander("📊 Table: Marks"):
        st.markdown("- **MarkId** (INTEGER, PK)\n- **StudentId** (INTEGER, FK)\n- **Subject** (VARCHAR)\n- **Score** (INTEGER)")
    st.caption("The Triple AI - Powered by Poetry")

# 🧠 STEP 4: Render the UI Workflow Dynamically based on Authenticated Role
if st.session_state.role == "admin":
    render_admin_dashboard()
else:
    render_user_dashboard()

# 5. Core Unified AI Query Generation Interface 
st.subheader("📝 Ask your Question")
question = st.text_input(
    "Enter your database query or analytical question:",
    placeholder="e.g., Show me the marks of Ahmed Akram or list students in Section 2." if st.session_state.role == 'user' else "e.g., Update score for student, delete student record, or fetch statistics...",
    key="input",
)

submit = st.button("🚀 Execute Query via Gemini Engine", type="primary")

if submit:
    if question.strip() == "":
        st.warning("⚠️ Please enter a question first!")
    else:
        with st.spinner("🤖 Security check passing & drafting optimized SQL..."):
            try:
                # Query the AI translation pipeline passing the active permission constraint
                generated_sql = get_gemini_response(question, st.session_state.role)
                
                # Intercept query execution if the engine triggered a security forbidden flag
                if generated_sql == "FORBIDDEN":
                    st.error(
                        "🚫 SECURITY VIOLATION: Your access level (USER) is strictly restricted to Read-Only operations. "
                        "Data definition or modification commands via text are blocked."
                    )
                else:
                    tab_results, tab_code = st.tabs(["📊 Database Records", "💻 Generated SQL Code"])
                    
                    with tab_results:
                        data = get_records(generated_sql)
                        if not data:
                            st.info("ℹ️ Query executed successfully. No records returned (or modifications saved if Admin).")
                        else:
                            st.success(f"🎉 Successfully fetched {len(data)} rows!")
                            df = pd.DataFrame(data)
                            st.dataframe(df, use_container_width=True)
                    
                    with tab_code:
                        st.markdown("The AI engine compiled and optimized the following statement:")
                        st.code(generated_sql, language='sql')

            except Exception as e:
                st.error(f"❌ Execution Blocked: {e}!")
                