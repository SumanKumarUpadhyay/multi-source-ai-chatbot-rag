from langchain_groq import ChatGroq
from config import GROQ_API_KEY
from functools import lru_cache
 
@lru_cache(maxsize=1)
def load_llm():
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.2,       # lower = more factual, less creative
        max_tokens=1048,       # cap output so response is fast and concise
        api_key=GROQ_API_KEY
    )