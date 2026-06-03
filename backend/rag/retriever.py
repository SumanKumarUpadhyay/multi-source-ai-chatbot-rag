def get_relevant_context(vector_db, query, max_chunks=4, chat_history=""):
    # 1. Retriever banao
    retriever = vector_db.as_retriever(search_kwargs={"k": 6})
    
    # 2. Chat history ke saath query banao
    if chat_history:
        query = f"{chat_history}\n{query}"
    
    # 3. Search karo
    docs = retriever.invoke(query)
    
    # 4. Duplicates hatao
    seen = set()
    unique_chunks = []
    for doc in docs:
        content = doc.page_content.strip()
        if content and content not in seen:
            seen.add(content)
            unique_chunks.append(content)
        if len(unique_chunks) >= max_chunks:
            break
    
    # 5. String banao
    context = "\n\n".join(unique_chunks)
    
    return context, docs