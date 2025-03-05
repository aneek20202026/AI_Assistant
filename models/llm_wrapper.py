import os
import openai
from groq import Groq
from dotenv import load_dotenv
from utils.caching import cache_response
from utils.logging import log_event
from transformers import pipeline

load_dotenv()

class LLMWrapper:
    def __init__(self, model_type="groq"):
        self.model_type = model_type

        if model_type == "groq":
            self.client = Groq()
            self.model_name = "llama-3.3-70b-versatile"
        elif model_type == "openai":
            openai.api_key = os.getenv("OPENAI_API_KEY")
        elif model_type == "huggingface":
            self.pipeline = pipeline("text-generation", model="gpt2")

    def check_ethics(self, text):
        log_event(f"Checking ethics for: {text[:100]}...")

        moderation_prompt = (
            "You are an AI ethics filter. Analyze the following text and determine whether it contains harmful, "
            "offensive, illegal, or unethical content. Respond with 'SAFE' if it is appropriate, or 'FLAGGED' "
            "if it violates ethical standards.\n\n"
            f"Text: {text}\n\nResponse:"
        )

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": moderation_prompt}],
            temperature=0, 
            max_completion_tokens=10,
            top_p=1,
            stream=False,
            stop=None
        )

        reply = response.choices[0].message.content.strip()

        if "FLAGGED" in reply:
            log_event(f"Ethical violation detected: {text[:100]}...")
            return False, "This prompt violates ethical guidelines."

        return True, None

    @cache_response  # Caching LLM responses
    def generate(self, prompt, vector_store):
        log_event(f"Generating response for prompt: {prompt}")

        is_safe, warning_message = self.check_ethics(prompt)
        if not is_safe:
            return warning_message

        # Retrieve relevant documents for better context
        retrieved_docs = vector_store.search(prompt, top_k=2)
        if retrieved_docs:
            log_event(f"Retrieved relevant documents: {retrieved_docs}")
            context = "\n".join(retrieved_docs)
            prompt = f"{context}\n\n{prompt}" 
            
        if self.model_type == "groq":
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=1,
                max_completion_tokens=5000,
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
        elif self.model_type == "huggingface":
            return self.pipeline(prompt, max_length=100)[0]["generated_text"]

        log_event(f"Generated response: {reply[:100]}...")
        is_safe, warning_message = self.check_ethics(reply)
        if not is_safe:
            return "The generated response was flagged as inappropriate."

        return reply

