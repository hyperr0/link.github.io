from flask import Flask, render_template, request
import re

app = Flask(__name__)

# URL'leri metin içinden çıkarma fonksiyonu
def extract_links_from_text(text):
    url_regex = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    return re.findall(url_regex, text)

@app.route('/', methods=['GET', 'POST'])
def index():
    urls = []
    if request.method == 'POST':
        text = request.form['text']
        urls = extract_links_from_text(text)
    return render_template('index.html', urls=urls)

if __name__ == '__main__':
    app.run(debug=True)
