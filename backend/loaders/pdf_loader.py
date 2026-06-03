from langchain_community.document_loaders import PyPDFLoader
import re

def load_pdf(file_path: str) -> str:
    loader = PyPDFLoader(file_path)
    pages = loader.load()

    # Join all pages
    raw_text = " ".join(page.page_content for page in pages)

    # Clean up: collapse multiple spaces/newlines into single space
    clean_text = re.sub(r"\s+", " ", raw_text).strip()

    return clean_text