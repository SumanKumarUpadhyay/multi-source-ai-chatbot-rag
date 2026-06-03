from functools import lru_cache
from backend.loaders.youtube_loader import load_youtube
from backend.loaders.pdf_loader import load_pdf
from backend.rag.vector_store import create_vector_store
from backend.llm.llm_loader import load_llm


# ─────────────────────────────────────────────
# VECTOR DB CACHE
# ─────────────────────────────────────────────

@lru_cache(maxsize=5)
def get_vector_db(video_id: str):
    text = load_youtube(video_id)
    if not text.strip():
        return None
    return create_vector_store(text)


@lru_cache(maxsize=3)
def get_pdf_db(file_path: str):
    text = load_pdf(file_path)
    if not text.strip():
        return None
    return create_vector_store(text)


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

def get_unique_context(docs, max_chunks: int) -> str:
    seen = set()
    unique = []
    for doc in docs:
        content = doc.page_content.strip()
        if content and content not in seen:
            seen.add(content)
            unique.append(content)
        if len(unique) >= max_chunks:
            break
    return "\n\n".join(unique)


def parse_answer(raw: str) -> list[str]:
    if not raw or not raw.strip():
        return []
    lines = [line.strip() for line in raw.strip().splitlines()]
    return [line for line in lines if line]


# ─────────────────────────────────────────────
# SHARED PROMPT TEMPLATE
# ─────────────────────────────────────────────

SYSTEM_RULES = """You are an expert AI assistant. Answer ONLY from the provided context.

═══ STRICT OUTPUT FORMAT ═══

Choose the format based on the question type:

──────────────────────────────────────────────
CASE 1 — Simple fact, number, name, date, yes/no question:
  Output ONE clear sentence only. No heading. No bullets.
  Example: The framework was released in 2020.

──────────────────────────────────────────────
CASE 2 — Explanation or concept question (what is X, how does X work, define X):
  Use this exact 4-part structure:

  ## <Topic Name>
  <One clear intro sentence summarizing what it is.>

  **Definition:** <one sentence>
  **How it works:** <one sentence>
  **Key benefit:** <one sentence>
  **Example:** <one concrete example from the context>

──────────────────────────────────────────────
CASE 3 — Summary, list, topics, overview, comparison, advantages, steps:
  Use this exact structure:

  ## <Short Descriptive Heading>
  <One to two sentence overview paragraph. Be specific, not vague.>

  **<Category or Point Label 1>:** <one complete sentence explaining it>
  **<Category or Point Label 2>:** <one complete sentence explaining it>
  **<Category or Point Label 3>:** <one complete sentence explaining it>
  **<Category or Point Label 4>:** <one complete sentence explaining it — optional>
  **<Category or Point Label 5>:** <one complete sentence explaining it — optional>

  Use REAL labels from the content (e.g. "Quantitative Aptitude", "Key Feature", "Step 1").
  Do NOT use generic labels like "Point 1" or "Item 2".

──────────────────────────────────────────────
ABSOLUTE RULES:
- Never start with "Based on", "According to", "The context says", or any filler phrase.
- Never repeat the question.
- Each labeled line must start with **Label:** on its own line.
- If the answer is not in the context → reply exactly: This topic is not covered.
"""

YOUTUBE_PROMPT = SYSTEM_RULES + """
═══ DATA ═══
Previous conversation:
{chat_history}

Context from video transcript:
{context}

Question: {query}

Answer:"""

PDF_PROMPT = SYSTEM_RULES + """
═══ DATA ═══
Previous conversation:
{chat_history}

Context from document:
{context}

Question: {query}

Answer:"""


# ─────────────────────────────────────────────
# YOUTUBE PIPELINE
# ─────────────────────────────────────────────

def run_youtube_pipeline(video_id: str, query: str, chat_history: str = ""):
    db = get_vector_db(video_id)
    if db is None:
        return ["⚠️ Could not load transcript. Check the Video ID and try again."], []

    retriever = db.as_retriever(search_kwargs={"k": 6})
    search_query = f"{chat_history}\n{query}".strip() if chat_history else query
    docs = retriever.invoke(search_query)

    context = get_unique_context(docs, max_chunks=4)
    if not context:
        return ["This topic is not covered in the video."], docs

    prompt = YOUTUBE_PROMPT.format(
        chat_history=chat_history or "None",
        context=context,
        query=query,
    )

    llm = load_llm()
    response = llm.invoke(prompt)
    lines = parse_answer(response.content)
    return lines if lines else ["This topic is not covered in the video."], docs


# ─────────────────────────────────────────────
# PDF PIPELINE
# ─────────────────────────────────────────────

def run_pdf_pipeline(file_path: str, query: str, chat_history: str = ""):
    db = get_pdf_db(file_path)
    if db is None:
        return ["⚠️ Could not read the PDF. Please try uploading again."], []

    retriever = db.as_retriever(search_kwargs={"k": 8})
    search_query = (
        f"Find sections relevant to: {query}\nPrevious context: {chat_history}"
        if chat_history
        else f"Find sections relevant to: {query}"
    )
    docs = retriever.invoke(search_query)

    context = get_unique_context(docs, max_chunks=5)
    if not context:
        return ["This topic is not covered in the document."], docs

    prompt = PDF_PROMPT.format(
        chat_history=chat_history or "None",
        context=context,
        query=query,
    )

    llm = load_llm()
    response = llm.invoke(prompt)
    lines = parse_answer(response.content)
    return lines if lines else ["This topic is not covered in the document."], docs