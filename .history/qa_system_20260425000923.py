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
    
    import requests

API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
headers = {"Authorization": "Bearer ТВОЙ_ТОКЕН_ЗДЕСЬ"}

def query_llm(prompt):
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
    return response.json()[0]['generated_text']

def get_answer(question, k=3):
    # Твой текущий поиск
    q_embedding = model.encode([question]).astype("float32")
    distances, indices = index.search(q_embedding, k)
    context = " ".join([texts[i] for i in indices[0]])

    # Формируем промпт для модели
    prompt = f"<|system|>\nОтветь на вопрос кратко, используя только контекст.</s>\n<|user|>\nКонтекст: {context}\nВопрос: {question}</s>\n<|assistant|>"
    
    full_response = query_llm(prompt)
    # Очищаем ответ от промпта (модель Zephyr возвращает всё вместе)
    return full_response.split("<|assistant|>")[-1].strip()