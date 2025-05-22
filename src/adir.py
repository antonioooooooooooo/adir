from gpt4all import GPT4All
from nomic import embed
from pathlib import Path
from PIL import Image
import pytesseract
model = GPT4All("orca-mini-3b-gguf2-q4_0.gguf")

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
        if not american:
            return model.generate("generate SAT "+category+" question.", max_tokens=1024)
        return model.generate("generate multiple choice SAT " + category + " question", max_tokens=1024)

def requestHint(question : str):
    with model.chat_session():
        return model.generate(question+" ,give me a small hint for solving" , max_tokens=1024)

def toggleSoultion(question : str, explain : bool):
    with model.chat_session():
        if not explain:
            return model.generate(question+"Solve it. don't explain" , max_tokens=1024)
        return model.generate(question + "Solve it. explain.", max_tokens=1024)


#q = generateQuestion("calculus", True)
#print (q)
#verify_sol(ocr_to_text(test_path))
#print(requestHint(q))
