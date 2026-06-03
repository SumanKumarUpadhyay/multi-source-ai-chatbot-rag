from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from functools import lru_cache

# ✅ Cache embeddings model so it loads only once (big speed win)
@lru_cache(maxsize=1)
def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}   # better cosine similarity
    )

def create_vector_store(text: str):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        separators=["\n\n", "\n", ". ", " ", ""]   # split at natural boundaries first
    )

    chunks = splitter.split_text(text)

    embeddings = get_embeddings()   # reuses cached model, no reload

    db = FAISS.from_texts(chunks, embeddings)

    return db