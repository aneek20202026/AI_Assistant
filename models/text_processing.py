import re
import spacy
import subprocess

try:
    nlp=spacy.load("en_core_web_sm")
except OSError:
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp=spacy.load("en_core_web_sm")

def preprocess_text(text):
    text = text.lower()
    
    text = re.sub(r"[^\w\s]", "", text)
    doc = nlp(text)

    processed_text = " ".join([token.lemma_ for token in doc if not token.is_stop])
    
    return processed_text
