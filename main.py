from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import openai

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# Allow React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Adjust if your frontend runs on another port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request body model
class EmailRequest(BaseModel):
    event_name: str
    hall_name: str
    venue: str
    image_url: str

# POST endpoint
@app.post("/generate-email")
async def generate_email(req: EmailRequest):
    prompt = f"""
    Create a responsive HTML email invitation for the event titled "{req.event_name}".
    It will be held in "{req.hall_name}" at "{req.venue}".
    Include the image: {req.image_url}.
    The HTML should be clean, mobile-friendly, and include:
    - A <h1> for the title
    - A <p> for the venue
    - An <img> tag for the image
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  
            messages=[
                {"role": "system", "content": "You are a professional HTML email designer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        email_html = response.choices[0].message.content.strip()
        return {"email_html": email_html}

    except Exception as e:
        return {"error": str(e)}
