# Prompt -> LLM -> SQL Query : DONE
# SQL Query -> DB -> Records : DONE
# First we will try it on Simple DB Like SQLite3 DB then we can Scale up to Like SQL-Server DB
# Try with more than 1 Table with Relationship between them. : DONE
# Display the Schema : DONE

import streamlit as st
import pandas as pd
from src.ai_engine import get_gemini_response
from src.db_manager import get_records
# ---------------------------------------------------------------------------------------
# Streamlit Front-End App
st.set_page_config(page_title="Talk with the Database", page_icon="🗄️", layout="wide")
# st.header("🗄️ Talk with the Database (Text-to-SQL)")
st.markdown(
    """
    <div style="background-color:#1E293B; padding:20px; border-radius:10px; margin-bottom:25px">
        <h1 style="color:#F8FAFC; text-align:center; margin:0;">🗄️ Text-to-SQL AI Engine</h1>
        <p style="color:#94A3B8; text-align:center; margin:5px 0 0 0;">Talk directly with your Faculty Database using natural language powered by Gemini 2.5</p>
    </div>
""",
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("🗺️ Database Schema Visualizer")
    st.info(
        "This app connects to `Faculty.db` which contains two related tables:"
    )
    with st.expander("👤 Table: Students"):
        st.markdown(
            """
        - **Id** (INTEGER, PK)
        - **Name** (VARCHAR)
        - **DoB** (TEXT)
        - **Section** (INTEGER)
        """
        )
    
    with st.expander("📊 Table: Marks"):
        st.markdown(
            """
        - **MarkId** (INTEGER, PK)
        - **StudentId** (INTEGER, FK)
        - **Subject** (VARCHAR)
        - **Score** (INTEGER)
        """
        )
    
    st.caption("The Triple AI - Powered by Poetry • Google GenAI • Streamlit")

st.subheader("💡 Ask your Question")

question = st.text_input(
    "Enter your query in plain English or Arabic:",
    placeholder="e.g., Show me the marks of Ahmed Akram in Machine Learning or list students in Section 2.",
    key="input",
)

submit = st.button("🚀 Generate SQL & Run Query", type="primary")

# If Submit is Clicked
if submit:
    if question.strip() == "":
        st.warning("⚠️Please enter a question first!")
    else:
        with st.spinner("🤖 Gemini is analyzing the schema and drafting SQL..."):
            try:
                generated_sql = get_gemini_response(question)
                tab_results, tab_code = st.tabs(
                    ["📊 Database Records", "💻 Generated SQL Code"]
                )
                
                with tab_results:
                    data = get_records(generated_sql, "Faculty.db")
                    if not data:
                        st.info("ℹ️ Query executed successfully, but no records were found.")
                    else:
                        st.success(f"🎉 Successfully fetched {len(data)} rows!")
                        df = pd.DataFrame(data)
                        st.dataframe(df, width='stretch')
                
                with tab_code:
                    st.markdown(
                        "The AI generated the following optimized SQL script:"
                    )
                    st.code(generated_sql, language='sql')

            except Exception as e:
                st.error(f"❌An Error Occurred: {e}!")