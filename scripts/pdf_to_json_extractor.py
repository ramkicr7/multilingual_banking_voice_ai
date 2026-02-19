import os
import json
import fitz  # PyMuPDF

PDF_FOLDER = "pdfs"
OUTPUT_FILE = "data/full_text_dataset.json"

def extract_pdf_to_json():
    output = []

    # Read all PDFs from pdfs folder
    for filename in os.listdir(PDF_FOLDER):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(PDF_FOLDER, filename)
            doc = fitz.open(pdf_path)

            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text = page.get_text("text").strip()

                output.append({
                    "document_name": filename,
                    "page_number": page_num + 1,
                    "text": text
                })

            doc.close()

    # Save all extracted text into JSON
    os.makedirs("data", exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"✅ Dataset created successfully: {OUTPUT_FILE}")
    print(f"✅ Total pages extracted: {len(output)}")

if __name__ == "__main__":
    extract_pdf_to_json()
