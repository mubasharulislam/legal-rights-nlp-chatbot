# Legal Rights NLP Chatbot

A retrieval-based NLP chatbot focused on workplace harassment awareness and legal information access in Pakistan.

The project is designed as a Computational Linguistics / NLP portfolio system that maps natural-language user queries to a curated legal knowledge base using:

- TF-IDF vectorization
- cosine similarity retrieval
- keyword scoring
- structured response generation

The chatbot provides general legal information only. It is not a substitute for advice from a lawyer, ombudsperson office, police, court, or trusted local support service.

---

# Research Motivation and Research Question

Recent NLP systems increasingly rely on semantic embeddings and transformer-based architectures for information retrieval. However, before adopting advanced models, it is important to understand the capabilities and limitations of classical retrieval methods. This project therefore explores a retrieval-based legal chatbot built on TF–IDF vectorization and cosine similarity matching.
The project is guided by the following research question:

What are the strengths and limitations of TF–IDF vectorization and cosine similarity for information retrieval in a legal-domain chatbot?

The objective is to investigate how effectively lexical representations retrieve relevant legal information, identify the linguistic situations in which they perform well, and examine where they struggle with ambiguity, paraphrasing, and semantic variation. By exploring these limitations through practical implementation, the project aims to develop a stronger understanding of information retrieval foundations before moving toward more advanced neural approaches.

# System Architecture

<p align="center">
  <img src="outputs/screenshots/tfidf_retrieval_pipeline_architecture.png" width="700"/>
</p>

---

# Chatbot Interface

## Homepage Interface

![Homepage](outputs/screenshots/homepage_interface.png)

## Example Conversation

![Conversation](outputs/screenshots/chatbot_conversation_example.png)

---

# Retrieval Evaluation

The system retrieves the most relevant legal topic using TF-IDF vectorization and cosine similarity ranking.

## Retrieval Metadata Example

![Retrieval Evaluation](outputs/screenshots/retrieval_evaluation_example.png)

---

# NLP Retrieval Analysis

The project includes a Jupyter notebook for retrieval experimentation and evaluation.

## Retrieval Ranking Table

![Notebook Analysis](outputs/screenshots/notebook_retrieval_analysis.png)

## Cosine Similarity Visualization

![Visualization](outputs/screenshots/retrieval_similarity_visualization.png)

---

# Key Features

- Flask web application with JSON chat API
- Curated legal knowledge base in `data/legal_knowledge.json`
- TF-IDF query-document matching with unigram and bigram features
- Graceful keyword-only fallback when `scikit-learn` is unavailable
- Optional OpenAI response generation grounded in retrieved knowledge-base context
- Responsive browser chat interface with quick prompts and local chat history
- `/topics` endpoint for dataset inspection
- `/health` endpoint for service and matching-mode status
- Unit tests for dataset loading, retrieval behavior, and API endpoints
- Cosine similarity ranking
- Explainable retrieval metadata
- Responsive frontend chat interface
- Quick-prompt legal guidance system

---

# NLP Methodology

The system treats each legal topic as a retrievable document.

Each topic document is constructed from:
- title
- keywords
- example questions
- legal guidance answer
- procedural steps

User queries are:
1. normalized
2. vectorized using TF-IDF
3. compared against topic documents using cosine similarity
4. ranked using hybrid lexical scoring

This makes the project a small-domain information retrieval system rather than an open-domain generative chatbot.

Core NLP concepts demonstrated:
- document representation
- sparse vector retrieval
- TF-IDF weighting
- n-gram features
- cosine similarity
- lexical overlap
- explainable retrieval
- threshold-based fallback behavior

Detailed methodology: [docs/methodology.md](docs/methodology.md)

## Architecture Summary

```text
Browser UI
  -> Flask API Backend
  -> TF-IDF Retrieval Engine
  -> optional OpenAI context-grounded generation
  -> Cosine Similarity Matching
  -> structured legal knowledge base
  -> formatted response with disclaimer
  -> Fronted Display
```

Project structure:

```text
chatbot_project/
  app.py                         Flask routes, API workflow, optional OpenAI layer
  chatbot_engine.py             Knowledge-base loading, TF-IDF indexing, retrieval, formatting
requirements.txt
data/
    legal_knowledge.json         Structured topic corpus
templates/
    index.html                   Browser chat interface
tests/
    test_chatbot.py              Unit and endpoint tests
notebooks/
    retrieval_analysis.ipynb
docs/
    methodology.md               NLP and retrieval methodology
    error_analysis.md            Retrieval failure modes and limitations
    future_work.md               Multilingual and low-resource NLP directions
reports/ 
    evaluation_examples.md       Qualitative retrieval examples
```

Additional documentation:

- [Architecture diagram](docs/architecture_diagram.md)
- [System architecture](docs/system_architecture.md)
- [NLP pipeline](docs/nlp_pipeline.md)
- [API workflow](docs/api_workflow.md)
- [Dataset structure](docs/dataset_structure.md)
- [Query processing pipeline](docs/query_processing_pipeline.md)
- [Evaluation examples](reports/evaluation_examples.md)
- [Retrieval evaluation examples](reports/retrieval_evaluation_examples.md)

# Technologies Used

- Python
- Flask
- HTML / CSS / JavaScript
- Scikit-learn
- TF-IDF Vectorization
- Cosine Similarity
- JSON Knowledge Base
- Jupyter Notebook
```

## Setup

Install dependencies:

```powershell
pip install -r requirements.txt
```

Run the app:

```powershell
python app.py
```

Open the browser interface:

```text
http://127.0.0.1:5000
```

## Optional OpenAI Integration

The application works without an API key. To enable optional context-grounded generation, create or update `.env`:

```text
ENABLE_OPENAI=true
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=your_model_here
```

When enabled, the app sends the top retrieved knowledge-base context with the user query. If the API call fails, the system falls back to local retrieval.

## Testing

Run with Python's built-in test runner:

```powershell
python -m unittest discover
```

Or with pytest:

```powershell
pytest
```

# Findings and Limitations

The retrieval experiments indicate that TF–IDF vectorization combined with cosine similarity can effectively identify relevant legal topics when user queries share meaningful lexical overlap with documents in the knowledge base. The approach is computationally efficient, transparent, and interpretable, allowing retrieval decisions to be inspected through similarity scores and ranking information.
At the same time, several limitations became apparent during retrieval analysis. The system relies primarily on lexical matching and may struggle when users express the same legal concept through substantially different vocabulary or indirect descriptions. Ambiguous queries can also correspond to multiple legal topics, while the retrieval mechanism currently returns a single best match. In addition, contextual meaning and broader semantic relationships are only partially captured by sparse vector representations.
These observations highlight both the usefulness and the limitations of classical retrieval techniques. While they provide an effective foundation for domain-specific information access, they also illustrate why recent NLP research increasingly incorporates semantic embeddings, contextual representations, and transformer-based reranking methods.

## Research Direction

The current system is an English-language sparse retrieval prototype. Future work focuses on Roman Urdu NLP, multilingual retrieval, code-switching detection, semantic embeddings, transformer-based reranking, and low-resource legal information retrieval.

Future work details: [docs/future_work.md](docs/future_work.md)

# Conclusion

This project investigated the strengths and limitations of TF-IDF vectorization and cosine similarity for information retrieval in a legal-domain chatbot. The results demonstrate that classical retrieval methods can provide transparent and efficient access to legal information within a curated knowledge base. At the same time, retrieval analysis revealed challenges related to semantic variation, indirect language, and query ambiguity. These findings provide practical insight into the foundations of information retrieval and motivate future exploration of embedding-based and transformer-based approaches for legal NLP applications.