import streamlit as st
import json
import pandas as pd
from models.llm_wrapper import LLMWrapper
from models.text_processing import preprocess_text
from utils.logging import log_event
from retrieval.vector_store import document_store, qa_store, summary_store, sentiment_store, ner_store

# Initialize LLM Wrapper
llm = LLMWrapper(model_type="groq")

st.title("AI Assistant")

task = st.selectbox("Choose a task", [
    "Summarization", "Sentiment Analysis", "NER", "Q&A", "Upload & Store Document"
])

if task == "Summarization":
    text = st.text_area("Enter text to summarize:")
    if st.button("Clear Summarization DB"):
        summary_store.clear()
        st.success("DB has been reset.")
    if st.button("Summarize"):
        if summary_store.is_empty():
            summary_store.add_document("Summarize the given user input") 
        log_event("User requested summarization")
        response = llm.generate(text, summary_store)
        summary_store.add_document(
            f"User: {preprocess_text(text)}\nResponse: {preprocess_text(response)}"
        )
        st.write(response)

elif task == "Sentiment Analysis":
    text = st.text_area("Enter text:")
    if st.button("Clear Sentiment DB"):
        sentiment_store.clear()
        st.success("DB has been reset.")
    if st.button("Analyze Sentiment"):
        if sentiment_store.is_empty():
            sentiment_store.add_document("Analyze the sentiment of the user from the provided input text") 
        log_event("User requested sentiment analysis")
        response = llm.generate(text, sentiment_store)
        sentiment_store.add_document(
            f"User: {preprocess_text(text)}\nResponse: {preprocess_text(response)}"
        )
        st.write(response)

elif task == "NER":
    text = st.text_area("Enter text:")
    if st.button("Clear NER DB"):
        ner_store.clear()
        st.success("DB has been reset.")
    if st.button("Extract Entities"):
        if ner_store.is_empty():
            ner_store.add_document("Extract named entities from the user input text") 
        log_event("User requested Named Entity Recognition (NER)")
        response = llm.generate(text,ner_store)
        ner_store.add_document(
            f"User: {preprocess_text(text)}\nResponse: {preprocess_text(response)}"
        )
        st.write(response)

elif task == "Q&A":
    context = st.text_area("Enter context:")
    question = st.text_input("Enter question:")
    if st.button("Clear Q&A DB"):
        qa_store.clear()
        st.success("DB has been reset.")
    if st.button("Get Answer"):
        if qa_store.is_empty():
            qa_store.add_document("Answer the Question of the user provided the context") 
        log_event("User requested Question Answering")
        prompt = f"Context:\n{context}\n\nQuestion:\n{question}"
        response = llm.generate(prompt,qa_store)
        qa_store.add_document(
            f"Context:\n{preprocess_text(context)}\n\nQuestion:\n{preprocess_text(question)}\nResponse:\n{preprocess_text(response)}"
        )
        st.write(response)

elif task == "Upload & Store Document":
    uploaded_file = st.file_uploader("Upload a document (TXT, CSV, JSON)", type=["txt", "csv", "json"])
    if st.button("Clear Document DB"):
        document_store.clear()
        st.success("Document storage has been reset.")

    if uploaded_file is not None:
        file_type = uploaded_file.name.split(".")[-1]

        try:
            if file_type == "txt":
                text = uploaded_file.read().decode("utf-8")
                log_event(f"Stored TXT document: {uploaded_file.name}")

            elif file_type == "csv":
                df = pd.read_csv(uploaded_file)
                text = df.to_string()
                log_event(f"Stored CSV document: {uploaded_file.name}")

            elif file_type == "json":
                data = json.load(uploaded_file)
                text = json.dumps(data, indent=2)
                log_event(f"Stored JSON document: {uploaded_file.name}")
            
            
            if document_store.is_empty():
                document_store.add_document(
                    preprocess_text(f"Document:\n{preprocess_text(text)}")
                )
                log_event(f"Indexed document content in vector store: {uploaded_file.name}")

            st.success(f"Stored {uploaded_file.name} successfully!")

            st.subheader("Ask Questions about the Uploaded Document")
            question = st.text_input("Enter question:")
            if st.button("Get Answer"):
                log_event("User requested Q&A on uploaded document")

                prompt = f"Question:\n{question}"
                response = llm.generate(prompt, document_store)
                document_store.add_document(
                    f"Question:\n{preprocess_text(question)}\nResponse:\n{preprocess_text(response)}"
                )
                st.write(response)
        except Exception as e:
            log_event(f"Error storing document: {str(e)}")
            st.error(f"Failed to store document: {str(e)}")
