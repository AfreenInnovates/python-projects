from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import pdfplumber
import google.generativeai as genai

app = Flask(__name__, static_url_path='', static_folder='static')
CORS(app)

# Ensure you have the correct API key
GEM_MODEL = genai.GenerativeModel('gemini-pro')
genai.configure(api_key="AIzaSyD9UoNoPQyBacklorVMmmB0yINJQcir6OU")

summary_text = ""

def extract_from_pdf(file_path):
    rows_containing_text = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            lines = text.split("\n")
            for line in lines:
                rows_containing_text.append(line.strip())
    
    file_content = "\n\n".join(rows_containing_text)
    return file_content

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    global summary_text
    summary_text = ""  # Reset summary_text for new file uploads

    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and file.filename.lower().endswith('.pdf'):
        file_path = os.path.join(os.getcwd(), file.filename)
        file.save(file_path)
        file_content = extract_from_pdf(file_path)
        
        response = GEM_MODEL.generate_content(f"Give me a summary of the file content: {file_content}.", 
                                              safety_settings=[
                                                    {"category":'HARM_CATEGORY_HARASSMENT', "threshold":'BLOCK_NONE'},
                                                    {"category":'HARM_CATEGORY_DANGEROUS_CONTENT', "threshold":'BLOCK_NONE'},
                                                    {"category":'HARM_CATEGORY_HATE_SPEECH', "threshold":'BLOCK_NONE'},
                                                    {"category":'HARM_CATEGORY_SEXUALLY_EXPLICIT', "threshold":'BLOCK_NONE'},
                                                    {"category": 'HARM_CATEGORY_DANGEROUS', "threshold":'BLOCK_NONE'}],
                                              generation_config=genai.types.GenerationConfig(temperature=0))
        summary_text = response.candidates[0].content.parts[0].text.replace('\n', " ").strip()
        return jsonify({"summary": summary_text})
    else:
        return jsonify({"error": "Invalid file format. Only PDF files are allowed."}), 400

@app.route('/ask', methods=['POST'])
def ask_question():
    global summary_text
    if not summary_text:
        return jsonify({"error": "No summary available. Please upload a PDF first."}), 400
    
    question = request.json.get('question')
    if not question:
        return jsonify({"error": "No question provided."}), 400
    
    response = GEM_MODEL.generate_content(f"""Summary: {summary_text}\n\nQuestion: {question}""", 
                                          safety_settings=[
                                                {"category":'HARM_CATEGORY_HARASSMENT', "threshold":'BLOCK_NONE'},
                                                {"category":'HARM_CATEGORY_DANGEROUS_CONTENT', "threshold":'BLOCK_NONE'},
                                                {"category":'HARM_CATEGORY_HATE_SPEECH', "threshold":'BLOCK_NONE'},
                                                {"category":'HARM_CATEGORY_SEXUALLY_EXPLICIT', "threshold":'BLOCK_NONE'},
                                                {"category": 'HARM_CATEGORY_DANGEROUS', "threshold":'BLOCK_NONE'}],
                                          generation_config=genai.types.GenerationConfig(temperature=0))
    answer = response.candidates[0].content.parts[0].text.replace('\n', " ").strip()
    return jsonify({"answer": answer})

if __name__ == '__main__':
    app.run(debug=True)