# Query Processing Pipeline

## Overview

The query processing pipeline converts a user's natural-language question into a ranked topic match. It is implemented primarily by the `ChatbotKnowledgeBase` class in `chatbot_engine.py`.

## Processing Steps

```text
Raw user input
  |
  v
Input validation
  |
  v
Normalization
  |
  v
TF-IDF scoring
  |
  v
Keyword scoring
  |
  v
Score combination
  |
  v
Threshold decision
  |
  v
Formatted response or fallback response
```

## 1. Input Validation

The Flask route reads the user message from the JSON body:

```json
{
  "message": "Can WhatsApp messages be evidence?"
}
```

If the message is missing, `get_response()` passes an empty string to the retrieval engine. The engine returns:

```text
Please type a question so I can help.
```

## 2. Normalization

The `_normalize()` method:

- strips whitespace
- lowercases the message
- replaces repeated whitespace with a single space

Example:

```text
"  Can WhatsApp   Messages be Evidence?  "
```

becomes:

```text
"can whatsapp messages be evidence?"
```

## 3. TF-IDF Scoring

If vector retrieval is available, `_tfidf_scores()` transforms the normalized query into the same TF-IDF vector space as the topic documents.

The system computes cosine similarity between:

- the query vector
- each topic document vector

The result is a list of vector scores, one score per topic.

## 4. Keyword Scoring

The `_keyword_score()` method compares the query with each topic's keyword list.

It awards:

- `3.0` for multi-word keyword phrase matches
- `2.0` for exact keyword token matches
- `1.0` for prefix-style partial matches on longer keywords

Example:

```text
Query: "Can an intern complain?"
Topic keyword: "intern complain"
```

This may receive a strong phrase-based keyword score.

## 5. Score Combination

For each topic, the system combines keyword and vector scores:

```text
combined_score = keyword_score + (tfidf_score * 8)
```

The multiplier increases the influence of TF-IDF cosine similarity while preserving the value of manually curated legal keywords.

## 6. Topic Ranking

The system iterates through all topics and tracks the topic with the highest combined score.

The output of this stage is a `TopicMatch` object containing:

- `topic`: the best matching topic or `None`
- `score`: the combined retrieval score
- `method`: either `tfidf+keyword` or `keyword`

## 7. Threshold Decision

If the best topic has a score of at least `1.0`, it is considered relevant.

If no topic reaches the threshold, the system returns a scope-setting fallback response. This fallback tells users the chatbot can help with workplace harassment questions in Pakistan and suggests supported areas.

## 8. Response Formatting

When a topic is selected, `_format_topic_response()` returns:

- the topic answer
- a "Useful next steps" list
- reference context, when sources are present
- the global legal-information disclaimer

This produces a controlled response grounded in the knowledge base.

## Example Query Walkthrough

Query:

```text
Can WhatsApp messages be evidence?
```

Expected processing:

1. Normalize to lowercase.
2. Compute TF-IDF similarity against all topic documents.
3. Match keywords such as `whatsapp`, `whatsapp messages`, `message evidence`, and `evidence`.
4. Rank evidence-related or online-harassment topics highly.
5. Select the strongest topic.
6. Return answer text with evidence-preservation steps.

## Research Notes

This pipeline is interpretable but limited. It is useful for demonstrating:

- sparse retrieval
- hybrid lexical scoring
- query-document matching
- domain lexicon design
- threshold-based fallback behavior

Future research improvements could include top-k output, query expansion, spelling correction, dense embeddings, intent classification, multilingual preprocessing, and clarification questions for ambiguous queries.
