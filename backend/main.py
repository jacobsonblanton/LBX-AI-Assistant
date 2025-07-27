# File: backend/main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import utils

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class UserQuery(BaseModel):
    query: str


@app.post("/ask")
async def ask_ai(data: UserQuery):
    response = utils.query_llm(data.query)
    return {"response": response}


# ========================
# STEP 3: LLM Utilities
# ========================
# File: backend/utils.py
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")


def query_llm(prompt: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"


# ========================
# STEP 6: Run the App
# ========================
# 1. Set your OpenAI key in a `.env` file:
# OPENAI_API_KEY=sk-xxxx

# 2. Start backend:
# $ cd backend
# $ uvicorn main:app --reload

# 3. Open frontend/index.html in browser

# You're now ready to start building a more advanced UI or RAG backend!
