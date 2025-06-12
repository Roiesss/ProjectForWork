import pdfplumber
import json

requirements = []
with pdfplumber.open("raw_requirements.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        for line in text.split('\n'):
            if "דרישה:" in line:
                # Example split, adjust as needed for your file's format
                parts = line.split(" - ")
                if len(parts) == 3:
                    requirements.append({
                        "title": parts[0].replace("דרישה:", "").strip(),
                        "condition": parts[1].strip(),
                        "detail": parts[2].strip()
                    })

with open("requirements.json", "w", encoding="utf-8") as f:
    json.dump(requirements, f, ensure_ascii=False, indent=2)