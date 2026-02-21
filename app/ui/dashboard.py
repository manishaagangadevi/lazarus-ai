import sys
import os

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import streamlit as st
from app.core.analyzer import CodeAnalyzer
from app.services.ai_service import analyze_function_with_ai

st.set_page_config(page_title="Lazarus AI", layout="wide")

st.title("🧠 Lazarus AI - Dead Code Intelligence System")

project_path = st.text_input("Enter Project Folder Path", value="tests")

if st.button("Analyze Project"):

    analyzer = CodeAnalyzer(project_path)
    result = analyzer.analyze_project()

    if not result["unused"]:
        st.success("No unused functions detected 🎉")
    else:
        for func_name, info in result["unused"].items():
            st.subheader(f"🔎 {func_name}")
            st.write(f"📂 File: {info['file']}")
            st.write(f"📍 Line: {info['line']}")

            with st.expander("View Function Source"):
                st.code(info["source"], language="python")

            with st.spinner("AI analyzing..."):
                ai_response = analyze_function_with_ai(info["source"])

            st.markdown("### 🤖 AI Risk Analysis")
            st.write(ai_response)
            st.divider()