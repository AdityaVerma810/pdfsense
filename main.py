import os
import json
import fitz
from flask import Flask, request, jsonify, render_template, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder="templates", static_folder="static")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(BASE_DIR, "input")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


def extract_headings_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    outline = []
    combined_title = []
    fallback_title = None

    for page_num in range(len(doc)):
        page = doc[page_num]
        blocks = page.get_text("dict")["blocks"]

        for block in blocks:
            if "lines" not in block:
                continue

            for line in block["lines"]:
                spans = line["spans"]
                text = " ".join(span["text"].strip() for span in spans).strip()

                if not text or len(text) < 2:
                    continue

                font_size = spans[0]["size"]
                font_flags = spans[0]["flags"]
                is_bold = font_flags & 2 != 0

                if page_num == 0 and fallback_title is None:
                    fallback_title = text

                if font_size > 14 or is_bold:
                    level = "H1" if font_size >= 16 else "H2"
                    heading = {
                        "level": level,
                        "text": text,
                        "page": page_num,
                    }
                    outline.append(heading)
                    if page_num == 0 and level == "H1":
                        combined_title.append(text)

    title = " ".join(combined_title).strip() or fallback_title or "Unknown Title"

    return {
        "title": title.strip(),
        "outline": outline,
    }


def process_pdf_file(pdf_path, filename):
    result = extract_headings_from_pdf(pdf_path)
    output_filename = f"output_{os.path.splitext(filename)[0]}.json"
    output_path = os.path.join(OUTPUT_DIR, output_filename)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

    return output_filename, result


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/process", methods=["POST"])
def process_files():
    if "files" not in request.files:
        return jsonify({"success": False, "message": "No files uploaded."}), 400

    uploaded_files = request.files.getlist("files")
    if not uploaded_files or all(file.filename == "" for file in uploaded_files):
        return jsonify({"success": False, "message": "Please choose at least one PDF."}), 400

    outputs = []
    for file in uploaded_files:
        if file.filename == "":
            continue

        if not file.filename.lower().endswith(".pdf"):
            return jsonify({"success": False, "message": "Only PDF files are supported."}), 400

        filename = secure_filename(file.filename)
        pdf_path = os.path.join(INPUT_DIR, filename)
        file.save(pdf_path)
        output_filename, result = process_pdf_file(pdf_path, filename)
        outputs.append({
            "input": filename,
            "output": output_filename,
            "json": result,
        })

    return jsonify({
        "success": True,
        "message": f"Processed {len(outputs)} file(s).",
        "outputs": outputs,
    })


@app.route("/output/<path:filename>")
def serve_output(filename):
    return send_from_directory(OUTPUT_DIR, filename)


if __name__ == "__main__":
    app.run(debug=True)
