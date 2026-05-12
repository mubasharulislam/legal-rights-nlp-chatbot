# NLP Pipeline

## Overview

The NLP pipeline is a retrieval-based question answering pipeline. It maps a natural-language user query to the most relevant topic in a curated legal knowledge base. The system does not train a supervised classifier; instead, it uses sparse vector retrieval with keyword scoring.

## Pipeline Stages

```text
User Query
  |
  v
Text Normalization
  |
  v
TF-IDF Query Vectorization
  |
  v
Cosine Similarity Against Topic Matrix
  |
  v
Keyword Scoring
  |
  v
Hybrid Ranking
  |
  v
Topic Selection
  |
  v
Response Formatting
```

## Topic Document Construction

Each topic in the knowledge base is converted into a retrievable document. The document is formed by concatenating:

- topic title
- keywords
- answer text
- procedural steps
- example user questions

This gives the retrieval model access to both formal topic descriptions and likely user phrasings.

## Text Normalization

The query normalization step:

- trims leading and trailing whitespace
- lowercases text
- collapses repeated whitespace

Keyword scoring also extracts alphabetic tokens with a regular expression. The current system does not perform stemming, lemmatization, spelling correction, named entity recognition, or language identification.

## TF-IDF Representation

When `scikit-learn` is available, the system builds a `TfidfVectorizer` with:

- lowercasing enabled
- English stop-word removal
- unigram and bigram features

The topic corpus is transformed into a sparse topic-document matrix. At query time, the user message is transformed into the same vector space.

## Similarity Scoring

The system computes cosine similarity between the query vector and each topic vector. Higher cosine similarity indicates greater lexical overlap after TF-IDF weighting.

The vector score is scaled before being combined with the keyword score:

```text
combined_score = keyword_score + (tfidf_cosine_similarity * 8)
```

This weighting makes TF-IDF influential while still allowing carefully selected keywords to improve domain-specific matching.

## Keyword Scoring

The keyword component uses three matching patterns:

- multi-word phrase match: `+3.0`
- exact single-word match: `+2.0`
- prefix-style match for longer keywords: `+1.0`

This helps capture legally important expressions that may be too sparse to dominate TF-IDF similarity by themselves.

## Topic Selection

The system ranks all topics by combined score and selects the highest-scoring topic. If the score is at least `1.0`, the topic is treated as relevant and returned. Otherwise, the system returns a fallback message describing the scope of supported questions.

## Fallback Mode

If `scikit-learn` is not installed, the system skips vector indexing and uses keyword scoring only. This fallback keeps the chatbot operational but reduces the system's ability to match broader lexical overlap.

## NLP Interpretation

The pipeline can be described as a hybrid sparse retrieval model:

- TF-IDF provides statistical term weighting.
- Cosine similarity provides query-document ranking.
- Manual keywords provide symbolic domain knowledge.
- The JSON knowledge base functions as a small curated corpus.

The pipeline is interpretable and easy to inspect, which is useful for a legal-information prototype. Its main limitation is that it relies on surface-form similarity rather than deep semantic understanding.
