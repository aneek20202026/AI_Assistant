import re
import json
import pandas as pd

def load_text(file_path):
    if file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    elif file_path.endswith(".csv"):
        return pd.read_csv(file_path).to_string()
    elif file_path.endswith(".json"):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        raise ValueError("Unsupported file format")

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text
