from gpt4all import GPT4All
model = GPT4All("orca-mini-3b-gguf2-q4_0.gguf")

def generateQuestion(category : str, american: bool) -> str:
    with model.chat_session():
        if not american:
            return model.generate("generate SAT "+category+" question.", max_tokens=1024)
        return model.generate("generate multiple choice SAT " + category + " question.", max_tokens=1024)

def requestHint(question : str):
    with model.chat_session():
        return model.generate(question+" ,give me a small hint for solving" , max_tokens=1024)

def toggleSoultion(question : str, explain : bool):
    with model.chat_session():
        if not explain:
            return model.generate(question+"Solve it. don't explain" , max_tokens=1024)
        return model.generate(question + "Solve it. explain.", max_tokens=1024)


#q = generateQuestion("calculus")
#print(q)

#print(requestHint(q))
