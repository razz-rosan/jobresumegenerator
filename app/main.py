# import os
# from fastapi import FastAPI, Form, File, UploadFile, Request
# from fastapi.responses import HTMLResponse, FileResponse
# from fastapi.staticfiles import StaticFiles
# from fastapi.templating import Jinja2Templates
# from dotenv import load_dotenv
# from app.llm_chain import get_chain
# from app.pdf_utils import generate_pdf
# from app.utils import extract_text_from_file
# from pathlib import Path
# from tempfile import NamedTemporaryFile

# load_dotenv()

# app = FastAPI()
# chain = get_chain()

# templates = Jinja2Templates(directory="app/templates")

# @app.get("/", response_class=HTMLResponse)
# async def home(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})

# @app.post("/generate")
# async def generate_resume(
#     request: Request,
#     mode: str = Form(...),
#     job_desc: str = Form(...),
#     resume_file: UploadFile = File(None),
#     name: str = Form(""),
#     email: str = Form(""),
#     phone: str = Form(""),
#     linkedin: str = Form(""),
#     github: str = Form(""),
#     field: str = Form(""),
#     summary: str = Form(""),
#     education: str = Form(""),
#     experience: str = Form(""),
#     projects: str = Form(""),
#     skills: str = Form("")
# ):
#     if mode == "upload":
#         if not resume_file:
#             return {"error": "No file uploaded"}
#         resume_text = extract_text_from_file(resume_file.file)
#     else:
#         resume_text = f"""
# # {name}
# 📧 {email} | 📞 {phone}
# 🔗 LinkedIn: {linkedin} | GitHub: {github}
# 🎯 Field: {field}

# ## Summary
# {summary}

# ## Education
# {education}

# ## Experience
# {experience}

# ## Projects
# {projects}

# ## Skills
# {skills}
# """

#     optimized = chain.invoke({
#         "resume": resume_text,
#         "job_description": job_desc
#     })

#     pdf_path = generate_pdf(optimized)
#     return FileResponse(pdf_path, media_type="application/pdf", filename="optimized_resume.pdf")


from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
        <head><title>Resume App</title></head>
        <body>
            <h1>✅ It works!</h1>
            <p>FastAPI on Vercel is running</p>
        </body>
    </html>
    """
