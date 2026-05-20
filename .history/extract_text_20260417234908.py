import pdfplumber
import os

DATA_PATH = "data"

def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def main():
    all_texts = {}
    for file in os.listdir(DATA_PATH):
        if file.endswith(".pdf"):
            path = os.path.join(DATA_PATH, file)
            print(f"Обработка файла: {file}")
            text = extract_text_from_pdf(path)
            all_texts[file] = text

    # Сохраняем извлечённый текст
    os.makedirs("processed", exist_ok=True)
    for filename, text in all_texts.items():
        with open(f"processed/{filename}.txt", "w", encoding="utf-8") as f:
            f.write(text)

    print("✅ Извлечение текста завершено!")

if __name__ == "__main__":
    main()