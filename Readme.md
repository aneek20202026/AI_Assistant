# AI Assistant Project

## Overview
This project is a multi-functional AI assistant built using Python and Streamlit. It integrates the Groq API with the `llama-3.3-70b-versatile` model and utilizes FAISS-based vector databases for efficient data retrieval. The assistant supports multi-turn conversations, document-based Q&A, logging, caching, and adheres to ethical AI practices.


## Hosted Application
Access the live version of this app at: [AI Assistant](<https://aiassistant-demo.streamlit.app/>)

## Setup Instructions

### Prerequisites
Ensure you have the following installed:
- Python 3.x
- pip
- Virtual environment (optional but recommended)

### Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/aneek20202026/AI_Assistant.git
   cd <repository-directory>
   ```
2. Create a virtual environment (optional):
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

### Running the Application
Start the Streamlit app:
```sh
streamlit run app.py
```

## Project Architecture
- **Streamlit Frontend**: Provides a simple UI for user interactions.
- **Backend (Python)**: Manages API calls, data processing, logging, and caching.
- **FAISS-based Vector Store**: Handles document storage and retrieval for different functionalities:
  - **Document Store**: Stores uploaded documents.
  - **QA Store**: Holds Q&A-related contexts.
  - **Summary Store**: Stores document summarizations.
  - **Sentiment Store**: Stores sentiment analysis results.
  - **NER Store**: Stores named entity recognition (NER) data.
  - **Code Store**: Stores code snippets and related embeddings.
- **Groq API**: Powers the AI assistant using `llama-3.3-70b-versatile`.

## Configuration
Update the `.env` file with necessary API keys and configuration parameters:
```
GROQ_API_KEY=your_api_key
```

## Technical Report
### Design Choices & Technical Decisions
- **FAISS for Vector Storage**: Enables fast similarity search for embeddings.
- **Multiple Vector Stores**: Organizes data for different use cases (documents, QA, summaries, etc.).
- **Logging & Caching**: Implemented to improve efficiency and debugging.
- **Ethical Considerations**: Ensuring fairness, transparency, and accuracy in responses.

### Optimization & Debugging Strategies
- Caching responses to reduce redundant API calls.
- Using logging for tracking system behavior and errors.
- Optimizing FAISS indexing for efficient retrieval.

### Potential Enhancements
- Adding support for more LLM models.
- Expanding document processing capabilities.
- Enhancing UI with additional user controls.


