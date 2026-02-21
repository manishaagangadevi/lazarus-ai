import sys
import os

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import streamlit as st
import json
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
        st.success(f"Found {len(result['unused'])} unused function(s)")

        for func_name, info in result["unused"].items():
            st.subheader(f"🔎 {func_name}")
            st.write(f"📂 File: {info['file']}")
            st.write(f"📍 Line: {info['line']}")

            with st.expander("View Function Source"):
                st.code(info["source"], language="python")

            with st.spinner("AI analyzing..."):
                ai_response = analyze_function_with_ai(info["source"])

            st.markdown("### 🤖 AI Risk Analysis")
            st.markdown(ai_response)
            st.divider()

        # ✅ Download Report Button (outside loop)
        report_data = result["unused"]

        st.download_button(
            label="📥 Download JSON Report",
            data=json.dumps(report_data, indent=4),
            file_name="lazarus_report.json",
            mime="application/json"
        )