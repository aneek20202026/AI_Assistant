import os
import openai
from groq import Groq
from dotenv import load_dotenv
from utils.caching import cache_response
from utils.logging import log_event
# from transformers import pipeline

load_dotenv()

class LLMWrapper:
    def __init__(self, model_type="groq"):
        self.model_type = model_type

        if model_type == "groq":
            self.client = Groq()
            self.model_name = "llama-3.3-70b-versatile"
        elif model_type == "openai":
            openai.api_key = os.getenv("OPENAI_API_KEY")
        # elif model_type == "huggingface":
        #     self.pipeline = pipeline("text-generation", model="gpt2")

    @cache_response  # Caching LLM responses
    def generate(self, prompt, vector_store):
        log_event(f"Generating response for prompt: {prompt}")

        # Retrieve relevant documents for better context
        retrieved_docs = vector_store.search(prompt, top_k=2)
        if retrieved_docs:
            log_event(f"Retrieved relevant documents: {retrieved_docs}")
            context = "\n".join(retrieved_docs)
            prompt = f"{context}\n\n{prompt}" 
            print("#########################################",prompt,"#####################################")
            
        if self.model_type == "groq":
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=1,
                max_completion_tokens=1024,
                top_p=1,
                stream=False,
                stop=None
            )
            reply = response.choices[0].message.content

        elif self.model_type == "openai":
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )
            reply = response["choices"][0]["message"]["content"]
        # elif self.model_type == "huggingface":
        #     return self.pipeline(prompt, max_length=100)[0]["generated_text"]

        log_event(f"Generated response: {reply[:100]}...")
        return reply

