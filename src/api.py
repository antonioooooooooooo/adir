from flask import Flask, request, jsonify
from flask_cors import CORS
from adir import generateQuestion, requestHint, toggleSoultion

app = Flask(__name__)

# Allow requests from your frontend origin (no trailing slash!)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

@app.route('/api/question', methods=['POST'])
def create_question():
    data = request.json
    category = data.get('category', 'calculus')
    hebrew = data.get('hebrew', False)
    question = generateQuestion(category, hebrew)
    return jsonify({'question': question})

@app.route('/api/hint', methods=['POST'])
def get_hint():
    data = request.json
    question = data.get('question', '')
    hint = requestHint(question)
    return jsonify({'hint': hint})

@app.route('/api/solution', methods=['POST'])
def get_solution():
    data = request.json
    question = data.get('question', '')
    explain = data.get('explain', True)
    solution = toggleSoultion(question, explain)
    return jsonify({'solution': solution})

if __name__ == '__main__':
    app.run(debug=True, port=5001)