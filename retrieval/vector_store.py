import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class VectorStore:
    def __init__(self, name, model_name="all-MiniLM-L6-v2", dim=384):
        self.name = name 
        self.model = SentenceTransformer(model_name)
        self.index = faiss.IndexFlatL2(dim)
        self.documents = []

    def add_document(self, text):
        embedding = self.model.encode([text])[0]
        self.index.add(np.array([embedding]))
        self.documents.append(text)

    def is_empty(self):
        return len(self.documents) == 0

    def search(self, query, top_k=2):
        if len(self.documents) == 0:
            return [f"No data found in {self.name} storage."]

        query_embedding = self.model.encode([query])[0]
        distances, indices = self.index.search(np.array([query_embedding]), top_k)

        valid_results = [
            self.documents[i] for i in indices[0] if i < len(self.documents)
        ]
        return valid_results if valid_results else [f"No relevant data found in {self.name}."]
    
    def clear(self):
       
        self.index.reset() 
        self.documents = [] 


document_store = VectorStore(name="documents")
qa_store = VectorStore(name="qa_contexts")  
summary_store = VectorStore(name="summarizations")
sentiment_store = VectorStore(name="sentiments") 
ner_store = VectorStore(name="entities")    
code_store = VectorStore(name="code")    