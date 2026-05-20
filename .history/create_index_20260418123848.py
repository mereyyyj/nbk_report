import os
os.environ["HF_HUB_ENABLE_PROGRESS_BARS"] = "1"

import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

CHUNKS_PATH = "chunks"
MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"

def main():
    model = SentenceTransformer(MODEL_NAME)

    texts = []
    for file in os.listdir(CHUNKS_PATH):
        with open(os.path.join(CHUNKS_PATH, file), "r", encoding="utf-8") as f:
            texts.append(f.read())

    embeddings = model.encode(texts, show_progress_bar=True)
    embeddings = np.array(embeddings).astype("float32")

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    faiss.write_index(index, "faiss_index.bin")

    with open("texts.txt", "w", encoding="utf-8") as f:
        for text in texts:
            f.write(text.replace("\n", " ") + "\n")

    print("✅ Векторный индекс успешно создан!")

if __name__ == "__main__":
    main()