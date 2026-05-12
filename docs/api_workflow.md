# API Workflow

## Overview

The Flask API provides a small set of endpoints for the browser interface, chatbot interaction, system health, and topic inspection. The API is designed for local demonstration and portfolio use rather than public production deployment.

## Endpoints

### `GET /`

Renders the browser chat interface.

Response type:

```text
text/html
```

The route passes `knowledge_base.suggested_prompts` into the template so the interface can display quick topic buttons.

### `POST /chat`

Accepts a user message and returns a chatbot reply.

Request body:

```json
{
  "message": "How do I file a complaint?"
}
```

Response body:

```json
{
  "reply": "A complaint can usually be made..."
}
```

Workflow:

1. Parse JSON from the request body.
2. Read the `message` field.
3. Pass the message to `get_response()`.
4. Return the selected response as JSON.

If the request body is missing or invalid, the API treats the message as an empty string and returns a prompt asking the user to type a question.

### `GET /topics`

Returns a summary of the knowledge-base topics.

Response body:

```json
[
  {
    "id": "complaint",
    "title": "How to file a complaint",
    "keywords": ["complaint", "complain", "report"],
    "examples": ["how do I file a complaint"]
  }
]
```

This endpoint supports dataset inspection and helps reviewers understand the domain coverage.

### `GET /health`

Returns basic service status.

Response body:

```json
{
  "status": "ok",
  "topics": 20,
  "matching": "tfidf+keyword"
}
```

The `matching` value indicates whether the system is using the TF-IDF plus keyword path or the keyword-only fallback.

## Response Selection Logic

The central API workflow is implemented in `get_response(user_input)`:

```text
user_input
  |
  v
openai_response(user_input)
  |
  | if configured and successful
  v
generated answer

otherwise
  |
  v
knowledge_base.answer(user_input)
  |
  v
retrieval-based answer
```

The optional OpenAI layer is controlled by environment variables:

- `ENABLE_OPENAI`
- `OPENAI_API_KEY`
- `OPENAI_MODEL`

When any required value is missing, the system uses local retrieval.

## Error Handling

The API is intentionally conservative:

- invalid JSON falls back to an empty dictionary
- missing messages are handled as empty input
- failed OpenAI requests fall back to local retrieval
- frontend network errors are shown as a browser message

This behavior keeps the demo stable and ensures that the local knowledge base remains the default answer source.

## API Limitations

The current API does not provide:

- authentication
- rate limiting
- persistent server-side conversation history
- structured confidence scores in the `/chat` response
- top-k topic rankings
- explicit error codes for low-confidence retrieval

For research evaluation, a future endpoint could return the top-k ranked topics, raw scores, selected matching method, and threshold decision.
