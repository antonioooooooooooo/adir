from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from adir import generateQuestion, requestHint, toggleSoultion, ocr_to_text, verify_sol

app = Flask(__name__)

# Allow requests from your frontend origin (no trailing slash!)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

@app.route('/api/verify-solution', methods=['POST'])
def verify_solution():
    if 'solution' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['solution']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Extract text from the image
            extracted_text = ocr_to_text(filepath)
            # Verify the solution
            is_correct = verify_sol(extracted_text)
            
            # Clean up the uploaded file
            os.remove(filepath)
            
            return jsonify({
                'isCorrect': is_correct,
                'extractedText': extracted_text
            })
        except Exception as e:
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Invalid file type'}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5001)


q1 = """1. קטע הכביש שבין יישוב A ליישוב B מחולק לשניים: קטע כביש עירוני וקטע כביש מהיר.
האורך של קטע הכביש המהיר גדול פי 7 מן האורך של קטע הכביש העירוני.
שתי מכוניות א' וב' יצאו באותה השעה ונסעו זו לקראת זו: מכונית א' יצאה מיישוב B ומכונית ב' יצאה מיישוב A.
במשך כל אותו היום מהירות הנסיעה של כל אחת מן המכוניות בקטע הכביש המהיר הייתה קבועה וגדולה פי 2 ממהירות הנסיעה שלה בקטע הכביש העירוני.
המכוניות נפגשו באמצע הקטע AB.
א. מצאו פי כמה גדולה מהירות הנסיעה של מכונית א' בקטע הכביש המהיר ממהירות הנסיעה של מכונית ב' בקטע הכביש המהיר.
ב. כאשר הגיעה מכונית א' ליישוב B, הייתה מכונית ב' בקטע הכביש העירוני, במרחק 18 ק"מ מיישוב A. מצאו את המרחק בין יישוב A ובין יישוב B.
ג. כאשר הגיעה מכונית א' ליישוב B היא מייד יצאה חזרה לכיוון היישוב A, וכאשר הגיעה מכונית ב' ליישוב A היא מייד יצאה חזרה לכיוון היישוב B.
בדרכן חזרה נפגשו המכוניות בקטע הכביש המהיר. מצאו באיזה מרחק מן היישוב B נפגשו המכוניות בדרכן חזרה."""

q2 = """2. נתונה סדרה הנדסית A שאיבריה הם a₁, a₂, a₃, ..., aₘ ובה m איברים (m הוא מספר טבעי גדול מ־4). כל איברי הסדרה A הם שליליים.
נתון: סכום m−4 האיברים האחרונים בסדרה הוא פי 16 מסכום 4 האיברים הראשונים בסדרה.
א(1). מצאו את מנת הסדרה.
א(2). האם הסדרה A עולה, יורדת או לא עולה ולא יורדת? נמקו את תשובתכם.
המשיכו את הסדרה A כך שנוצרה סדרה הנדסית אין־סופית.
נתונה סדרה אין־סופית B שאיבריה מקיימים: bₙ = aₙ / kⁿ, כאשר k הוא פרמטר שונה מ־0 ולכל n טבעי.
ב. הוכיחו כי הסדרה B היא סדרה הנדסית, והביעו את המנה שלה באמצעות k.
ג. נתון כי סכום הסדרה B מתכנס. מצאו את תחום הערכים האפשרי של k.
ד. נתון: מנת הסדרה B היא 1/4, סכום הסדרה הוא 9−. מצאו את הערך של b₁ ואת הערך של k.
ה. בסדרה B מחקו כל איבר שלישי (b₃, b₆, b₉, ...). מצאו את סכום האיברים הנותרים."""

q3 = """3. בכד א' יש 10 כדורים אדומים ו־15 כדורים צהובים, ובכד ב' יש רק כדורים אדומים.
דנה בוחרת באקראי כד ומוציאה ממנו באקראי כדור.
אם הכדור צהוב, היא מוציאה באקראי כדור שני מאותו הכד (הוצאה ללא החזרה).
אם הכדור הראשון אדום, היא מחזירה את הכדור לכד ושוב מוציאה באקראי כדור מאותו הכד.
א. ידוע שדנה הוציאה שני כדורים באותו הצבע. מהי ההסתברות ששניהם צהובים?
ב. דנה מחזירה לכד את הכדורים שהוציאה. יעל מבצעת את התהליך הזה:
היא בוחרת באקראי כד, מוציאה ממנו באקראי כדור אחד ומחזירה אותו לכד.
יעל חוזרת על תהליך זה עד שהיא מוציאה כדור אדום, מחזירה אותו לכד ומפסיקה להוציא כדורים.
מצאו את ההסתברות שיעל ביצעה תהליך זה 6 פעמים בדיוק.
ג. העבירו חלק מן הכדורים מכד ב' לכד א'. לאחר מכן בחרו באקראי כד והוציאו ממנו באקראי כדור אחד.
נתון כי לאחר ההעברה ההסתברות שהכדור שהוציאו היה אדום היא 19/24.
האם ייתכן שלפני ההעברה היו בכד ב' 10 כדורים? נמקו את תשובתכם."""
