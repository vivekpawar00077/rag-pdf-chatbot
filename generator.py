import os
import time
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import errors

load_dotenv(Path(__file__).parent / ".env")
from google.genai import types
client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"],
    http_options=types.HttpOptions(timeout=20000),
)
MODEL = "gemini-flash-lite-latest"
RETRYABLE = (429, 500, 503, 504)


def answer(question, retrieved, retries=4):
    context = "\n\n".join(f"[Page {r['page']}]\n{r['text']}" for r in retrieved)
    prompt = f"""You are a helpful assistant answering questions about a document.
Use ONLY the context below. If the answer is not in the context,
say "I couldn't find that in the document."

Context:
{context}

Question: {question}
Answer:"""

    for attempt in range(retries):
        try:
            response = client.models.generate_content(model=MODEL, contents=prompt)
            return response.text
        except errors.APIError as e:
            if e.code in RETRYABLE and attempt < retries - 1:
                time.sleep(2 * (2 ** attempt))
                continue
            if e.code in RETRYABLE:
                return "The AI service is busy right now. Please try again in a minute."
            raise