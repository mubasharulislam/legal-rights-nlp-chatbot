# System Architecture

## Overview

The Legal Rights Chatbot is organized as a lightweight retrieval-based question answering system with a Flask delivery layer. The application separates user interaction, API routing, knowledge-base retrieval, optional generative response support, and browser rendering.

The current implementation is intentionally compact:

- `app.py` defines the Flask app, HTTP routes, environment loading, optional OpenAI call, and final response selection.
- `chatbot_engine.py` defines the knowledge-base object, topic indexing, TF-IDF retrieval, keyword scoring, and response formatting.
- `data/legal_knowledge.json` stores the domain corpus.
- `templates/index.html` provides the browser chat interface.
- `tests/test_chatbot.py` validates dataset loading, representative retrieval behavior, and Flask endpoints.

## High-Level Components

```text
Browser UI
  |
  | POST /chat
  v
Flask API Layer
  |
  | get_response(user_input)
  v
Optional Generative Layer
  |
  | fallback when disabled or unavailable
  v
Retrieval Engine
  |
  | topic match + formatted response
  v
JSON Response
```

## Component Responsibilities

### Browser Interface

The browser interface in `templates/index.html` provides:

- a chat input area
- quick topic prompts
- local browser chat history
- optional browser speech recognition
- basic error handling when the Flask server is unavailable

The frontend does not perform NLP. It sends the user message to the backend through `POST /chat`.

### Flask API Layer

The Flask layer in `app.py` is responsible for:

- loading environment variables from `.env`
- initializing the knowledge base from JSON
- serving the browser interface
- exposing the chat API
- exposing metadata endpoints
- choosing between optional OpenAI generation and local retrieval

The main response function is `get_response(user_input)`. It first attempts the optional generative layer if enabled. If that layer is disabled, incomplete, or unavailable, the system returns the local retrieval-based answer.

### Retrieval Engine

The retrieval engine in `chatbot_engine.py` is the core NLP component. It:

- loads topics from the JSON dataset
- constructs a document representation for each topic
- builds a TF-IDF matrix when `scikit-learn` is installed
- computes keyword scores
- computes cosine similarity between the query and topic documents
- combines vector and keyword scores
- formats the selected topic into an answer

### Data Layer

The data layer is a structured JSON knowledge base. Each topic represents a retrievable document with legal-information content and user-facing response text. The dataset is small, manually curated, and domain-specific.

### Optional Generative Layer

The optional OpenAI integration is a response-generation extension, not the primary retrieval mechanism. It receives the top retrieved context from the local knowledge base and the user question. If the API call fails or configuration is missing, the system silently falls back to local retrieval.

## Runtime Flow

1. The user enters a question in the browser.
2. JavaScript sends the message to `POST /chat`.
3. Flask extracts the `message` field from the request body.
4. `get_response()` checks whether OpenAI generation is enabled.
5. If enabled and successful, the generated answer is returned.
6. Otherwise, the retrieval engine finds the closest legal topic.
7. The selected topic is formatted with answer text, useful next steps, source context, and disclaimer.
8. Flask returns the answer as JSON.
9. The browser renders the chatbot response.

## Design Rationale

This architecture supports a research-oriented NLP prototype because the retrieval engine is separable from the web interface. The same `ChatbotKnowledgeBase` class can be reused in notebooks, batch evaluation scripts, or future retrieval experiments without depending on the browser interface.

The design also keeps legal-information responses controlled. The default answer is drawn from curated knowledge-base content rather than unconstrained generation.
