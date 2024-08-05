from flask import Flask, request, jsonify, render_template_string
import newspaper
import nltk
from flask_cors import CORS
import os

# Set NLTK data path
nltk.data.path.append(os.path.join(os.path.dirname(__file__), 'nltk_data'))

app = Flask(__name__)
CORS(app)

# HTML template for the startup page
startup_page = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome</title>
</head>
<body>
    <h1>Welcome Home</h1>

</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(startup_page)

@app.route('/summarize', methods=['POST'])
def summarize_article():
    url = request.json.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    try:
        article = newspaper.Article(url)
        article.download()
        article.parse()
        article.nlp()

        img_url = article.top_image
        title = article.title
        full_text = article.text.replace('Advertisement', '')
        summary = article.summary.replace('Advertisement', '')

        return jsonify({
            'img_url': img_url,
            'title': title,
            'full_text': full_text,
            'summary': summary
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
