# MVP AI Assistant App

# ========================
# STEP 1: Project Structure
# ========================
# root/
# ├── backend/
# │   ├── main.py              # FastAPI backend
# │   ├── utils.py              # Utilities (e.g., LLM call)
# │   └── rag.py                # RAG logic (optional)
# ├── frontend/
# │   └── index.html           # Barebones chat UI (can switch to React later)
# └── requirements.txt            # Dependencies

# ========================
# STEP 2: Backend (FastAPI)
# ========================
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
