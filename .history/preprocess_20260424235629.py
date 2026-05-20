import os
import re

INPUT_PATH = "processed"
OUTPUT_PATH = "chunks"
CHUNK_SIZE = 500  # количество символов

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def split_into_chunks(text, chunk_size=500, overlap=100):
    chunks = []
    for i in range(0, len(text), chunk_size - overlap):
        chunks.append(text[i:i + chunk_size])
    return chunks

def main():
    os.makedirs(OUTPUT_PATH, exist_ok=True)

    for file in os.listdir(INPUT_PATH):
        if file.endswith(".txt"):
            with open(os.path.join(INPUT_PATH, file), "r", encoding="utf-8") as f:
                text = clean_text(f.read())

            chunks = split_into_chunks(text)

            for i, chunk in enumerate(chunks):
                with open(
                    os.path.join(OUTPUT_PATH, f"{file}_chunk_{i}.txt"),
                    "w",
                    encoding="utf-8",
                ) as out:
                    out.write(chunk)

    print("✅ Текст успешно очищен и разбит на фрагменты!")

if __name__ == "__main__":
    main()