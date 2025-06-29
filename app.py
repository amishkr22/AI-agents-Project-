import streamlit as st
import os
from main import create_crew_method
from file_conversion import FileConverter

st.title("Smart Job Application Optimizer 🚀")

uploaded_file = st.file_uploader("Upload your Resume PDF", type=['pdf'])

if uploaded_file is not None:
    pdf_path = os.path.join("uploaded_resume.pdf")
    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.read())

    converter = FileConverter()
    converter.pdf_to_md(pdf_path)
    st.success("PDF converted to Markdown ✅")

    job_posting_url = st.text_input("Job Posting URL")
    github_url = st.text_input("GitHub URL")
    personal_writeup = st.text_area("Personal Write-up")

    if st.button("Run CrewAI 🚀"):
        if not job_posting_url or not github_url or not personal_writeup:
            st.error("Please fill in all the fields.")
        else:
            crew = create_crew_method()
            inputs = {
                'job_posting_url': job_posting_url,
                'github_url': github_url,
                'personal_writeup': personal_writeup
            }
            result = crew.kickoff(inputs=inputs)

            st.write("✅ CrewAI Pipeline Completed!")
            st.json(result)

            if os.path.exists("new_resume.md"):
                with open("new_resume.md", "r") as f:
                    st.download_button("Download New Resume", f, file_name="new_resume.md")

            if os.path.exists("interview_materials.md"):
                with open("interview_materials.md", "r") as f:
                    st.download_button("Download Interview Materials", f, file_name="interview_materials.md")
