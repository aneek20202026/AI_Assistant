from models.llm_wrapper import LLMWrapper

llm = LLMWrapper()

def summarize_text(text):
    prompt = f"Summarize this:\n{text}"
    return llm.generate(prompt)

def analyze_sentiment(text):
    prompt = f"Analyze the sentiment of this text and return positive, negative, or neutral:\n{text}"
    return llm.generate(prompt)

def extract_entities(text):
    prompt = f"Extract named entities from the following text:\n{text}"
    return llm.generate(prompt)

def answer_question(context, question):
    prompt = f"Context: {context}\nQuestion: {question}\nAnswer:"
    return llm.generate(prompt)
