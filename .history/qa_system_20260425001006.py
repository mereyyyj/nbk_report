import faiss
import numpy as np
import os
from sentence_transformers import SentenceTransformer

MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"

# Загружаем всё один раз при импорте
if not os.path.exists("faiss_index.bin") or not os.path.exists("texts.txt"):
    raise FileNotFoundError("Сначала запустите скрипты создания индекса!")

model = SentenceTransformer(MODEL_NAME)
index = faiss.read_index("faiss_index.bin")

with open("texts.txt", "r", encoding="utf-8") as f:
    texts = [line.strip() for line in f.readlines()]

def get_answer(question, k=3):
    # Превращаем вопрос в вектор
    q_embedding = model.encode([question]).astype("float32")
    
    # Поиск
    distances, indices = index.search(q_embedding, k)
    
    # Собираем уникальные результаты (чтобы не дублировать из-за overlap)
    unique_results = []
    seen = set()
    
    for idx in indices[0]:
        if idx != -1 and idx < len(texts):
            content = texts[idx]
            if content not in seen:
                unique_results.append(content)
                seen.add(content)
    
    if not unique_results:
        return "К сожалению, подходящая информация в отчетах не найдена."

    # Для улучшения точности без LLM, возвращаем нумерованный список
    formatted_answer = ""
    for i, res in enumerate(unique_results):
        formatted_answer += f"**Фрагмент {i+1}:**\n{res}\n\n"
    
    return formatted_answer