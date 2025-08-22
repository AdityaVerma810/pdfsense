# PDFsense - PDF Heading Extractor

## Steps to Run Locally

1. Install Python 3.8+
2. Install dependencies:
   pip install -r requirements.txt
3. Put any PDF inside the `input/` folder
4. Run:
   python main.py
5. Output will be saved in the `output/` folder as .json



PDF Multilingual Parser

A Python tool to extract headings from multilingual PDFs and output them as structured JSON files. It supports dynamic PDF parsing for any language and automatically detects headings (H1, H2) using font size and bold formatting. This tool runs in a Docker container for portability.

Folder Structure

PDFsense/
├── Dockerfile               # Docker configuration
├── main.py                  # Python script to process PDF and extract outline
├── requirements.txt         # Dependencies for the project
├── input/                   # Folder to store input PDFs for processing
│   └── your-test.pdf        # Example PDF file
└── output/                  # Folder where output JSON files will be stored
    └── output.json          # Output JSON generated after processing PDF

Dependencies
This project requires the following Python libraries:

pymupdf: For PDF text extraction and analysis.

langdetect: For detecting the language of the extracted headings.

You can install these dependencies using the requirements.txt file.

How to Set Up and Run
1. Clone the repository
First, clone this repository to your local machine.


git clone <repository-url>
cd adobe_pdf_parser
2. Build the Docker container
Ensure you have Docker installed on your system. If not, install it from here.

Then, build the Docker image:

bash
Copy
Edit
docker build -t adobe-parser .
This command will:

Build the container using the Dockerfile provided.

Install all dependencies specified in requirements.txt.

3. Run the Docker container
After building the Docker image, you can run the container to process a PDF file. The script will look for PDFs inside the input/ folder and generate a structured JSON file in output.json.

To run the container:

bash
Copy
Edit
docker run --rm -v "$(pwd)/input:/app/input" -v "$(pwd)/output:/app/output" adobe-parser
This command will:

Mount the input/ folder of your local machine to the container.

Mount the output/ folder to store the output.json file.

The script will process the first PDF it finds in the input/ folder and generate output.json in the output/ folder.

4. Check Output
The result will be saved in the output/output.json file, which will contain the extracted headings and their detected language. Here's an example output:

json
Copy
Edit
{
    "title": "",
    "outline": [
        {
            "level": "H1",
            "text": "परिचय ",
            "page": 0,
            "language": "hi"
        },
        {
            "level": "H2",
            "text": "目的 ",
            "page": 1,
            "language": "ja"
        },
        {
            "level": "H1",
            "text": "Introduction ",
            "page": 2,
            "language": "en"
        }
    ]
}
5. Add More PDFs
You can add any number of PDFs to the input/ folder, and the script will process the first PDF found in that folder.

Docker Workflow
If you want to run this tool without worrying about your environment, Docker makes it easy. With the provided Docker configuration, you can build the container, run it, and process any PDFs by simply adding them to the input/ folder.# pdfsense
# pdfsense
