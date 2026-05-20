import os
import re

INPUT_PATH = "processed"
OUTPUT_PATH = "chunks"
CHUNK_SIZE = 600  # Длина фрагмента
OVERLAP = 150     # Перекрытие (соседние чанки содержат часть текста друг друга)

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def split_into_chunks(text, size=CHUNK_SIZE, overlap=OVERLAP):
    chunks = []
    start = 0
    while start < len(text):
        end = start + size
        chunks.append(text[start:end])
        if end >= len(text):
            break
        start += (size - overlap)
    return chunks

def main():
    os.makedirs(OUTPUT_PATH, exist_ok=True)
    
    # Очищаем папку chunks перед новой работой
    for f in os.listdir(OUTPUT_PATH):
        os.remove(os.path.join(OUTPUT_PATH, f))

    for file in os.listdir(INPUT_PATH):
        if file.endswith(".txt"):
            with open(os.path.join(INPUT_PATH, file), "r", encoding="utf-8") as f:
                text = clean_text(f.read())

            chunks = split_into_chunks(text)

            for i, chunk in enumerate(chunks):
                with open(os.path.join(OUTPUT_PATH, f"{file}_chunk_{i}.txt"), "w", encoding="utf-8") as out:
                    out.write(chunk)

    print(f"✅ Текст разбит на фрагменты с перекрытием {OVERLAP} символов!")

if __name__ == "__main__":
    main()