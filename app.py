from flask import Flask, render_template, request
import re
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'txt'}

# Dosya uzantısını kontrol etme fonksiyonu
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# URL'leri metin içinden çıkarma fonksiyonu
def extract_links_from_text(text):
    url_regex = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    return re.findall(url_regex, text)

@app.route('/', methods=['GET', 'POST'])
def index():
    urls = []
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'r') as f:
                text = f.read()
            urls = extract_links_from_text(text)
    return render_template('index.html', urls=urls)

if __name__ == '__main__':
    app.run(debug=True)
