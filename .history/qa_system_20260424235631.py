import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"

# Загрузка модели и индекса
model = SentenceTransformer(MODEL_NAME)
index = faiss.read_index("faiss_index.bin")

# Загрузка текстов
with open("texts.txt", "r", encoding="utf-8") as f:
    texts = f.readlines()



def get_answer(question, k=3):
    q_embedding = model.encode([question]).astype("float32")
    distances, indices = index.search(q_embedding, k)
    
    context = ""
    for i in indices[0]:
        context += texts[i].strip() + " "

   
    prompt = f"Контекст: {context}\n\nВопрос: {question}\n\nОтвети коротко и точно, основываясь только на контексте:"
    
    