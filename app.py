# import gradio as gr
# from llm_chain import get_chain
# from pdf_utils import generate_pdf
# from utils import extract_text_from_file  

# chain = get_chain()

# def process(file, job_desc):
#     try:
#         resume_text = extract_text_from_file(file)
#     except Exception as e:
#         return f"❌ Error reading file: {e}", None
    
#     optimized = chain.invoke({
#         "resume": resume_text,
#         "job_description": job_desc
#     })
#     pdf_path = generate_pdf(optimized)
#     return optimized, pdf_path

# gr.Interface(
#     fn=process,
#     inputs=[
#         gr.File(label="Upload Your Resume (PDF, DOCX, or TXT)"),  # ✅ File input
#         gr.Textbox(label="Paste Job Description", lines=20, placeholder="Job description you're applying to")
#     ],
#     outputs=[
#         gr.Textbox(label="Optimized Resume"),
#         gr.File(label="Download Optimized Resume as PDF")
#     ],
#     title="📄 Smart Resume Generator Based on Job Description",
#     description="Upload your resume file and job description to get a tailored resume that matches the job!"
# ).launch()


import gradio as gr
from llm_chain import get_chain
from pdf_utils import generate_pdf
from utils import extract_text_from_file

chain = get_chain()

def build_resume_from_fields(name, email, phone, linkedin, github, field, summary, education, experience, projects, skills):
    return f"""
# {name}

📧 {email} | 📞 {phone}  
🔗 LinkedIn: {linkedin} | GitHub: {github}  
🎯 Field: {field}  

## Summary
{summary}

## Education
{education}

## Experience
{experience}

## Projects
{projects}

## Skills
{skills}
"""

def process(resume_mode, file, name, email, phone, linkedin, github, field, summary, education, experience, projects, skills, job_desc):
    if resume_mode == "Upload Resume File":
        if file is None:
            return "❌ Please upload a resume file.", None
        try:
            resume_text = extract_text_from_file(file)
        except Exception as e:
            return f"❌ Error reading file: {e}", None
    else:  # Manual Mode
        resume_text = build_resume_from_fields(name, email, phone, linkedin, github, field, summary, education, experience, projects, skills)

    optimized = chain.invoke({
        "resume": resume_text,
        "job_description": job_desc
    })

    pdf_path = generate_pdf(optimized)
    return optimized, pdf_path

# Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("# 📄 Smart Resume Generator")
    resume_mode = gr.Radio(["Upload Resume File", "Enter Resume Manually"], label="Choose Resume Input Mode")

    # Upload Section
    file_input = gr.File(label="Upload Resume File", visible=False)

    # Manual Fields Section
    with gr.Group(visible=False) as manual_section:
        name = gr.Textbox(label="Full Name")
        email = gr.Textbox(label="Email")
        phone = gr.Textbox(label="Phone")
        linkedin = gr.Textbox(label="LinkedIn")
        github = gr.Textbox(label="GitHub")
        field = gr.Textbox(label="Field (e.g., Data Science, Software Dev)")
        summary = gr.Textbox(label="Summary", lines=2)
        education = gr.Textbox(label="Education", lines=3)
        experience = gr.Textbox(label="Experience", lines=4)
        projects = gr.Textbox(label="Projects", lines=3)
        skills = gr.Textbox(label="Skills (comma-separated)")

    job_desc = gr.Textbox(label="Job Description (Paste full JD here)", lines=8)
    output_text = gr.Textbox(label="Optimized Resume (Markdown)", lines=20)
    output_pdf = gr.File(label="Download Optimized Resume PDF")

    def toggle_mode(choice):
        return {
            file_input: gr.update(visible=choice == "Upload Resume File"),
            manual_section: gr.update(visible=choice == "Enter Resume Manually")
        }

    resume_mode.change(toggle_mode, inputs=resume_mode, outputs=[file_input, manual_section])

    submit = gr.Button("Generate Resume")

    submit.click(
        fn=process,
        inputs=[
            resume_mode, file_input,
            name, email, phone, linkedin, github, field,
            summary, education, experience, projects, skills,
            job_desc
        ],
        outputs=[output_text, output_pdf]
    )

if __name__ == "__main__":
    demo.launch()

