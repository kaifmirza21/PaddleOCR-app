from flask import Flask, render_template, request
from paddleocr import PaddleOCR
import os
import arabic_reshaper
from bidi.algorithm import get_display


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'upload/'

# Initialize PaddleOCR


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():

    language = request.form['language']

    ocr = PaddleOCR(lang=language)

    if 'uploaded_file' not in request.files:
        return "No file part"
    
    file = request.files['uploaded_file']

    if file.filename == '':
        return "No selected file"
    
    
    if file:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)

        result = ocr.ocr(filename)


        res = []
        if language == 'ar':
            extracted_text = []
            
            for ara in result[0]:
                arabic_text = ara[1][0]  # Example Arabic text
                bidi_text = get_display(arabic_text)           # correct its direction
                reshaped_text = arabic_reshaper.reshape(bidi_text)    # correct its shape

                extracted_text.insert(0, reshaped_text)
                # extracted_text.append(reshaped_text)

            separator = ' ' 
            result = separator.join(extracted_text) 
            return render_template('ar_result.html', res =result, length=len(extracted_text)-1)

        else:
            for i in result[0]:
                res.append(i[1][0])

        
        extracted_text = res
        length = len(extracted_text)-1

        return render_template('result.html', extracted_text=extracted_text, length=length)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
