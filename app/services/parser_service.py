"""
Parse Resumes
"""
from fastapi import UploadFile
from openai import OpenAI
import json
import os
import PyPDF2


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))



def extract_text_from_resume(file: UploadFile) -> str:
    if file.filename.endswith(".pdf"):
        reader = PyPDF2.PdfFileReader(file.filename)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    else:
        raise ValueError("Unsupported file type")


def parse_resume(text: str) -> dict:
    """Send resume text to OpenAI for parsing into structured JSON."""

    prompt =f"""
        Extract structured resume information from the text below.
    Return valid JSON with fields:
    - name
    - email
    - phone
    - skills (list of strings)
    - experience (list of {{company, role, years}})
    - education (list of {{degree, institution, years}})
    - achievements (list of {{achievement, years}})
    
    Resume Text: {text}
    """

    response = client.responses.create(
        model="gpt-4.1-mini",  # lightweight + good for parsing
        input=prompt,
        temperature=0,
    )

    try:
        parsed_resume = json.loads(response.output_text)
    except Exception:
        parsed_resume = {"raw_output": response.output_text}

    return parsed_resume
