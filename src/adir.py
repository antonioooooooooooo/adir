from gpt4all import GPT4All
from nomic import embed
from pathlib import Path
from PIL import Image
import pytesseract
#model = GPT4All("orca-mini-3b-gguf2-q4_0.gguf")

model = GPT4All("Meta-Llama-3-8B-Instruct.Q4_0.gguf")

def generateQuestion(category: str, hebrew: bool) -> str:
curr_dir = Path.cwd()
img_path = curr_dir / "assets" / "test.png"
test_path = curr_dir / "assets" / "test.png"

#embeddings = embed.image([str(img_path)])['embeddings']
#heb = "in hebrew"

def ocr_to_text(path: str) -> str:
    # Optional: set path to tesseract binary if not in PATH (Windows) ### ANNOTATE IF NOT IN WINDOWS
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    # Load image
    #img_path = Path("assets/pool.jpeg")
    img_path = Path(path)
    image = Image.open(img_path)

    # Perform OCR
    text = pytesseract.image_to_string(image)

    #print("Extracted Text:")
    #print(text)
    return text


def verify_sol(text: str) -> bool:
    answer = model.generate("answer only YES or NO: is '"+text+"' a good solution?", max_tokens=1024)
    return answer == 'YES'


def generateQuestion(category : str, american: bool) -> str:
    with model.chat_session():
        if not hebrew:
            question = model.generate("generate SAT "+category+" question.", max_tokens=1024)
        else:
            question = model.generate(
                "Generate a maths question in the category: " + category +
                ", in the style of the israeli SAT exam \"5 unit bagrut\". Here is a question for example: " +
                "נתונה סדרה הנדסית A שאיבריה הם 3 2 1 ... , a , ,a a , ובה m איברים )m הוא מספר טבעי גדול מ־ 4(.\n" +
                "נתון: כל איברי הסדרה A הם שליליים.\n" +
                "סכום - 4 m האיברים האחרונים בסדרה הוא פי 16 מסכום - 4 m האיברים הראשונים בסדרה.\n" +
                "א. )1( מצאו את מנת הסדרה A .\n" +
                ")2( האם הסדרה A עולה, יורדת או לא עולה ולא יורדת? נמקו את תשובתכם.\n" +
                "המשיכו את הסדרה A כך שנוצרה סדרה הנדסית אין־סופית.\n" +
                "a b לכל n טבעי. k הוא פרמטר שונה מ־ 0 .\n" +
                "n n k\n" +
                "n\n" +
                "נתונה סדרה אין־סופית B שאיבריה מקיימים =\n" +
                "ב. הוכיחו כי הסדרה B היא סדרה הנדסית, והביעו את המנה שלה באמצעות k .\n" +
                "נתון כי סכום הסדרה B מתכנס.\n" +
                "ג. מצאו את תחום הערכים האפשרי של k .\n" +
                "4 .\n" +
                "1\n" +
                "נתון: מנת הסדרה B היא\n" +
                "סכום הסדרה B הוא 9 - .\n" +
                "ד. מצאו את הערך של k ואת הערך של 1b .\n" +
                "בסדרה B מחקו כל איבר שלישי 9 6 3 (... b , b b , ( .\n" +
                "ה. מצאו את סכום האיברים הנותרים.\n" +
                "Please write it only in hebrew (no english at all) with no additional text (only the question).\n" +
                "If there are several parts to the question (for example questions א,ב,ג), make sure to write them on different lines.\n" +
                "Please note that if there are several parts, the first one must be א, second must be ב, third must be ג and so on.",
                max_tokens=1024
            )

        return question

def requestHint(question: str):
    with model.chat_session():
        hint = model.generate(
            "This is the current question that the user has been given by the system:\n\n" +
            question +
            "\n\nPlease provide the user with a small hint for solving the question, which gives them a direction but doesn't completely solve the problem." +
            "Please generate the response in hebrew and don't add any additional text, and avoid using any text in English.",
            max_tokens=1024
        )
        return hint

def toggleSoultion(question: str, explain: bool):
    with model.chat_session():
        if not explain:
            solution = model.generate(
                "This is the current question that the user has been given by the system:\n\n:" +
                question +
                "Solve it in hebrew (do not use any english text). Please do not add explanations.",
                max_tokens=1024
            )
        else:
            solution = model.generate(
                "This is the current question that the user has been given by the system:\n\n:" +
                question +
                "Solve it in hebrew (do not use any english text). Please add explanations.",
                max_tokens=1024
            )
        return solution


#q = generateQuestion("calculus", True)
#print (q)
#verify_sol(ocr_to_text(test_path))
#print(requestHint(q))
